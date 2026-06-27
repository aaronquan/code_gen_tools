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
class ObjectType:
    name: str
    type: Type

@dataclass
class Type:
    name: str
    generic: list[GenericNode]
    is_optional: bool
    is_pointer: bool

@dataclass 
class GenericNode:
   name: str
   extends: str

@dataclass
class TypeNode:
  name: str
  is_single: bool # is single type
  generics: list[GenericNode]
  single_type: Type | None
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

#todo: globally fix types!

def nextWord(s: str, i: int) -> tuple[str, int]:
    i = nextNonSpace(s, i)
    st = i
    sp_chars = [" ", "=", "(", ":", "\n", '<']
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

# starts without the opening bracket
def nextBracket(s: str, i:int=0, ebr=")", obr="(") -> int:
    bi = 0
    for j in range(i, len(s)):
        if s[j] == '"' or s[j] == "'":
            j = nextQuote(s, s[j], j)
        if s[j] == obr:
            bi += 1
        elif s[j] == ebr:
            if bi == 0:
                return j
            else:
               bi -= 1
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

def nextEnd(s: str, i: int) -> int:
    while i < len(s):
        if s[i] == "'" or s[i] == '"':
            i = nextQuote(s, s[i], i)
        elif s[i] == ";" or s[i] == "\n":
            return i
        i += 1
    return len(s)

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

def parseGenerics(s: str) -> list[GenericNode]:
    gens = []
    def addGen(st: str):
        sp = st.split()
        tp = sp[0]
        ex = ""
        if len(sp) >= 3 and sp[1] == "extends":
            ex = sp[2] 
        gens.append(GenericNode(tp, ex))
    i = 0
    e = nextChar(s, 0, ",")
    while e != len(s):
        addGen(s[i:e])
        i = e+1
        e = nextChar(s, e+1, ",")
    addGen(s[i:e])
    return gens

def parseType(s: str, is_optional: bool) -> Type:
    name = cleanString(s)
    gens = []
    is_pointer = False
    opt = s.find('|')
    if opt != -1:
        name = cleanString(s[:opt])
        rem = cleanString(s[opt+1:])
        if rem == "undefined":
            is_optional = True
        elif rem == "null":
            is_pointer = True
    if name[-1] == ">":
        o = nextChar(name, 0, "<")
        gen_str = name[o+1:]
        gens = parseGenerics(gen_str)
        name = cleanString(name[:o])
    return Type(name, gens, is_optional, is_pointer)

def parseObjectType(s: str) -> ObjectType | None:
    i = 0
    while i < len(s):
        if s[i] == '"' or s[i] == "'":
            i = nextQuote(s, s[i], i)
        elif s[i] == ':':
            first = cleanString(s[0:i])
            is_optional = False
            if first[-1] == "?":
               first = first[:-1]
               is_optional = True
            second = cleanString(s[i+1:])
            typ = parseType(second, is_optional)
            return ObjectType(first, typ)
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
            pt = parseObjectType(content)
            if pt != None:
                types.append(pt)
            st = j
        j += 1
    last = cleanString(rest[st:j])
    pt = parseObjectType(last)
    if pt != None:
        types.append(pt)
    return types, b

def parseTypeNode(code: str, i: int) -> tuple[TypeNode, int]:
    type_name, i = nextWord(code, i)
    generics = []
    if code[i] == "<":
        i+=1
        e = nextBracket(code, i, ">", "<")
        gen_str = code[i:e]
        generics = parseGenerics(gen_str)
        i = e+1
       
    i = code.find("=", i)
    i+=1
    i = nextNonSpace(code, i)
    single_type = None
    is_single = True
    types = []
    if code[i] == "{":
        is_single = False
        types, i = parseMultiType(code, i)
    else:
        e = nextEnd(code, i)
        single_type_str = code[i:e]
        #print(f"sg {single_type_str}")
        single_type = parseType(single_type_str, False)
        i = e+1

    node = TypeNode(type_name, is_single, generics, single_type, types)

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
        i += 1
        ty = ValueNodeType.VALUENODE
        e = nextBracket(code, i)
        node, _ = parseValueNode(code[i:e], 0)
        
    elif code[i] == '{':
        i += 1
        ty = ValueNodeType.DICT
        e = nextBracket(code, i+1, '}', '{')
        print(code[i:e])
        dct = parseDict(code[i:e], 0)
        i = e+1
    else:
        s = cleanString(code[i:end_op])
        i = end_op
    
    #parsing operators
    while is_op and i < len(code):
        operator = code[i]
        i += 1
        end_op, is_op = nextOperator(code, i)
        vnode, _ = parseValueNode(code[i:end_op], 0)
        ops.append(OperatorNode(operator, vnode))
    
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


