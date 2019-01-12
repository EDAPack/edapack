
SCRIPTS_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
EDAPACK_DIR:=$(abspath $(SCRIPTS_DIR)/..)
MKFILES_DIR:=$(SCRIPTS_DIR)/mkfiles
PACKAGES_DIR:=$(EDAPACK_DIR)/packages
BUILD_DIR:=$(EDAPACK_DIR)/build

include $(EDAPACK_DIR)/etc/package.info

MK_INCLUDES += $(wildcard $(MKFILES_DIR)/*.mk)
EDAPACK_TARGETS += $(BUILD_DIR)/edapack_init.d

PYTHON_PACKAGES += argparse textwrap fusesoc
EDAPACK_PACKAGES += iverilog verilator gtkwave

MODULES_VERSION=4.2.1
MODULES_DIR=modules-$(MODULES_VERSION)
MODULES_TGZ=$(MODULES_DIR).tar.gz
MODULES_URL=https://sourceforge.net/projects/modules/files/Modules/$(MODULES_DIR)/$(MODULES_TGZ)/download

TCL_VERSION=8.6.9
TCL_DIR=tcl$(TCL_VERSION)
TCL_TGZ=$(TCL_DIR).tar.gz
TCL_URL=https://sourceforge.net/projects/tcl/files/Tcl/$(TCL_VERSION)/$(TCL_DIR)-src.tar.gz/download

PYTHON_VERSION_MAJOR=3.6
PYTHON_VERSION=$(PYTHON_VERSION_MAJOR).8
PYTHON_DIR=Python-$(PYTHON_VERSION)
PYTHON_TXZ=$(PYTHON_DIR).tar.xz
PYTHON_URL=https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_TXZ)

ifeq (true,$(VERBOSE))
Q=
WGET=wget
UNTARXZ=tar xvJf
UNTARGZ=tar xvzf
else
Q=@
WGET=wget -q
UNTARXZ=tar xJf
UNTARGZ=tar xzf
endif

uname_o:=$(shell uname -o)

ifeq (Linux,$(uname_o))
platform=linux_x86_64
else
ifeq (GNU/Linux,$(uname_o))
platform=linux_x86_64
else
platform=unknown
endif
endif

EDAPACK_PREFIX=$(BUILD_DIR)/edapack-$(platform)-$(version)
TCL_ENV=export PATH=$(EDAPACK_PREFIX)/tcl/bin:$$PATH;

include $(MK_INCLUDES)

RULES := 1

all : $(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz

$(BUILD_DIR)/modules.d : \
		$(BUILD_DIR)/tcl.d \
		$(PACKAGES_DIR)/$(MODULES_TGZ)
	$(Q)rm -rf $(BUILD_DIR)/modules
	$(Q)mkdir -p $(BUILD_DIR)/modules
	$(Q)cd $(BUILD_DIR)/modules ; \
		$(UNTARGZ) $(PACKAGES_DIR)/$(MODULES_TGZ)
	$(Q)cd $(BUILD_DIR)/modules/$(MODULES_DIR) ; \
		patch -p1 < $(SCRIPTS_DIR)/modules.patch
	$(Q)cd $(BUILD_DIR)/modules/$(MODULES_DIR) ; \
		./configure --prefix=$(EDAPACK_PREFIX)/modules \
			--with-tclsh=$(EDAPACK_PREFIX)/tcl/bin/tclsh8.6 \
			--with-tcl=$(EDAPACK_PREFIX)/tcl/lib \
			--with-tcl-ver=8.6 \
			--disable-compat-version
	$(Q)cd $(BUILD_DIR)/modules/$(MODULES_DIR) ; \
		$(MAKE)
	$(Q)cd $(BUILD_DIR)/modules/$(MODULES_DIR) ; \
		$(MAKE) install
	$(Q)rm -f $(EDAPACK_PREFIX)/modules/module-git
	$(Q)touch $@

$(PACKAGES_DIR)/$(MODULES_TGZ) :
	$(Q)mkdir -p $(PACKAGES_DIR)
	$(Q)$(WGET) -O $@ $(MODULES_URL)

$(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz : \
		$(BUILD_DIR)/modules.d \
		$(BUILD_DIR)/tcl.d \
		$(BUILD_DIR)/python3.d \
		$(BUILD_DIR)/scripts.d \
		$(BUILD_DIR)/edapack.zip 
	$(Q)cd $(BUILD_DIR) ; \
		tar czf $(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz \
			edapack-$(platform)-$(version)

release : \
	$(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz \
	$(PACKAGES_DIR)/upload.py
	$(Q)python3 $(PACKAGES_DIR)/upload.py \
		--org EDAPack --repo edapack \
		--key $(GITHUB_API_TOKEN) --version $(version) \
		$(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz

clean : 
	$(Q)rm -rf $(BUILD_DIR)


$(BUILD_DIR)/tcl.d : $(PACKAGES_DIR)/$(TCL_TGZ)
	$(Q)rm -rf $(BUILD_DIR)/tcl
	$(Q)mkdir -p $(BUILD_DIR)/tcl
	$(Q)cd $(BUILD_DIR)/tcl; $(UNTARGZ) $(PACKAGES_DIR)/$(TCL_TGZ)
	$(Q)cd $(BUILD_DIR)/tcl/$(TCL_DIR)/unix; \
		./configure --prefix=$(EDAPACK_PREFIX)/tcl \
			--disable-shared
	$(Q)cd $(BUILD_DIR)/tcl/$(TCL_DIR)/unix; $(MAKE)
	$(Q)cd $(BUILD_DIR)/tcl/$(TCL_DIR)/unix; $(MAKE) install
	$(Q)touch $@

$(PACKAGES_DIR)/$(TCL_TGZ) : 
	$(Q)mkdir -p $(PACKAGES_DIR)
	$(Q)$(WGET) -O $@ $(TCL_URL)

$(BUILD_DIR)/python3.d : $(PACKAGES_DIR)/$(PYTHON_TXZ)
	$(Q)rm -rf $(BUILD_DIR)/python
	$(Q)mkdir -p $(BUILD_DIR)/python
	$(Q)cd $(BUILD_DIR)/python ; $(UNTARXZ) $^
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR) ; \
		./configure --prefix=$(EDAPACK_PREFIX)/python3
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR); $(MAKE)
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR); $(MAKE) install
	$(Q)$(EDAPACK_PREFIX)/python3/bin/pip3 install Jinja2
	$(Q)$(EDAPACK_PREFIX)/python3/bin/pip3 install pyyaml
	$(Q)$(EDAPACK_PREFIX)/python3/bin/pip3 install PyGitHub
	$(Q)touch $@

$(PACKAGES_DIR)/$(PYTHON_TXZ) :
	$(Q)if test ! -d $(PACKAGES_DIR); then mkdir -p $(PACKAGES_DIR); fi
	$(Q)$(WGET) -O $@ $(PYTHON_URL)

$(BUILD_DIR)/scripts.d : \
		$(SCRIPTS_DIR)/edapack \
		$(SCRIPTS_DIR)/edapack.sh \
		$(SCRIPTS_DIR)/edapack.csh \
		$(EDAPACK_DIR)/etc/sources \
		$(EDAPACK_DIR)/etc/edapack.index \
		$(BUILD_DIR)/edapack.zip
	$(Q)mkdir -p $(EDAPACK_PREFIX)/bin
	$(Q)cp $(SCRIPTS_DIR)/edapack $(EDAPACK_PREFIX)/bin/edapack
	$(Q)chmod +x $(EDAPACK_PREFIX)/bin/edapack
	$(Q)mkdir -p $(EDAPACK_PREFIX)/etc
	$(Q)cp $(EDAPACK_DIR)/etc/sources $(EDAPACK_PREFIX)/etc/sources
	$(Q)cp $(EDAPACK_DIR)/etc/edapack.index $(EDAPACK_PREFIX)/etc/edapack.index
	$(Q)cp $(SCRIPTS_DIR)/edapack.sh $(EDAPACK_PREFIX)/etc/edapack.sh
#	$(Q)cp $(SCRIPTS_DIR)/edapack.csh $(EDAPACK_PREFIX)/etc/edapack.csh
	$(Q)touch $@
	
EDAPACK_FILES:=$(shell find $(EDAPACK_DIR)/edapack -type f)
	
$(BUILD_DIR)/edapack.zip : $(EDAPACK_FILES)
	$(Q)mkdir -p $(EDAPACK_PREFIX)/lib
	$(Q)rm -f $(BUILD_DIR)/edapack.zip
	$(Q)cp -r $(EDAPACK_DIR)/edapack $(EDAPACK_PREFIX)/lib
	$(Q)echo "version = '$(version)'" > $(EDAPACK_PREFIX)/lib/edapack/version.py
	$(Q)cd $(EDAPACK_PREFIX)/lib/edapack ; zip -r $@ *

$(PACKAGES_DIR)/upload.py :
	$(Q)mkdir -p $(PACKAGES_DIR)
	$(Q)$(WGET) -O $@ \
          https://github.com/EDAPack/edapack-build/raw/master/scripts/upload.py

include $(MK_INCLUDES)


