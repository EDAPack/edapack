#****************************************************************************
#* update.py
#****************************************************************************

from . import read_packages

def update(args):
    print("Update EDAPack Packages")
    edapack = read_packages.edapack_dir()
    
    packages = read_packages.read_packages()
   
    update_packages = [] 
    if len(args.packages) == 0:
        print("TODO: no packages specified. update all packages")
        for pkg in packages.keys():
            print("Processing pkg " + pkg + " edapack=" + edapack)
            update_packages.append(pkg)
    else:
        update_packages.append(args.packages)
        

        
    for pkg in update_packages:
        print("Update package: " + pkg)
        if (pkg in packages.keys()) == False:
            print("Error: package \"" + pkg + "\" is not a recognized package")
            exit(1)