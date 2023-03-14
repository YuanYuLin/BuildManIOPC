import importlib
import json
import sys
import os

def debug(debug_txt):
  with open(file_path, 'w') as fp :
    fp.write('')

def init_jsoncfg(json_path):
  json_obj = {}
  with open(json_path) as fp :
    json_obj = json.load(fp)

  return json_obj

def init_package_list(CFG):
  root_dir = CFG['ROOTDIR']
  pkg_list = CFG['PACKAGES']
  pkgs_dir = CFG['PKGSDIR']

  for pkg_name, pkg in pkg_list.items() :
    pkg_enable = pkg["ENABLE"]
    if not pkg_enable :
      continue

    pkg['package.name']               = pkg_name

    pkg['package.dir.out']            = os.path.join(os.path.abspath(root_dir), 'output')
    pkg['package.dir.rootfs']         = os.path.join(os.path.abspath(pkg['package.dir.out']), 'rootfs')
    pkg['package.dir.pkg.src']        = os.path.join(os.path.abspath(pkgs_dir), pkg_name)
    pkg['package.dir.pkg.dst']        = os.path.join(os.path.abspath(pkg['package.dir.out']), pkg_name)
    pkg['package.dir.pkg.build']      = os.path.join(os.path.abspath(pkg['package.dir.pkg.dst']), 'build')
    pkg['package.dir.pkg.install']    = os.path.join(os.path.abspath(pkg['package.dir.pkg.dst']), 'install')
    pkg['package.dir.pkg.sdk']        = os.path.join(os.path.abspath(pkg['package.dir.pkg.dst']), 'sdk')
    for key in pkg :
      if 'package.dir.' in key :
        if not os.path.exists(pkg[key]) :
          os.makedirs(pkg[key])

    try :
      rule_path = '{}.{}.{}.{}'.format(pkgs_dir, pkg_name, 'Rule', 'CONFIG')
      rule = importlib.import_module(rule_path)
      pkg['package.rule.env']           = rule.env
      pkg['package.rule.extract']       = rule.extract
      pkg['package.rule.patch']         = rule.patch
      pkg['package.rule.configure']     = rule.configure
      pkg['package.rule.build']         = rule.build
      pkg['package.rule.install']       = rule.install
      pkg['package.rule.sdk']           = rule.sdk
      pkg['package.rule.clean']         = rule.clean
    except :
      print("Error: please check file {}".format(rule_path))
      sys.exit(1)

def touch_file(file_path):
  with open(file_path, 'w') as fp :
    fp.write('')

def action_traversal(pkg, CFG, ACTION, actions):
  act_reached = False
  for act in actions :
    if act == ACTION :
      act_reached = True

    func = actions[act]
    if func :
      pkg_name = pkg['package.name']
      pkgdstdir = pkg['package.dir.pkg.dst']
      pkg_flag = os.path.join(pkgdstdir, ".{}".format(act))
      if not os.path.exists(pkg_flag) :
        if func(pkg_name, CFG) :
          touch_file(pkg_flag)

    if act_reached :
      break

def run_rules(CFG, ACTION):
  pkg_list = CFG['PACKAGES']
  for pkg_name, pkg in pkg_list.items() :
    pkg_enable = pkg["ENABLE"]
    if not pkg_enable :
      continue

    action_build = {
            'ENV'     :pkg['package.rule.env'],
            'EXTRACT' :pkg['package.rule.extract'], 
            'PATCH'   :pkg['package.rule.patch'], 
            'CONFIGURE':pkg['package.rule.configure'], 
            'BUILD'   :pkg['package.rule.build'], 
            'INSTALL' :pkg['package.rule.install'], 
            'SDK'     :pkg['package.rule.sdk'], 
            'ALL'     :None
            }
    action_clean = {
            'ENV'     :pkg['package.rule.env'],
            'CLEAN'   :pkg['package.rule.clean']
            }

    if ACTION in action_build :
      action_traversal(pkg, CFG, ACTION, action_build)
    elif ACTION in action_clean :
      action_traversal(pkg, CFG, ACTION, action_clean)
    else :
      print("{} NOT supported...".format(ACTION))

def main(argc, argv):
  if argc < 2 :
    print("{} <packages_dir> <package_config_file> ACTION".format(argv[0]))
    print("ACTION:[ALL, EXTRACT, PATCH, CONFIGURE, BUILD, INSTALL, CLEAN]")
    sys.exit(1)

  packages_dir = argv[1]
  json_path = argv[2]
  ACTION = argv[3]
  CFG=init_jsoncfg(json_path)
  CFG['ROOTDIR'] = os.path.dirname(os.path.abspath(sys.argv[0]))
  CFG['PKGSDIR'] = packages_dir
  init_package_list(CFG)
  run_rules(CFG, ACTION)

if __name__ == '__main__' :
  main(len(sys.argv), sys.argv)

