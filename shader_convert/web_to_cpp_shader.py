import sys
import json
import os
from typing import TypedDict
from dataclasses import dataclass

def main():
  cf = open("config.json")
  config = json.load(cf)
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    if fn == "shader_sources" or fn == "all":
      # convert all

main()