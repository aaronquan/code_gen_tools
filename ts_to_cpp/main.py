from __future__ import annotations
import sys
from dataclasses import dataclass
from enum import Enum



ts_type_to_ctype = {
  "Int32": "int",
  "Float": "float",
  "Double": "double",
  "Short": "short",
  "boolean": "bool",

}
  
def insideBrackets(s: str) -> int:
  open_b = 0
  quote = None
  for i in range(len(s)):
    if quote == None and (s[i] == "'" or s[i] == '"'):
      quote = s[i]
    elif s[i] == quote:
      quote = None
    elif s[i] == '(':
      open_b+=1
    elif s[i] == ')':
      if open_b == 0:
        return i
      open_b-=1
  return len(s)

def nextBracket(s: str, i:int=0) -> int:
  for j in range(i, len(s)):
    if s[j] == '"' or s[j] == "'":
      j = nextQuote(s, s[j], j)
    if s[j] == ")":
      return j
  return len(s)


def nextQuote(s: str, qt:str="'", i:int=0) -> int:
  for j in range(i, len(s)):
    if s[j] == qt:
      return j

  return j

class NodeType(Enum):
  NONE = 0
  FUNCTION = 1
  FOR = 2
  IF = 3
  RETURN = 4
  VAR = 5
  CLASS = 6
  TYPE = 7
  BRACKETCLOSE = 8


operators = ["+", "-", "%"]

def firstWord(line: str, i: int=0) -> tuple[str, int]:
  sp_chars = [" ", "=", "("]
  st = i
  #i = 0
  while i < len(line):
    if any(line[i] == c for c in sp_chars):
        break
    i+=1
  return line[st:i], i

def lwhiteSpaceIndex(line: str) -> int:
  i = 0
  sp = [' ', '\n', '\t']
  while i < len(line):
    if all(line[i] != c for c in sp):
      break
    i+=1
  return i

def getTypeOfLine(line: str) -> tuple[NodeType, int]:
  #sp = s.lstrip().split(" ") # split on special character
  i = lwhiteSpaceIndex(line)
  first, i = firstWord(line, i)
  typ = NodeType.NONE
  if first == "function":
    typ = NodeType.FUNCTION
    i+=1
  elif first == "for":
    typ = NodeType.FOR
  elif first == "if":
    typ = NodeType.IF
  elif first == "return":
    typ = NodeType.RETURN
    i+=1
  elif first == "var" or first == "const" or first == "let":
    typ = NodeType.VAR
    i+=1
  elif first == "type":
    typ = NodeType.TYPE
  elif first == "}":
    typ = NodeType.BRACKETCLOSE
    
  return typ, i

class ASTNode:
  def __init__(self):
    self.type = NodeType.FUNCTION
    self.name = ""
    self.children = [] # ASTNode[]

@dataclass
class OperatorNode:
  operator: str
  value_node: ValueNode

# 1 + 1 -> VN(OP(+, VN(1), VN(1)))

@dataclass
class ValueNode:
  is_str: bool
  value: ValueNode | str
  operators: list[OperatorNode]

@dataclass
class VariableAssignmentNode:
  name: str
  type_hint: str
  value_node: ValueNode 


def parseVariableAssignmentLine(line: str, i: int) -> VariableAssignmentNode:
  st = i
  while i < len(line) and line[i] != '=':
    i+=1
  var_name = line[st:i-1]
  colon = var_name.find(":")
  type_hint = ""
  if colon != -1:
    type_hint = var_name[colon+1:].lstrip()
    var_name = var_name[:colon]

  st = i+1


  van = VariableAssignmentNode(var_name, type_hint, parseValueNode(line[st:]))
  print(van)
  return van

def parseValueNode(s: str) -> ValueNode:
  i = lwhiteSpaceIndex(s)

  ops, vals = splitOperators(s)
  op_nodes = []
  for j in range(len(ops)):
    is_str = vals[j+1][0] != "("
    vn = vals[j+1] if is_str else parseValueNode(vals[j+1][1:-1])
    op_node = OperatorNode(ops[j], ValueNode(is_str, vn, []))
    op_nodes.append(op_node)
  is_str = vals[0][0] != "("
  vn = vals[0] if is_str else parseValueNode(vals[0][1:-1])
  node = ValueNode(is_str, vn, op_nodes)
  #print(node)
  return node

def splitOperators(s: str) -> tuple[list[str], list[str]]:
  ops = []
  vals = []
  st = 0
  i = 0
  while i < len(s):
    i = nextSyntax(s, i)
    if i >= len(s): 
      break
    if any(s[i] == c for c in operators):
      vals.append(valueRemoveFluff(s[st:i]))
      ops.append(s[i])
      st = i+1

    i+=1
  vals.append(valueRemoveFluff(s[st:i]))
  return ops, vals

def valueRemoveFluff(s: str) -> str:
  s = s.lstrip().rstrip()
  if s[-1] == ';':
    return s[:-1]
  return s
    

