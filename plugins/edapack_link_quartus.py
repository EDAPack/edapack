#****************************************************************************
#* edapack_link_template.py
#*
#* Template for an extension script to link a tool into EDAPack
#****************************************************************************
from string import Template
import os

#********************************************************************
#* get_short_description
#*
#* Returns a sort description of this plug-in's functionality
#********************************************************************
def get_short_description():
    return "Links a Quartus installation into an EDAPack tree"

#********************************************************************
#* validate_tool_install
#*
#* Validates that the user-specified path is valid. 
#* Throw an exception with an error message if the installation 
#* is not valid
#********************************************************************
def validate_tool_install(tool_path):
    if os.path.isdir(os.path.join(tool_path, "quartus")) == False:
        raise Exception("missing 'quartus' subdirectory")

#********************************************************************
#* get_tool_version
#*
#* Queries the tool version based on the installation. 
#* Throw an exception if this operation is not supported
#********************************************************************
def get_tool_version(tool_path):
  raise("Querying the version is not supported")

#********************************************************************
#* get_modulefile
#*
#* Returns the modulefile for this tool install and version. The
#* modulefile will be added to the EDAPack tree
#********************************************************************
def get_modulefile(tool_path, tool_version):
  modulefile = """
    prepend-path PATH [file join ${tool_path} quartus bin]
    setenv QUARTUS [file join ${tool_path} quartus]
  
    # Configure Modelsim if it is installed
    if [file isdirectory [file join ${tool_path} modelsim_ase]] {
      prepend-path PATH [file join ${tool_path} modelsim_ase bin]
    }
  """

  template_vars = {
    "tool_path": tool_path,
    "tool_version": tool_version
  }

  template = Template(modulefile)

  return template.safe_substitute(template_vars)

