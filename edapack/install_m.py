#****************************************************************************
#* install_m.py
#*
#* Implements the install command for EDAPack
#****************************************************************************

from github import Github
from subprocess import call
import os
import sys
import platform
import urllib
import tarfile
from . import read_packages
from . import tempdir_m


#********************************************************************        
#* install
#********************************************************************        
def install(args):
    packages = read_packages.read_packages()
    
    # First, validate that all packages exist
    for pkg in args.packages:
        if (pkg in packages.keys()) == False and os.path.exists(pkg) == False and pkg.startswith("http://") == False and pkg.startswith("https://") == False:
            print("Error: package \"" + pkg + "\" does not exist");
            exit(1)
            
    # Okay, now we believe that we know how to deal with all packages
    for pkg in args.packages:
        if pkg in packages.keys():
            print("Note: installing package \"" + pkg + "\"")
            install_index_pkg(packages[pkg])
     
    edapack_script_dir = os.path.dirname(os.path.abspath(__file__))
#    print("edapack_script_dir=" + edapack_script_dir)
  
    # First, validate that all packages make sense 
#    for pkg in args.packages:
#        print("package=" + pkg);
    
#********************************************************************        
#* install_index_pkg
#********************************************************************        
def install_index_pkg(pkg_src):
    tempdir = tempdir_m.mktempdir()
   
    without_protocol = pkg_src.url[pkg_src.url.find("://")+3:]
    path = without_protocol.split('/')
    archive = None
    if path[0] == "github.com":
        # Okay, we know how to work with this
        archive = fetch_github(path[1], path[2], pkg_src.id, tempdir)
    else:
        print("Error: unsupported host (" + path[0] + ") in URL " + pkg_src.url)
        exit(1)

    install_tar_gz(archive, True)
        

def fetch_github(org_user, repo, id, tempdir):
    # TODO: need to probe platform
    pkg_platform_prefix = id + "-" + "linux" + "_" + "x86_64";
    pkg_any_prefix = id + "-" + "any";
    g = Github()
    
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

    assets = latest.get_assets()
    pkg_asset = None
    for asset in assets:
#        print("asset.name=" + asset.name + " pkg_prefix=" + pkg_platform_prefix)
        if (asset.name.startswith(pkg_platform_prefix) or asset.name.startswith(pkg_any_prefix)) and asset.name.endswith(".tar.gz"):
            pkg_asset = asset
            break
        
    if pkg_asset == None:
        print("Error: failed to find a package to download for " + org_user + "/" + repo)
        exit(1)
        
    print("Note: downloading package from " + pkg_asset.browser_download_url)

    package_path = os.path.join(tempdir, os.path.basename(pkg_asset.name))
    response = urllib.request.urlretrieve(
        pkg_asset.browser_download_url, 
        package_path)

    print("Done... ")
    return package_path
    

def install_tar_gz(archive, in_tempdir):
    if in_tempdir == True:
        tempdir = os.path.dirname(archive)
    else:
        tempdir = tempdir_m.mktempdir()
        
    # Extract etc/install.py and etc/package.info
    tf = tarfile.open(archive, "r:gz")
    tf.extract("etc/package.info", tempdir) 
    tf.extract("etc/install.py", tempdir) 
   
    # Run the installer
    print("Note: running package installer")
    call([sys.executable, 
              os.path.join(tempdir, "etc/install.py"),
              "install",
              read_packages.edapack_dir(),
              "--archive", archive])
    print("Done!")


