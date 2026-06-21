from dataclasses import dataclass


def cleanString(s: str) -> str:
  if s == "": 
    return s
  s = s.lstrip().rstrip()
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



def nextWord(s: str, i: int) -> tuple[str, int]:
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
        if any(s[i] == c for c in sp_chars):
            break
        i+=1
    return i+1

def nextChar(s: str, i: int, c: str) -> int:
    while i < len(s):
        if s[i] == "'" or s[i] == '"':
            i = nextQuote(s, s[i], i)
        elif s[i] == c:
            return i
        i += 1
    return len(s)

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

    node = TypeNode(is_single, type_name, single_type, types)

    return node, i

def parseVariableNode(code: str, i: int):
    pass

def parseTSCode(code: str):
    i = 0
    while i < len(code):
        if code[i].isalpha():
            first, i = nextWord(code, i)
            first = cleanString(first)
            if first == "type":
                node, i = parseTypeNode(code, i)
                print(node)
            elif first == "const":
               print("is const")
            else:
               print(f"|{first}|")

        i += 1


