#****************************************************************************
#* edapack.sh
#*
#* Setup script for bourne shell
#****************************************************************************

etc_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd)"
edapack_dir=$(dirname $etc_dir)

# Add the bin directory to the PATH
if [[ ! ":$PATH:" =~ ":${edapack_dir}/bin:" ]]; then
  export PATH=${edapack_dir}/bin:$PATH
fi

# Add our modules directory to the MODULESPATH
modulepath=${MODULEPATH:-}
if [[ ! ":$modulepath:" =~ ":${edapack_dir}/modulefiles:" ]]; then
  MODULEPATH=${edapack_dir}/modulefiles${modulepath:+:}$modulepath
  export MODULEPATH
fi

# Bring in modules commands
source ${edapack_dir}/modules/init/bash


