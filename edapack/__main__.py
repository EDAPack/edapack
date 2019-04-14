#****************************************************************************
#* edapack __main__.py
#*
#* Main entry point for the 'edapack' command
#*
#****************************************************************************
import argparse
import configparser
import os

# Bring in local modules
from . import install_m
from . import avail_m
from . import update_m
from . import tempdir_m
from . import update_scripts_m
from . import link_m
from . import plugins_m

#********************************************************************
#* Bring in the script version
#********************************************************************
try:
    from . import version
    version = version.version
except Exception as e:
    version = "unknown"

# Installation steps
# - Fetch package to a temporary location
# - Determine the package version
# - Determine whether the version is already installed
#   - Abort unless --force
#   - Remove old package if --force
# - Unpack into install_m location
# - 

def main():
    main_arguments = argparse.ArgumentParser()
    
    main_arguments.add_argument("-p", action="append",
        help="Append to plug-in path")
    
    subparsers = main_arguments.add_subparsers(
        help="EDAPack sub-commands",
        dest="subparser_name")
    avail_cmd = subparsers.add_parser("avail", help="checks for available packages")
    avail_cmd.add_argument("--no-update-indexes",
        action="store_true",
        default=False,
        help="Disable updating of package-index files")
    
    install_cmd = subparsers.add_parser("install", help="installs one or more packages")
    install_cmd.add_argument("--no-update-indexes",
        action="store_true",
        default=False,
        help="Disable updating of package-index files")
    
    install_cmd.add_argument("packages", nargs="+", 
        help="package identifiers of packages to install")
#        help="Package identifier, archive path, or URL")

    link_cmd = subparsers.add_parser("link", help="links external tools into an EDAPack installation")
#    link_cmd.add_argument("-create-link", action="store_true",
#                          help="Creates a link to the tool installation inside the EDAPack tree")
    link_cmd.add_argument("-version", help="specifies the tool version if it cannot be determined")
    link_cmd.add_argument("tool", help="specifies the name of the tool to link")
    link_cmd.add_argument("tool_path", help="specifies the installation location for the tool")
    
    list_plugins_cmd = subparsers.add_parser("list-plugins",
        help="Lists available plug-ins")
    list_plugins_cmd.add_argument("-p", action="append",
        help="Specifies entries to the plug-in path")
    
    update_cmd = subparsers.add_parser("update", help="updates all packages, or a select set")
    update_cmd.add_argument("packages", nargs="*", help="specifies the packages to update")
    update_cmd.add_argument("-y", 
        action="store_true",
        help="Forces installation without confirmation")
#    update_cmd.add_argument("--check-only", help="Only checks for newer packages")
#    update_cmd.add_argument("--no-update-indexes",
#        action="store_true",
#        help="Disable updating of package-index files")
    
    update_scripts_cmd = subparsers.add_parser("update-scripts",
        help="updates the EDAPack core scripts")
    update_scripts_cmd.add_argument("--force",
        action="store_true",
        help="force updating scripts")
    
#    check_update_cmd = subparsers.add_parser("check-update", help="Checks for available package updates")
    
    args = main_arguments.parse_args()
    
    if args.subparser_name == "avail":
        avail_m.avail(args)
    elif args.subparser_name == "install":
        install_m.install(args)
    elif args.subparser_name == "link":
        link_m.link(args)
    elif args.subparser_name == "list-plugins":
        plugins_m.list_plugins(args)
    elif args.subparser_name == "update":
        update_m.update(args)
    elif args.subparser_name == "update-scripts":
        update_scripts_m.update_scripts(args)
    else:
        main_arguments.print_help()
        exit(1)


if __name__ == "__main__":
  main()
  
  

