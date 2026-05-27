import sys
from dataclasses import dataclass
from enum import Enum



ts_type_to_ctype = {
  "Int32": "int",
  "boolean": "bool"
}
  
def insideBrackets(s: str) -> str:
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

def getTypeOfLine(s: str) -> NodeType:
  sp = s.lstrip().split(" ") # split on special character
  first = sp[0]
  print(first)
  if first == "function":
    return NodeType.FUNCTION
  elif first == "for":
    return NodeType.FOR
  elif first == "if":
    return NodeType.IF
  elif first == "return":
    return NodeType.RETURN
  elif first == "var" or first == "const" or first == "let":
    return NodeType.VAR


class ASTNode:
  def __init__(self):
    self.type = NodeType.FUNCTION
    self.name = ""
    self.children = [] # ASTNode[]

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
        print(content)
        for line in content.splitlines():
          getTypeOfLine(line)
    except FileNotFoundError:
      print("not found")
  pass


main()