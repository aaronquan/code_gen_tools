import parser

ts_type_to_ctype = {
  "Int32": "int",
  "Float": "float",
  "Double": "double",
  "Short": "short",
  "boolean": "bool",
  "string": "std::string"
}

cpp_optional = "std::optional"

def getCppType(pt: parser.Type) -> str:
    ts = pt.name
    if ts[-1] == "":
        pass
    return ts_type_to_ctype[ts] if ts in ts_type_to_ctype else ts

def typeNodeToCpp(node: parser.TypeNode) -> str:
    s = ""
    if node.is_type:
        if node.type_name in ts_type_to_ctype:
            s += f"typedef {ts_type_to_ctype[node.type_name]} {node.name};"
    else:
        s += f"struct {node.name} {'{'}\n"
        for ty in node.types:
            print(ty)
            s += f"\t{getCppType(ty.type)} {ty.name};\n"
            s += "};"
    return s
def valueNodeToCpp(value_node: parser.ValueNode):
    pass