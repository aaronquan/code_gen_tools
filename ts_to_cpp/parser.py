from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

def cleanString(s: str) -> str:
  s = s.lstrip().rstrip()
  if s == "": 
    return s
  if s[-1] == ';':
    return s[:-1]
  return s

@dataclass
class Type:
  type: str
  name: str

@dataclass
class TypeNode:
  is_single: bool # is single type
  name: str
  single_type: str
  types: list[Type]

class ValueNodeType(Enum):
  STRING = 0
  VALUENODE = 1
  DICT = 2

@dataclass
class DictEntry:
  key: str
  value: ValueNode

@dataclass
class OperatorNode:
  operator: str
  value_node: ValueNode

@dataclass
class ValueNode:
  type: ValueNodeType
  #is_str: bool
  value_node: ValueNode | None
  string: str | None
  dict: list[DictEntry]
  operators: list[OperatorNode]

# 1 + 1 -> VN(OP(+, VN(1), VN(1)))

class ValueNodeType(Enum):
  STRING = 0
  VALUENODE = 1
  DICT = 2

@dataclass
class VariableAssignmentNode:
  name: str
  type_hint: str
  value_node: ValueNode
  #multi_line: bool


def nextWord(s: str, i: int) -> tuple[str, int]:
    i = nextNonSpace(s, i)
    st = i
    sp_chars = [" ", "=", "(", ":", "\n"]
    while i < len(s):
        if any(s[i] == c for c in sp_chars):
            break
        i+=1
    return s[st:i], i

def nextQuote(s: str, qt:str="'", i:int=0) -> int:
  for j in range(i, len(s)):
    if s[j] == qt:
      return j

  return len(s)

def nextBracket(s: str, i:int=0, br=")") -> int:
    for j in range(i, len(s)):
        if s[j] == '"' or s[j] == "'":
            j = nextQuote(s, s[j], j)
        if s[j] == br:
            return j
    return len(s)

def nextNonSpace(s: str, i:int) -> int:
    sp_chars = [" ", "\n", "\t"]
    while i < len(s):
        if all(s[i] != c for c in sp_chars):
            break
        i+=1
    return i

def nextChar(s: str, i: int, c: str) -> int:
    while i < len(s):
        if s[i] == "'" or s[i] == '"':
            i = nextQuote(s, s[i], i)
        elif s[i] == c:
            return i
        i += 1
    return len(s)

def nextSyntax(s: str, i: int) -> int:
  if s[i] == '(':
    i = nextBracket(s, i+1)+1
  elif s[i] == '"' or s[i] == "'":
    i = nextQuote(s, s[i], i+1)+1
  return i

# +, -, *, /
# -1 for no operator
def nextOperator(s: str, i: int) -> tuple[int, bool]:
    ops = ['+', '-', '*', '/']
    while i < len(s):
        i = nextSyntax(s, i)
        if i >= len(s):
           break
        if s[i] == ';' or s[i] == '\n':
           return i, False
        if any(s[i] == c for c in ops):
           return i, True
        
        i += 1
    return len(s), False

def parseSingleType(s: str) -> Type | None:
    i = 0
    while i < len(s):
        if s[i] == '"' or s[i] == "'":
            i = nextQuote(s, s[i], i)
        elif s[i] == ':':
            first = cleanString(s[0:i])
            second = cleanString(s[i+1:])
            print(f"{first} {second}")
            return Type(first, second)
        i+=1
    return None

def parseMultiType(code: str, i: int) -> tuple[list[Type], int]:
    types = []
    b = nextBracket(code, i, "}")
    rest = code[i+1:b]
    i = b
    j = 0
    st = 0
    while j < len(rest):
        if rest[j] == "'" or rest[j] == '"':
            j = nextQuote(rest, rest[j], j)
        elif rest[j] == ';' or rest[j] == ',':
            content = cleanString(rest[st+1:j])
            pt = parseSingleType(content)
            if pt != None:
                types.append(pt)
            st = j
        j += 1
    last = cleanString(rest[st:j])
    pt = parseSingleType(last)
    if pt != None:
        types.append(pt)
    return types, b

def parseTypeNode(code: str, i: int) -> tuple[TypeNode, int]:
    type_name, i = nextWord(code, i)
    i = code.find("=", i)
    i = nextNonSpace(code, i)
    single_type = ""
    is_single = True
    types = []
    if code[i] == "{":
        is_single = False
        types, i = parseMultiType(code, i)
    else:
       single_type, i = nextWord(code, i)
       single_type = cleanString(single_type)

    node = TypeNode(is_single, type_name, single_type, types)

    return node, i

def parseVariableNode(code: str, i: int) -> tuple[VariableAssignmentNode, int]:
    var_name, i = nextWord(code, i)
    i = nextNonSpace(code, i)
    hint = ""
    if code[i] == ":":
        i += 1
        hint, i = nextWord(code, i)
    i = nextNonSpace(code, i)
    i += 1 # = character
    i = nextNonSpace(code, i)
    node, i = parseValueNode(code, i)
    print(f"var: {var_name}")
    return VariableAssignmentNode(var_name, hint, node), i



def parseDict(s: str, i: int) -> list[DictEntry]:
    d = []
    if s[-1] == "}":
        s = s[:-1]

    def addDictEntry(st: str):
        if len(st) != 0:
            e = nextChar(st, 0, ":")
            key = cleanString(st[:e])
            val_node = parseValueNode(cleanString(st[e+1:]), 0)
            d.append(DictEntry(key, val_node))

    while i < len(s):
        e = nextChar(s, i, ",")
        dict_str = cleanString(s[i:e])
        addDictEntry(dict_str)
        i = e+1
    print(d)
    return d
   

def parseValueNode(code: str, i: int) -> tuple[ValueNode, int]:
    i = nextNonSpace(code, i)
    ty = ValueNodeType.STRING
    node = None
    s = None
    dct = None
    ops = []
    end_op, is_op = nextOperator(code, i)
    if code[i] == '(':
        ty = ValueNodeType.VALUENODE
        e = nextBracket(code, i)
        i += 1
        node, _ = parseValueNode(code[i:e], 0)
        
    elif code[i] == '{':
        ty = ValueNodeType.DICT
        e = nextBracket(code, i, '}')
        i += 1
        dct = parseDict(code[i:e], 0)
        i = e+1
    else:
        s = cleanString(code[i:end_op])
        #print(f"s: {s}")
        i = end_op
    
    #parsing operators
    while is_op and i < len(code):
        operator = code[i]
        #print(operator)
        i += 1
        end_op, is_op = nextOperator(code, i)
        vnode, _ = parseValueNode(code[i:end_op], 0)
        ops.append(OperatorNode(operator, vnode))
        #print(f"op_str: {code[i:end_op]}")
    
    return ValueNode(ty, node, s, dct, ops), i

def parseTSCode(code: str):
    i = 0
    while i < len(code):
        if code[i].isalpha():
            first, i = nextWord(code, i)
            first = cleanString(first)
            i = nextNonSpace(code, i)
            if first == "type":
                node, i = parseTypeNode(code, i)
                print(node)
            elif first == "const" or first == "let" or first == "var":
                print("is const")
                node, i = parseVariableNode(code, i)
                print(node)
            else:
                print(f"|{first}|")

        i += 1


