edapack
=======

The EDAPack provides a simple way to install and manage EDA tools, along with a packaged collection of open source EDA tools. This project (edapack) provides the base software needed to install and manage other tool installations.


# Installing
Install the EDAPack base tools by downloading the latest release from GitHub. Extract the .tar.gz file.

# Environment Setup
Source <edapack>/etc/edapack.sh to configure the environment. This adds the 'edapack' command to your path, and configures Environment Modules.

# Installing Tools
Run 'edapack avail' to list the packages that are available to install.
Run 'edapack install <pkg>' will download and install one of the packages shown by 'edapack avail'
   
# Enable Tools
Configuring tools in the environment is done via the 'module' command. 'module avail' lists tools and tool versions that can be added to the environment. 'module load <tool/version>' enables a specific tool. The most-recent installed tool version can always be enabled by loading <tool>/latest. To load the latest version of Verilator, for example, 'module load verilator/latest'.
   
   
