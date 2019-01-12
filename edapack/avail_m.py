#****************************************************************************
#* avail_m.py
#*
#* Implements the EDAPack 'avail' command to list available packages
#****************************************************************************
from . import read_packages

#********************************************************************        
#* avail
#********************************************************************        
def avail(args):
    print("Available EDAPack packages")
    packages = read_packages.read_packages()
   
    max_len = 0
    for pkg in packages.keys():
        if len(pkg) > max_len:
            max_len = len(pkg)

    fmt_string = "%-" + str(max_len) + "s - %s"            
    for pkg in sorted(packages.keys()):
        print(fmt_string % (pkg, packages[pkg].description))
