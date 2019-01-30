#****************************************************************************
#* update_scripts_m.py
#*
#* Update the 
#****************************************************************************
from . import read_packages
from . import tempdir_m
from github import Github
import os
import urllib
import tarfile
import shutil


#********************************************************************
#* Bring in the script version
#********************************************************************
try:
    from . import version
    version = version.version
except Exception as e:
    version = "unknown"
    
def update_scripts(args):
    print("Checking for scripts update...")
    print("  Current script version is: " + version)

    g = Github()
    
    org = g.get_organization("EDAPack")
    repo = org.get_repo("edapack")
    
    latest_release = repo.get_latest_release()
    
    print("  Latest script version is: " + latest_release.title)
    
    if read_packages.compare_versions(latest_release.title, version) > 0:
        print("  Installing new script version")
        download_install(latest_release)
        print("  Done installing latest scripts")
    else:
        print("  Scripts are up-to-date")
        if args.force:
            print("  --force specified. Re-installing anyway")
            download_install(latest_release)

def download_install(latest_release):
    edapack_dir = read_packages.edapack_dir()
    tempdir = tempdir_m.mktempdir()
  
    pkg_asset = None 
    for asset in latest_release.get_assets():
        if asset.name.startswith("edapack-scripts-update") and asset.name.endswith(".tar.gz"):
            pkg_asset = asset
            break

    if pkg_asset == None:
        print("Error: failed to find edapack-scripts-update package");
        exit(1)
        
    package_path = os.path.join(tempdir, os.path.basename(pkg_asset.name))

    response = urllib.request.urlretrieve(
        pkg_asset.browser_download_url,
        package_path)

    # Now, delete the existing ${EDAPACK}/lib/edapack directory and
    # unpack the new one
    shutil.rmtree(
        os.path.join(edapack_dir, 'lib', 'edapack')
        )
    
    tf = tarfile.open(package_path, "r:gz")
    tf.extractall(os.path.join(edapack_dir, "lib"))
    os.makedirs(os.path.join(edapack_dir, "lib2"))
    tf.extractall(os.path.join(edapack_dir, "lib2"))
    
