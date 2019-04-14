#****************************************************************************
#* link_m.py
#****************************************************************************
import os
import importlib.util
from . import read_packages
from . import plugins_m

#********************************************************************
#* link()
#* Entry-point for the link command
#********************************************************************
def link(args):
    
    edapack = read_packages.edapack_dir();
    plugin_path = plugins_m.get_plugin_path(args.p)
   
    # Validate that the tool location exists
    if os.path.isdir(args.tool_path) == False:
        print("Error: tool-installation path \"" + args.tool_path + "\" does not exist")
        exit(1)
        
    # Try to find the link plug-in on the plug-in path
    link_plugin = ""
    for pd in plugin_path:
        for file in os.listdir(pd):
            if file.startswith("edapack_link_") and file.endswith(".py"):
                if file == "edapack_link_" + args.tool + ".py":
                    link_plugin = os.path.join(pd, file)
                    break
        if link_plugin != "":
            break

    if link_plugin == "":
        print("Error: no link plug-in found for tool \"" + args.tool + "\"")
        print("  Try running edapack list-plugins to see available plug-ins")
        raise("Failed to find link plug-in")


    # Okay, load the plug-in and see what we can do
    spec = importlib.util.spec_from_file_location(os.path.basename(link_plugin), link_plugin)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)

    print("Note: validating installation directory...");
    try:
        plugin_module.validate_tool_install(args.tool_path)    
    except Exception as e:
        print("Error: installation path is invalid (" + str(e) + ")")
        exit(1)
        
    # Now, see if we can get a version
    if args.version != None:
        version = args.version
    else:
        try:
            version = plugin_module.get_tool_version(args.tool_path)
        except:
            print("Error: no -version specified, and \"" + args.tool + "\" version cannot be queried from install")
            exit(1)
            
    # Okay, now we have
    # - link plug-in
    # - tool install path
    # - tool version
    #
    # Next, we need to create the modulefile and add it to the EDAPack tree
    modulefile = plugin_module.get_modulefile(args.tool_path, version)
   
    # Create the modulefiles dir if it doesn't exist
    if os.path.isdir(os.path.join(edapack, "modulefiles", args.tool)) == False:
        os.makedirs(os.path.join(edapack, "modulefiles", args.tool))
        
    # First, determine whether we should update the 'latest' modulefile version
    is_latest = True
    for exist_ver in os.listdir(os.path.join(edapack, "modulefiles", args.tool)):
        if exist_ver != "latest":
            if read_packages.compare_versions(version, exist_ver) == False:
                is_latest = False
                break
            
    # Now, create a version-specific modulefile
    print("Note: creating modulefile...")
    fp = open(os.path.join(edapack, "modulefiles", args.tool, version), "w")
    fp.write(modulefile)
    fp.close()
    
    # See if we also need to update the 'latest'
    if is_latest == True:
        print("Note: updating 'latest' link...")
        fp = open(os.path.join(edapack, "modulefiles", args.tool, "latest"), "w")
        fp.write(modulefile)
        fp.close()
        
    print("Note: done!")
   
