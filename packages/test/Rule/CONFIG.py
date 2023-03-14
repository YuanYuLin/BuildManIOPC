def env(pkg_name, CFG):
    print(pkg_name, "env")
    print(CFG)
    return False

def extract(pkg_name, CFG):
    print(pkg_name, "extract")
    return True

def patch(pkg_name, CFG):
    print(pkg_name, "patch")
    return True

def configure(pkg_name, CFG):
    print(pkg_name, "configure")
    return True

def build(pkg_name, CFG):
    print(pkg_name, "build")
    return True

def install(pkg_name, CFG):
    print(pkg_name, "install")
    return True

def sdk(pkg_name, CFG):
    print(pkg_name, "sdk")
    return True

def clean(pkg_name, CFG):
    print(pkg_name, "clean")
