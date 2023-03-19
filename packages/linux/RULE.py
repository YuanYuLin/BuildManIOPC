from Builder import Package
import os
import sys
import shutil
import subprocess

class Rule(Package) :
  def env(self):
    return False

  def extract(self):
    info = self.info
    pkgsrcs = info.getSources()
    pkgrepo = info.getRepository()
    pkgtmp = info.getTemporaryDir()
    version = "linux-6.1.19"
    split_files = "{}.tar.xz.part-*".format(version)
    merged_file = "{}/{}.tar.xz".format(pkgtmp, version)

    cmd, workdir = ["cat", split_files, ">", merged_file], pkgsrcs
    print(cmd, workdir)
    subprocess.run(cmd, cwd=workdir)

    cmd, workdir = ["tar", "Jxvf", merged_file], pkgtmp
    subprocess.run(cmd, cwd=workdir)

    cmd, workdir = ["ln", "-s", version, "linux"], pkgtmp
    subprocess.run(cmd, cwd=workdir)

    return True

  def patch(self):
    return True

  def configure(self):
    return True

  def build(self):
    try:
      info = self.info
      pkgtmp = info.getTemporaryDir("linux")
      build=subprocess.run(["make", "ARCH=$ARCH", "-j5", "V=1"], cwd=pkgsrc)
      build.check_returncode()
    except:
      sys.exit(1)
    return True

  def install(self):
    PKG=CFG['PACKAGES'][pkg_name]
    pkgdst=PKG['package.dir.pkg.dst']
    workdir=PKG['package.dir.pkg.dst.build']
    linux_image = PKG['package.dir.pkg.dst.buildimage']
    pkginstall = PKG['package.dir.pkg.install']
    build=subprocess.run(["cp", linux_image, pkginstall], cwd=pkgsrc)
    return True

  def install(self):

    return True

  def sdk(self):
    return True

  def clean(self):
    return False
