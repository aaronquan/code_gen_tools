import sys
import json
import os
from typing import TypedDict
from dataclasses import dataclass

output_path = "outputs/cpp/"
input_path = "inputs/web/"

class Config(TypedDict):
  pass

@dataclass
class ShaderDetails:
  file_name: str
  name: str
  cap_name: str
  short_type_name: str
  type_name: str
  cap_type_name: str

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

def startingWhiteSpace(s: str) -> tuple[int, int]:
  sps = 0
  tabs = 0
  i = 0
  while i < len(s) and (s[i] == ' ' or s[i] == '\t'):
    if s[i] == ' ':
      sps+=1
    elif s[i] == '\t':
      tabs+=1
    i+=1
  return sps, tabs

def webToCppGenerate(fn: str, config: Config):
  try:
    with open(fn) as f:
      content = f.read()
      file_lines = []
      for line in content.splitlines():
        if line.startswith('precision medium float;'):
          file_lines.append('') #todo
        elif line.startswith("varying"):
          pass
          
          #file_lines.append(rep)
        elif line.startswith("gl_"):
          pass
        else:
          ws = startingWhiteSpace(line)
          print(ws)
          new_line = line[ws:]
          print(new_line)
          file_lines.append(line)



  except FileNotFoundError:
    print("File not found")

def main():
  cf = open("config.json")
  config = json.load(cf)
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    if fn == "shader_sources" or fn == "all":
      # convert all
      for file in os.listdir(input_path):
        webToCppGenerate(file, config)
    else:
      webToCppGenerate(fn, config)


main()