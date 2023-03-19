from Builder import Package
import os
import sys
import subprocess

class Rule(Package) :
  def env(self):
    info = self.info
    builder = self.builder
    builder.checkDependency('arch-amd64')
    print(info.getTemporary())
    os.environ['PATH']='{}:{}'.format(os.environ['PATH'], info.getTemporary('toolchains/bin'))
    os.environ['CROSS_COMPILE']='x86_64-linux-'

    return False

  def extract(self):
    PKG=CFG['PACKAGES'][pkg_name]
    pkgsrc=PKG['package.dir.pkg.src']
    pkgdst=PKG['package.dir.pkg.dst']
    subprocess.run(["./extract.sh", pkgdst], cwd=pkgsrc)

    return True

  def patch(self):
    return True

  def configure(self):
    return True

  def build(self):
    return True

  def install(self):
    return True

  def sdk(self):
    return True

  def clean(self):
    return False