@dataclass
class ParameterNode:
  name: str
  type: str
  default: ValueNode | None

@dataclass
class FunctionNode:
  name: str
  return_type: str
  params: list[ParameterNode]
  children: list[NodeSignature]

@dataclass 
class NodeSignature:
  type: NodeType
  index: int

def parseFunctionHeader(s: str) -> FunctionNode:
  i = 0
  while i < len(s) and s[i] != "(":
    i+=1
  name = s[:i]

  e = nextBracket(s, i)
  full_param_str = s[i+1:e]
  
  param_strs = parseFunctionParams(full_param_str, 0)

  params = []
  for p in param_strs:
    j = p.find(':')
    name = valueRemoveFluff(p[:j])
    p_type = valueRemoveFluff(p[j+1:])
    st = j+1
    j = p.find('=')
    default_node = None
    if j != -1:
      p_type = valueRemoveFluff(p[st:j])
      default_str = valueRemoveFluff(p[j+1:])
      default_node = parseValueNode(default_str)
    param_node = ParameterNode(name, p_type, default_node)
    params.append(param_node)

  remaining = s[e+1:]
  i = remaining.find(":")
  j = remaining.find("{")
  return_type = valueRemoveFluff(remaining[i+1:j])
  
  return FunctionNode(name, return_type, params, [])


# expects bracket contents of function params
def parseFunctionParams(s: str, i: int) -> list[str]:
  #i = nextBracket(s, i)
  #i+=1
  params = []
  st = i
  while i < len(s):
    i = nextSyntax(s, i)
    if s[i] == ",":
      params.append(valueRemoveFluff(s[st:i]))
      st = i+1
    i+=1
  params.append(valueRemoveFluff(s[st:i]))
  return params

def findInside(s: str, i:int=0) -> str:
  if s[i] == "'" or s[i] == '"':
    j = nextQuote(s, s[i], 1)
    return s[i+1:j]
  elif s[i] == "(":
    j = nextBracket(s, 1)
    return s[i+1:j]
  return s[i:]

def nextSyntax(s: str, i: int) -> int:
  if s[i] == '(':
    i = nextBracket(s, i+1)+1
  elif s[i] == '"' or s[i] == "'":
    i = nextQuote(s, s[i], i+1)+1
  return i
class AST:
  def __init__(self):
    self.types = []
    self.function_nodes = [] # function node
    self.variable_nodes = []
    self.type_nodes = []

def valueNodeToCStr(node: ValueNode) -> str:
  s = ""
  if node.is_str:
    s += node.value
  else:
    s += f"({valueNodeToCStr(node.value)})"
  for op in node.operators:
    s += op.operator + valueNodeToCStr(op.value_node)
  return s

def variableAssignNodeToCLine(node: VariableAssignmentNode) -> str:
  if node.type_hint == "":
    return ""
  line = f"{ts_type_to_ctype[node.type_hint]} {node.name} = {valueNodeToCStr(node.value_node)};"
  return line

@dataclass
class ReturnNode:
  value: ValueNode

def parseReturn(s: str):
  return ReturnNode(parseValueNode(s))


@dataclass
class Type:
  type: str
  name: str

@dataclass
class TypeNode:
  is_type: bool
  name: str
  type_name: str
  types: list[Type]

def parseTypeHeader(s: str):
  eq = s.find("=")
  name = s[:eq]
  rest = valueRemoveFluff(s[eq+1:])
  is_single = rest[0] == '{'
  type_name = rest
  types = []
  if rest[0] == is_single:
    #struct type
    type_name = ""
  return TypeNode(is_single, name, type_name, types)

def main():
  '''
  i1 = findInside("('fdasf'+4)", 0)
  print(i1)
  i1 = findInside("'fdasf'+4)", 0)
  print(i1)
  '''
  
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    ast = AST()
    try:
      with open(fn) as f:
        content = f.read()
        node_stack = []
        for line in content.splitlines():
          tp, i = getTypeOfLine(line)
          rest = line[i:].lstrip()
          if tp == NodeType.VAR:
            #print(rest)
            node = parseVariableAssignmentLine(line, i)
            print(variableAssignNodeToCLine(node))
          elif tp == NodeType.FUNCTION:
            node = parseFunctionHeader(rest)
            current_node = node
            print(node)
          elif tp == NodeType.RETURN:
            node = parseReturn(rest)
          elif tp == NodeType.TYPE:
            print(f"type: {rest}")
            node = parseTypeHeader(rest)
            if node.is_type:
              node_stack.append(NodeSignature(NodeType.TYPE, len(ast.type_nodes)))
              ast.type_nodes.append(node)
          elif tp == NodeType.BRACKETCLOSE:
            if len(node_stack) >= 1:
              node_stack.pop()
            else:
              print("No stack")
          else:
            if len(node_stack) >= 1:
              node_sig = node_stack[-1]

              #node = ast.
              print(f"{node_sig} {line}")
    except FileNotFoundError:
      print("not found")
  pass


main()