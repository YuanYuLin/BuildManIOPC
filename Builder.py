import json
import importlib
import os
import sys

'''
'''
class PackageInfo :
  def __init__(self, pkg_cfg):
    self.__pkg = pkg_cfg
    print(json.dumps(self.__pkg, indent=2))

  def getName(self):
    return self.__pkg['name']

  def getRootFs(self):
    return self.__pkg['dir.rootfs']

  def getTemporaryDir(self, sub_dir=''):
    return os.path.join(self.__pkg['dir.pkg.tmp'], sub_dir)

  def getRepository(self):
    return self.__pkg['dir.pkg.repo']

  def getSources(self):
    return self.__pkg['dir.pkg.src']

class Tools :

  def checkSize_and_splitFilelist(folder):
    #TODO
    for filename in os.listdir(folder):
      statinfo = os.stat(ops.path_join(folder, filename))
      if statinfo.st_size > 90000000:
        print(folder, filename, statinfo.st_size)
        split_file_name = "{}.part-".format(filename)
        cmd = ['split', '--verbose', '-d', '-b', '90000000', file_name, split_file_name]
        rsp=subprocess.run(cmd, cwd=workdir)
        rsp.check_returncode()

  def mergeFiles(workspace, output_file_name, file_list):
    #TODO
    for filename in os.listdir(folder):
      if filename.endswith(".part-info") :
    fp = file(os.path.join(workspace, output_file_name), 'wb')
    for file_name in file_list:        
      with open(os.path.join(workspace, file_name)) as src_file:
        fp.write(src_file.read())
    fp.close()                                             
                                          
    return os.path.join(workspace, output_file_name)

class Package :
  def __init__(self, pkg_info, builder):
    self.builder = builder
    self.info = pkg_info
    self.tools = Tools()
      
class Builder :
  def __init__(self, CFG):
    work_dir = CFG['WORKDIR']
    pkg_list = CFG['PACKAGES']
    pkgs_dir = CFG['PKGSDIR']

    self.packages = []
    for pkg_name, info in pkg_list.items() :
      pkg_enable = info["ENABLE"]
      if not pkg_enable :
        continue

      info['name']           = pkg_name
      info['dir.output']     = os.path.join(os.path.abspath(work_dir), 'output')
      info['dir.rootfs']     = os.path.join(os.path.abspath(info['dir.output']), 'rootfs')
      info['dir.pkg.repo']   = os.path.join(os.path.abspath(pkgs_dir), pkg_name)
      info['dir.pkg.src']    = os.path.join(os.path.abspath(info['dir.pkg.repo']), 'sources')
      info['dir.pkg.tmp']    = os.path.join(os.path.abspath(info['dir.output']), pkg_name)
      info['dir.pkg.build']  = os.path.join(os.path.abspath(info['dir.pkg.tmp']), 'build')
      info['dir.pkg.install']= os.path.join(os.path.abspath(info['dir.pkg.tmp']), 'install')
      info['dir.pkg.sdk']    = os.path.join(os.path.abspath(info['dir.pkg.tmp']), 'sdk')
      for key in info :      
        if 'dir.' in key :   
          if not os.path.exists(info[key]) :
            os.makedirs(info[key])

      try :
        rule_path = '{}.{}.{}'.format(pkgs_dir, pkg_name, 'RULE')
        mod = importlib.import_module(rule_path)
        PkgRule = getattr(mod, "Rule")
        self.packages.append(PkgRule(PackageInfo(info), self))
      except Exception as err:
        print("Error: please check file {}".format(rule_path))
        print(err)
        sys.exit(1)

  def __touch_file(self, file_path):
    with open(file_path, 'w') as fp :
      fp.write('')

  def __action_traversal(self, pkg, ACTION, actions):
    act_reached = False
    for act in actions :
      if act == ACTION :
        act_reached = True

      func = actions[act]
      if func :
        info = pkg.info
        pkg_name = info.getName()
        pkgdstdir = info.getTemporaryDir()
        pkg_flag = os.path.join(pkgdstdir, ".{}".format(act))
        if not os.path.exists(pkg_flag) :
          print("PKG {} - {} Begin".format(pkg_name, act))
          func_ret = func()
          print("PKG {} - {} End".format(pkg_name, act))
          if func_ret :
            self.__touch_file(pkg_flag)

      if act_reached :
        break

  def getPackage(self, pkg_name):
    for pkg in self.packages :
      info = pkg.info
      if pkg_name == info.getName() :
        return pkg

  def checkDependency(self, pkg_name):
    if self.getPackage(pkg_name) :
      pass
    else:
      print("Package dependency error {}".format(pkg_name))
      sys.exit(1)

  def run_rule(self, ACTION):
    for pkg in self.packages :
      action_build = {                             
            'ENV'     :pkg.env,
            'EXTRACT' :pkg.extract,
            'PATCH'   :pkg.patch,
            'CONFIGURE':pkg.configure,      
            'BUILD'   :pkg.build,                          
            'INSTALL' :pkg.install,
            'SDK'     :pkg.sdk,
            'ALL'     :None
            }        
      action_clean = {
            'ENV'     :pkg.env,
            'CLEAN'   :pkg.clean                
            } 
      if ACTION in action_build :
        self.__action_traversal(pkg, ACTION, action_build)
      elif ACTION in action_clean :
        self.__action_traversal(pkg,  ACTION, action_clean)
      else :
        print("{} NOT supported...".format(ACTION))

