#****************************************************************************
#* plugins_m.py
#****************************************************************************
import os
import importlib.util
from . import read_packages

def get_plugin_path(extra_plugins=None):
    edapack = read_packages.edapack_dir();
    plugin_path = [os.path.join(edapack, "lib", "plugins")]
    
    # Build up the plug-in path first
    if extra_plugins != None:
        for path in extra_plugins:
            plugin_path.append(path)
            
    if "EDAPACK_PLUGIN_PATH" in os.environ.keys():
        path = os.environ["EDAPACK_PLUGIN_PATH"]
        for elem in path.split(":"):
            elem = elem.strip()
            
            if elem != "":
                if os.path.isdir(elem):
                    plugin_path.append(elem)
                else:
                    print("Warning: ignoring non-existent plug-in path dir \"" + elem + "\"")
   
    return plugin_path

#********************************************************************
#* load_plugin()
#********************************************************************
def load_plugin(plugin):
    spec = importlib.util.spec_from_file_location(
        os.path.basename(plugin), 
        plugin)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)
   
    return plugin_module

#********************************************************************
#* list_plugins()
#* Entry-point for the list-plugins command
#********************************************************************
def list_plugins(args):
    
    plugin_path = get_plugin_path(args.p)

    link_plugins = {}

    for pd in plugin_path:
        for file in os.listdir(pd):
            if file.startswith("edapack_") and file.endswith(".py"):
                if file.startswith("edapack_link_"):
                    id = file[len("edapack_link_"):len(file)-3]
                    link_plugins[id] = os.path.join(pd, file)
                else:
                    # Ignore plug-ins that we don't recognize
                    print("Warning: unknown plug-in type for file \"" + file + "\"")
                    
   
    # Link plug-ins first
    print("Link Plug-ins:")
    for id in sorted(link_plugins.keys()):
        plugin = load_plugin(link_plugins[id])
        try:
            desc = plugin.get_short_description()
        except Exception as e:
            desc = "(Error: exception thrown)"
            
        print("    " + id + ": " + desc)
