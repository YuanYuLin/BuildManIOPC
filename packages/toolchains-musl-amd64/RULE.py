from Builder import Package
import os
import sys
import subprocess

class Rule(Package) :
  def env(self):
    info = self.info
    builder = self.builder
    builder.checkDependency('arch-amd64')
    os.environ['PATH']='{}:{}'.format(os.environ['PATH'], info.getTemporaryDir('toolchains/bin'))
    os.environ['CROSS_COMPILE']='x86_64-linux-'

    return False

  def extract(self):
    info = self.info
    pkgsrcs = info.getSources()
    pkgrepo = info.getRepository()
    pkgtmp = info.getTemporaryDir()
    version = "x86-64--musl--stable-2022.08-1"
    tarball = "{}/{}.tar.bz2".format(pkgsrcs, version)

    cmd, workdir = ["tar", "jxvf", tarball, "-C", pkgtmp], pkgtmp
    subprocess.run(cmd, cwd=workdir)

    cmd, workdir = ["ln", "-s", version, "toolchains"], pkgtmp
    subprocess.run(cmd, cwd=workdir)

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
