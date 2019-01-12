#****************************************************************************
#* update_scripts_m.py
#*
#* Update the 
#****************************************************************************
from . import read_packages
from github import Github


#********************************************************************
#* Bring in the script version
#********************************************************************
try:
    from . import version
    version = version.version
except Exception as e:
    version = "unknown"
    
def update_scripts(args):
    edapack_dir = read_packages.edapack_dir()
    print("Checking for scripts update...")
    print("  Current script version is: " + version)

    g = Github()
    
    org = g.get_organization("EDAPack")
    repo = org.get_repo("edapack")
    
    latest_release = repo.get_latest_release()
    
    print("  Latest script version is: " + latest_release.title)
    
    if read_packages.compare_versions(latest_release.title, version) > 0:
        print("TODO: update")
    else:
        print("  Scripts are up-to-date")

    
