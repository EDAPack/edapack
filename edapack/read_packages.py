#****************************************************************************
#* read_packages.py
#****************************************************************************

import os;
import configparser

class package_src:
    def __init__(self, source, id, description, url):
        self.source = source
        self.id = id
        self.description = description
        self.url = url

#********************************************************************        
#* edapack_dir
#********************************************************************        
def edapack_dir():
    edapack_pkg_dir = os.path.dirname(os.path.abspath(__file__))
    edapack_lib_dir = os.path.dirname(edapack_pkg_dir)
   
    print("edapack_lib_dir=" + edapack_lib_dir) 
    if os.path.basename(edapack_lib_dir) == "edapack.zip":
        edapack_lib_dir = os.path.dirname(edapack_lib_dir)
        
        
        
    edapack = os.path.dirname(edapack_lib_dir)
    
    return edapack

def read_index(path, source, packages):
    index = configparser.ConfigParser()
    index.read(path)
    
    for pkg in index.sections():
        packages[pkg] = package_src(
            source, pkg, 
            index[pkg]["description"], 
            index[pkg]["url"])
        
def read_packages():
    packages = {}
    edapack = edapack_dir()
    sources = configparser.ConfigParser()
    if os.path.exists(os.path.join(edapack, "etc", "sources")) == False:
        print("Error: etc/sources doesn't exist")
        exit(1)

    sources.read(os.path.join(edapack, "etc", "sources"))
    
    for source in sources.sections():
        
        index_path = os.path.join(edapack, "etc", source + ".index")
        
        if os.path.exists(index_path) == True:
            read_index(index_path, source, packages)
        else:
            print("Error: index file \"" + index_path + "\" does not exist")
            exit(1)

    return packages

def compare_versions(v1, v2):    
    v1_list = v1.split(".")
    v2_list = v2.split(".")

    # Ensure the versions are the same length
    while len(v1_list) < len(v2_list):
        v1_list.append("0")
    while len(v2_list) < len(v1_list):
        v2_list.append("0")

    # Convert each version to an integer that can be compared
    v1_val = 0
    v2_val = 0
    for i in range(len(v1_list)):
        v1_val *= 10
        v1_val += int(v1_list[i])
    for i in range(len(v2_list)):
        v2_val *= 10
        v2_val += int(v2_list[i])
        
    is_ge = v1_val >= v2_val
#    print("Compare: " + v1 + " " + v2 + ": " + str(is_ge))
    if v1_val > v2_val:
        return 1
    elif v1_val < v2_val:
        return -1
    else:
        return 0
