
ifneq (1,$(RULES))

EDAPACK_TARGETS += $(BUILD_DIR)/fusesoc.d

else # Rules

$(BUILD_DIR)/fusesoc.d : $(BUILD_DIR)/edapack_init.d
	$(Q)$(BUILD_DIR)/edapack/bin/pip3 install fusesoc
	$(Q)touch $@

endif

