#****************************************************************************
#* update.py
#****************************************************************************


import urllib
import os
import shutil
from . import read_packages
from. import tempdir_m

def update(args):
    print("Update EDAPack Packages")
    
    # Update the index files as long as the user didn't 
    # force skipping of this
    if args.no_update_indexes == False:
        update_indexes()

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

#********************************************************************            
#* Ensure we are working with up-to-date index information
#********************************************************************            
def update_indexes():
    tmp = tempdir_m.mktempdir()
    print("Updating EDAPack Indexes")
    edapack = read_packages.edapack_dir()
    
    srcs = read_packages.read_sources()
    
    for src in srcs:
        print("  Fetching " + src.source + ".index from " + src.url)
        urllib.request.urlretrieve(
            src.url,
            os.path.join(tmp, src.source + ".index"))
        
    for src in srcs:
        shutil.copy(
            os.path.join(tmp, src.source + ".index"),
            os.path.join(edapack, "etc", src.source + ".index")
            )
        
    print("Done updating indexes")

    