
SCRIPTS_DIR:=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
EDAPACK_DIR:=$(abspath $(SCRIPTS_DIR)/..)
MKFILES_DIR:=$(SCRIPTS_DIR)/mkfiles
PACKAGES_DIR:=$(EDAPACK_DIR)/packages
BUILD_DIR:=$(EDAPACK_DIR)/build

include $(EDAPACK_DIR)/etc/edapack.info

MK_INCLUDES += $(wildcard $(MKFILES_DIR)/*.mk)
EDAPACK_TARGETS += $(BUILD_DIR)/edapack_init.d

PYTHON_PACKAGES += argparse textwrap fusesoc
EDAPACK_PACKAGES += iverilog verilator gtkwave

ifeq (true,$(VERBOSE))
Q=
WGET=wget
UNTARXZ=tar xvJf
else
Q=@
WGET=wget -q
UNTARXZ=tar xJf
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

include $(MK_INCLUDES)

RULES := 1

all : $(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz
	$(Q)echo "EDAPack"

$(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz : $(BUILD_DIR)/python.d
	$(Q)rm -rf $(BUILD_DIR)/edapack-$(platform)-$(version)
	$(Q)$(BUILD_DIR)/python/inst/bin/virtualenv \
		$(BUILD_DIR)/edapack-$(platform)-$(version)
	$(Q)rm -rf $(BUILD_DIR)/edapack-$(platform)-$(version)/lib/python$(PYTHON_VERSION_MAJOR)
	$(Q)rm -rf $(BUILD_DIR)/edapack-$(platform)-$(version)/lib/python$(PYTHON_VERSION_MAJOR)/config-*
	$(Q)cp -r $(BUILD_DIR)/python/inst/lib/python$(PYTHON_VERSION_MAJOR) $(BUILD_DIR)/edapack-$(platform)-$(version)/lib
	$(Q)rm -f $(BUILD_DIR)/edapack-$(platform)-$(version)/include/python$(PYTHON_VERSION_MAJOR)m
	$(Q)cp -r $(BUILD_DIR)/python/inst/include/python$(PYTHON_VERSION_MAJOR)m $(BUILD_DIR)/edapack-$(platform)-$(version)/include
	$(Q)for pkg in $(PYTHON_PACKAGES); do \
		echo "Note: installing Python package $$pkg"; \
		$(BUILD_DIR)/edapack-$(platform)-$(version)/bin/pip3 \
			install $${pkg}; \
	done
	$(Q)for pkg in $(EDAPACK_PACKAGES); do \
		cd $(BUILD_DIR)/edapack-$(platform)-$(version) ; \
		tar xvzf /project/fun/edapack/edapack-$${pkg}/build/*.tar.gz \
			--strip-components=1; \
	done
	$(Q)$(BUILD_DIR)/python/inst/bin/virtualenv \
		--relocatable $(BUILD_DIR)/edapack-$(platform)-$(version)
	$(Q)cd $(BUILD_DIR) ; \
		tar czf $(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz \
			edapack-$(platform)-$(version)

release : $(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz
	$(Q)$(EDAPACK_DIR)/scripts/upload.py \
		--org EDAPack --repo edapack \
		--key $(GITHUB_API_TOKEN) --version $(version) \
		$(BUILD_DIR)/edapack-$(platform)-$(version).tar.gz

clean : 
	$(Q)rm -rf $(BUILD_DIR)

include $(MK_INCLUDES)


