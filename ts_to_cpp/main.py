import sys
from dataclasses import dataclass
from enum import Enum



ts_type_to_ctype = {
  "Int32": "int",
  "boolean": "bool"
}

class NodeTypes(Enum):
  FUNCTION = 1
  FOR = 2
  IF = 3
  RETURN = 4

class ASTNode:
  def __init__(self):
    self.type = NodeTypes.FUNCTION
    self.name = ""


@dataclass
class FunctionNode:
  name: str
  return_type: str
  params: list[str]
  nodes: list[ASTNode]



class AST:
  def __init__(self):
    self.nodes = [] # function node

def main():
  
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    try:
      with open(fn) as f:
        content = f.read()
        print(content)
    except FileNotFoundError:
      print("not found")
  pass


main()