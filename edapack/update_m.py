#****************************************************************************
#* update.py
#****************************************************************************


import urllib
import os
import shutil
from . import read_packages
from. import tempdir_m
from . import install_m
from github import Github

def update(args):
    print("Update EDAPack Packages")
    
    # Update the index files as long as the user didn't 
    # force skipping of this
#    if args.no_update_indexes == False:
    update_indexes()

    edapack = read_packages.edapack_dir()
    
    packages = read_packages.read_packages()
   
    update_packages_l = [] 
    if len(args.packages) == 0:
        for pkg in packages.keys():
            if os.path.isdir(os.path.join(edapack, pkg)):
                update_packages_l.append(pkg)
    else:
        for pkg in args.packages:
            update_packages_l.append(pkg)
        
    update_packages(edapack, packages, update_packages_l, args.y)
        

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

#********************************************************************            
#* is_version_gt
#*
#* Compares two versions and returns (v1>v2)
#********************************************************************            
def is_version_gt(v1, v2):    
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    
    if v1_list[0] == "":
        v1_list.clear()
    if v2_list[0] == "":
        v2_list.clear()

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
        
    is_ge = v1_val > v2_val

    return is_ge

#********************************************************************            
#* update_packages()
#********************************************************************            
def update_packages(edapack, packages, update_packages_l, force):
    if os.getenv("GITHUB_API_TOKEN") is not None:
        g = Github(os.environ['GITHUB_API_TOKEN'])
    else:
        g = Github()
    packages_with_update = []
    
    for pkg in update_packages_l:
        if packages.get(pkg) == None:
            print("Error: package \"" + pkg + "\" is not a recognized package")
            exit(1)
   
        pkg_src = packages[pkg]
        without_protocol = pkg_src.url[pkg_src.url.find("://")+3:]
        path = without_protocol.split('/')

        latest_remote_version = "0.0.0"
        latest_local_version = local_get_latest_version(edapack, pkg)
        if path[0] == "github.com":
            #
            latest_remote_version = github_get_latest_version(g, path[1], path[2], pkg_src.id)
        else:
            print("Error: unsupported host (" + path[0] + ") in URL " + pkg_src.url)
            exit(1)
        
        print("Checking package " + pkg + ": local version=" + latest_local_version + 
              " remote version=" + latest_remote_version)
        
        if is_version_gt(latest_remote_version, latest_local_version):
            packages_with_update.append(pkg)
     
    if len(packages_with_update) == 0:
        print("Note: packages are up-to-date");
        return
  
    if force == True:
        print("Installing " + str(len(packages_with_update)) + " packages with updates.")
    else:
        yn = input("" + str(len(packages_with_update)) + " packages have updates. Install (Y/n)?")
        
        if yn != "" and yn != "y" and yn != "Y" and yn != "yes":
            print("Cancelling...")
            return

    print("Installing updates...")
    for pkg in packages_with_update:
        install_m.install_index_pkg(packages[pkg])
        
    print("Note: finished updating " + str(len(packages_with_update)) + " packages")
       
def local_get_latest_version(edapack, pkg_id): 
    if os.path.isdir(os.path.join(edapack, pkg_id)) == False:
        print("Error: package " + pkg_id + " is not installed");
        exit(1)
        
    version = ""
    
    for v in os.listdir(os.path.join(edapack, pkg_id)):
        if is_version_gt(v, version):
            version = v
        
    return version
        
def github_get_latest_version(g, org_user, repo, pkg_id):
   
    org = g.get_organization(org_user);
    
    if org != None:
        r = org.get_repo(repo) 
    else:
        user = g.get_user(org_user)
        if user == None:
            print("Error: specified organization or user (" + org_user + ") is invalid");
            exit(1)
        else:
            r = user.get_repo(repo)

    if r == None:
        print("Error: Failed to obtain repository " + repo + " for org/user " + org_user)
        exit(1)

    latest = r.get_latest_release()
    
    if latest == None:
        print("Error: there doesn't appear to be a release on GitHub for " + org_user + "/" + repo)
        exit(1)

    return latest.title
