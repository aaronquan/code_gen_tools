import sys
import json
import os
from typing import TypedDict
from dataclasses import dataclass

tab = "  "

class Config(TypedDict):
  shader_class_path: str
  source_class_path: str
  fragment_class: str
  vertex_class: str
  mixin_class: str
  matrix_3x3_class: str
  matrix_path: str
  program_path: str
  shader_class_path_back: str
  shader_program_mixin_class: str

@dataclass
class ShaderDetails:
  file_name: str
  name: str
  cap_name: str
  short_type_name: str
  type_name: str
  cap_type_name: str

@dataclass
class Uniform:
  full_var_name: str
  var_name: str
  type_name: str

@dataclass
class Attribute:
  full_var_name: str
  var_name: str
  type_name: str

def genUniform(line: str) -> Uniform:
  sp = line.split(' ')
  fvn = sp[2][:-1]
  return Uniform(fvn, fvn[2:] if fvn.startswith("u_") else fvn, sp[1])

def hasMatrixUniform(uniforms: list[Uniform]) -> bool:
  for uni in uniforms:
    if uni.type_name.startswith("mat"):
      return True
  return False

def genAttribute(line: str) -> Attribute:
  sp = line.split(' ')
  fvn = sp[2][:-1]
  return Attribute(fvn, fvn[2:] if fvn.startswith("a_") else fvn, sp[1])

def capitaliseVariable(var: str) -> str:
  sp = var.split("_")
  return "".join([part.capitalize() for part in sp])

def fileNameToShaderDetail(path: str) -> ShaderDetails:
  sp = path.split('/')
  full_file_name = sp[-1]
  sp_file = full_file_name.split('.')
  name = sp_file[0]
  cap_name = "".join([p[0].upper()+p[1:] for p in name.split('_')])
  short_ty = sp_file[-1]
  ty = "fragment" if short_ty == "frag" else "vertex"
  cty = ty.capitalize()
  return ShaderDetails(full_file_name, name, cap_name, short_ty, ty, cty)

def uniformTypeToSetterStrings(ty: str, config: Config) -> tuple[str,str,str]:
  if ty == "float":
    return ("a: GLfloat", "Float", "a")
  elif ty == "vec2":
    return ("a: GLfloat, b: GLfloat", "Float2", "a, b")
  elif ty == "vec3":
    return ("a: GLfloat, b: GLfloat, c: GLfloat", "Float3", "a, b, c")
  elif ty == "vec4":
    return ("a: GLfloat, b: GLfloat, c: GLfloat, d: GLfloat", "Float4", "a, b, c, d")
  elif ty == "mat3":
    return (f"mat: Matrix.{config['matrix_3x3_class']}", "Mat3", "mat.matrix")
  return ("", "", "")

