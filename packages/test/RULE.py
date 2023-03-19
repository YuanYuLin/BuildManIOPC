from Builder import Package

class Rule(Package) :
  def env(self):
    return False

  def extract(self):
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
