# Makefile for testing

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += test_module.v

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = test_module

# MODULE is the basename of the Python test file
MODULE = test_module

# Add SDF file if specified
ifdef SDF_FILE
  EXTRA_FLAGS += +sdf_annotate_file=${SDF_FILE}
endif

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