def genSourceFile(sd: ShaderDetails, uniforms: list[Uniform],  conf: Config, attributes: list[Attribute] = []) -> str:
  class_type_name = conf['fragment_class'] if sd.type_name == "fragment" else conf['vertex_class']
  is_vertex = sd.type_name == "vertex"

  sf = f"import {sd.cap_name} from '{conf['source_class_path']}/{sd.file_name}?raw';\n"
  if hasMatrixUniform(uniforms):
    sf += f"import * as Matrix from '{conf['matrix_path']}';\n"
  sf += f"import * as Shader from '{conf['shader_class_path']}';\n\n"
  # shader source class
  sf += f"export class {sd.cap_name}{sd.cap_type_name}Shader{{\n"
  sf += f"{tab}static shader?: Shader.{class_type_name};\n"
  sf += f"{tab}static load(){{\n"
  sf += f"{tab}{tab}if(this.shader == undefined){{\n"
  sf += f"{tab}{tab}{tab}this.shader = new Shader.{class_type_name}();\n"
  sf += f"{tab}{tab}{tab}if(!this.shader.addSource({sd.cap_name})){{\n"
  sf += f"{tab}{tab}{tab}{tab}console.log('{sd.cap_name}: {sd.type_name} source not added');\n"
  sf += f"{tab}{tab}{tab}}}\n"
  sf += f"{tab}{tab}}}\n"
  sf += f"{tab}}}\n"
  sf += f"}}\n\n"
  # program mixin
  sf += f"export function {sd.cap_name}ShaderProgramMix<TBase extends Shader.{conf['mixin_class']}>(Base: TBase){{\n"
  sf += f"{tab}return class {sd.cap_name} extends Base{{\n"

  #add attribute declarations (vert only)
  if is_vertex:
    for att in attributes:
      sf += f"{tab}{tab}private declare {att.var_name}_attribute_location: GLint | null;\n" #TODO

  #add uniform declarations
  for uni in uniforms:
    sf += f"{tab}{tab}private declare {uni.var_name}_uniform_location: WebGLUniformLocation | null;\n"
  # setup fragment function
  sf += f"{tab}{tab}protected override setup{sd.cap_type_name}(){{\n"
  sf += f"{tab}{tab}{tab}this.{sd.type_name}_name = '{sd.cap_name}Shader';\n"
  sf += f"{tab}{tab}{tab}if({sd.cap_name}{sd.cap_type_name}Shader.shader){{\n"
  sf += f"{tab}{tab}{tab}{tab}this.program.add{sd.cap_type_name}({sd.cap_name}{sd.cap_type_name}Shader.shader)\n"
  sf += f"{tab}{tab}{tab}}}else{{\n"
  sf += f"{tab}{tab}{tab}{tab}throw new Error(`${{this.{sd.type_name}_name}} not loaded`);\n"
  sf += f"{tab}{tab}{tab}}}\n"
  sf += f"{tab}{tab}}}\n"

  #attribute location init (vertex only)
  if is_vertex:
    sf += f"{tab}{tab}protected override add{sd.cap_type_name}AttributeLocations(): void{{\n"
    for att in attributes:
      sf += f"{tab}{tab}{tab}this.{att.var_name}_attribute_location = this.program.getAttributeLocation('{att.full_var_name}');\n"
    sf += f"{tab}{tab}}}\n"

  #uniform location init
  sf += f"{tab}{tab}protected override add{sd.cap_type_name}UniformLocations(): void{{\n"
  for uni in uniforms:
    sf += f"{tab}{tab}{tab}this.{uni.var_name}_uniform_location = this.program.getUniformLocation('{uni.full_var_name}');\n"
  sf += f"{tab}{tab}}}\n"

  # uniform setters
  for uni in uniforms:
    utss = uniformTypeToSetterStrings(uni.type_name, conf)
    sf += f"{tab}{tab}set{capitaliseVariable(uni.var_name)}({utss[0]}){{\n"
    sf += f"{tab}{tab}{tab}this.program.set{utss[1]}(this.{uni.var_name}_uniform_location!, {utss[2]});\n"
    sf += f"{tab}{tab}}}\n"

  sf += f"{tab}}}\n"
  sf += f"}}\n"

  return sf

def generateFromFile(fn: str, config: Config) -> ShaderDetails:
  sd = fileNameToShaderDetail(fn)
  #print(sd)
  uniforms = []
  attributes = []
  try:
    with open(fn) as f:
      content = f.read()
      for line in content.splitlines():
        if line.startswith("uniform"):
          uniforms.append(genUniform(line))
        if line.startswith("attribute"):
          attributes.append(genAttribute(line))
          
    #print(uniforms)
    source_file = genSourceFile(sd, uniforms, config, attributes)
    print(source_file)
    output = open(f"outputs/{sd.type_name}/{sd.name}.ts", 'w')
    output.write(source_file)
  except FileNotFoundError:
    print("File not found")
  return sd

def generateCollectorFile(ty: str, config: Config):
  cap_type = ty.capitalize()
  files = os.listdir(f"outputs/{ty}")
  print(files)
  my_files = []
  for fn in files:
    name = fn.split(".")[0]
    cap_name = capitaliseVariable(name)
    my_files.append((name, cap_name))
    print(f"{name} {cap_name}")

  content = ""
  #imports
  content += f"import * as Shader from '{config['shader_class_path_back']}';\n"
  for file in my_files:
    content += f"import * as {file[1]} from '{config['program_path']}{file[0]}';\n"
  content += "\n"
  content += f"export function load{cap_type}Shaders(){{\n"
  for file in my_files:
    content += f"{tab}{file[1]}.{file[1]}{cap_type}Shader.load();\n"
  content += f"}}\n"
  if ty == "vertex":
    for file in my_files:
      content += f"export const {file[1]}Mixin = {file[1]}.{file[1]}ShaderProgramMix(Shader.{config['shader_program_mixin_class']});\n"
  else:
    for file in my_files:
      content += f"export const {file[1]}Mixin = {file[1]}.{file[1]}ShaderProgramMix;\n"
  output = open(f"outputs/{ty}.ts", "w")
  output.write(content)


def main():
  cf = open("config.json")
  config = json.load(cf)
  #print(config)
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    if fn == "shader_sources" or fn == "all":
      #all in folder
      for file in os.listdir("shader_sources"):
        generateFromFile(f"shader_sources/{file}", config)
    else:
      generateFromFile(fn, config)

  generateCollectorFile("fragment", config)
  generateCollectorFile("vertex", config)
main()