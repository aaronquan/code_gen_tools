import sys
import json
import os
from typing import TypedDict
from dataclasses import dataclass
from common import ShaderDetails, fileNameToShaderDetail, startingWhiteSpace

output_path = "outputs/web/"
input_path = "inputs/cpp/"

class Config(TypedDict):
  pass
'''
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

def startingWhiteSpace(s: str) -> int:
  i = 0
  while i < len(s) and (s[i] == ' ' or s[i] == '\t'):
    i+=1
  return i
'''
def hasOut(s: str, outs: dict[str, int]) -> bool:
  for key in outs:
    if s.startswith(key):
      return True
  return False

def cppToWebGenerate(fn: str, config: Config):
  print(fn)
  try:
    with open(input_path+fn) as f:
      content = f.read()
      file_lines = []
      outs = {}
      for line in content.splitlines():
        if line.startswith('#version'):
          file_lines.append('precision medium float;')
        elif line.startswith("out "):
          sp = line.split(' ')
          outs[sp[2][:-1]] = 0
          print(f"out var {sp[2][:-1]}")
        elif line.startswith("in"):
          rep = line.replace("in", "varying")
          
          file_lines.append(rep)
        else:
          sps, tabs = startingWhiteSpace(line)
          clean_line = line[sps+tabs:]
          if hasOut(clean_line, outs):
            line = sps*' '+tabs*'\t'+"gl_"+clean_line
          file_lines.append(line)
      print(file_lines)
      output = "\n".join(file_lines)
      out_file = open(f"{output_path}{fn}", 'w')
      out_file.write(output)

  except FileNotFoundError:
    print("File not found")

def main():
  cf = open("config.json")
  config = json.load(cf)
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    if fn == "shader_sources" or fn == "all":
      # convert all
      print(os.listdir(input_path))
      for file in os.listdir(input_path):
        cppToWebGenerate(file, config)
    else:
      cppToWebGenerate(fn, config)
  else:
    print("No Input")


main()