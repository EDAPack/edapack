
ifneq (1,$(RULES))
PYTHON_VERSION_MAJOR=3.6
PYTHON_VERSION=$(PYTHON_VERSION_MAJOR).8
PYTHON_DIR=Python-$(PYTHON_VERSION)
PYTHON_TXZ=$(PYTHON_DIR).tar.xz
PYTHON_URL=https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_TXZ)

EDAPACK_TARGETS += $(BUILD_DIR)/python.d

else # Rules

$(BUILD_DIR)/python.d : $(PACKAGES_DIR)/$(PYTHON_TXZ)
	$(Q)rm -rf $(BUILD_DIR)/python
	$(Q)mkdir -p $(BUILD_DIR)/python
	$(Q)cd $(BUILD_DIR)/python ; $(UNTARXZ) $^
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR) ; \
		./configure --prefix=$(BUILD_DIR)/python/inst
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR); $(MAKE)
	$(Q)cd $(BUILD_DIR)/python/$(PYTHON_DIR); $(MAKE) install
	$(Q)$(BUILD_DIR)/python/inst/bin/python3 -m pip install virtualenv
	$(Q)touch $@

$(PACKAGES_DIR)/$(PYTHON_TXZ) :
	$(Q)if test ! -d $(PACKAGES_DIR); then mkdir -p $(PACKAGES_DIR); fi
	$(Q)$(WGET) -O $@ $(PYTHON_URL)
endif

