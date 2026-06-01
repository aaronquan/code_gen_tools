from __future__ import annotations
import sys
from dataclasses import dataclass
from enum import Enum



ts_type_to_ctype = {
  "Int32": "int",
  "boolean": "bool"
}
  
def insideBrackets(s: str) -> int:
  open_b = 0
  quote = None
  for i in range(len(s)):
    if quote == None:
      if s[i] == "'" or s[i] == '"':
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

class NodeType(Enum):
  FUNCTION = 1
  FOR = 2
  IF = 3
  RETURN = 4
  VAR = 5
  CLASS = 6


operators = ["+", "-"]

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
  typ = NodeType.FUNCTION
  print(first)
  if first == "function":
    typ = NodeType.FUNCTION
  elif first == "for":
    typ = NodeType.FOR
  elif first == "if":
    typ = NodeType.IF
  elif first == "return":
    typ = NodeType.RETURN
  elif first == "var" or first == "const" or first == "let":
    typ = NodeType.VAR
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

@dataclass
class ValueNode:
  value: ValueNode | str
  next: OperatorNode | None

@dataclass
class VariableAssignmentNode:
  name: str
  value_node: ValueNode 


def parseVariableAssignmentLine(line: str) -> VariableAssignmentNode:
  pass

def parseFunctionHeader(line: str) -> ASTNode:
  pass

@dataclass
class FunctionNode:
  name: str
  return_type: str
  params: list[str]
  nodes: list[ASTNode]



class AST:
  def __init__(self):
    self.types = []
    self.function_nodes = [] # function node
    self.variable_nodes = []

def main():
  
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    try:
      with open(fn) as f:
        content = f.read()
        for line in content.splitlines():
          tp, i = getTypeOfLine(line)
          rest = line[i:].lstrip()
          if tp == NodeType.VAR:
            print(rest)
    except FileNotFoundError:
      print("not found")
  pass


main()