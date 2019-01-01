edapack
=======

Provides a packaged collection of open source EDA tools

* - GTKWave
- SystemC
- UVM-SC
* - Verilator
x - Icarus Verilog
- VTE (Python package?)
-- DVTE
- Simscripts (Python package?)
- DVKit

- DTC

- Target compilers (RISC-V)

- ChiselScript binaries (Python package? Has a Java dependency)
-> May just be an EDAPack package, since it both requires
   Java and non-python binaries

Built on a Python3 installation that includes:
- Binary build of PyYAML
- Jinja2
- PyGit
- ELF Utilities
- PyGTK, PyQT
- Necessary platform libraries
- ?

EDAPack Base -- core tools and a setup script
-- Need to see if we can post a release at the Organization level
EDAPack      -- scripts

Packages can have dependencies on a specific EDAPack Base version
- Must detect that we're running there, since technically EDAPack can
  install into any Python directory
Packages can depend on other EDAPack packages

