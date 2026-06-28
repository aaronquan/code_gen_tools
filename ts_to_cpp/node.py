from __future__ import annotations
#from parser import ValueNode
from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
  #NONE = 0
  FUNCTION = 1
  FOR = 2
  IF = 3
  RETURN = 4
  VAR = 5
  CLASS = 6
  TYPE = 7

#representation of any other node
@dataclass 
class NodeSignature:
  type: NodeType
  index: int

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

@dataclass
class ParameterNode:
  name: str
  type: Type
  default: ValueNode | None

@dataclass
class FunctionNode:
  name: str
  return_type: TypeNode
  params: list[ParameterNode]
  children: list[NodeSignature]

class ValueNodeType(Enum):
  STRING = 0
  VALUENODE = 1
  DICT = 2
  FUNCTION = 3

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

@dataclass
class VariableAssignmentNode:
  name: str
  type_hint: str
  value_node: ValueNode