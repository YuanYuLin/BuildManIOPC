import os
import sys
import json
from Builder import Builder

def init_jsoncfg(json_path):
  json_obj = {}
  with open(json_path) as fp :
    json_obj = json.load(fp)

  return json_obj

def main(argc, argv):
  if argc < 2 :
    print("{} <package_config_file> ACTION".format(argv[0]))
    print("ACTION:[ALL, EXTRACT, PATCH, CONFIGURE, BUILD, INSTALL, CLEAN]")
    sys.exit(1)

  workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
  json_path = argv[1]
  ACTION = argv[2]
  packages_dir = 'packages'
  output_dir = 'output'
  cfg_obj = init_jsoncfg(json_path)
  cfg_obj['WORKDIR'] = workdir
  cfg_obj['PKGSDIR'] = packages_dir
  cfg_obj['OUTPUTDIR'] = output_dir
  cfg_obj['ACTION'] = ACTION

  builder = Builder(cfg_obj)
  builder.run_rule(ACTION)
  pkg = builder.getPackage('test')
  print(pkg)

if __name__ == '__main__' :
  main(len(sys.argv), sys.argv)
