# Makefile



# defaults

SIM ?= icarus
SDF_FILE ?=

include ${MAKEFILE_INC_HOME}/makefile_vcs.inc


TOPLEVEL_LANG ?= verilog

# Add SDF file if specified
ifdef SDF_FILE
  EXTRA_FLAGS += +sdf_annotate_file=${SDF_FILE}
endif


VERILOG_SOURCES += and2_top_formal_verification.v
VERILOG_SOURCES += ${NETLIST_TYPE}/fabric_netlists.v

# Add SDF file if specified
ifdef SDF_FILE
  EXTRA_FLAGS += +sdf_annotate_file=${SDF_FILE}
endif

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file

TOPLEVEL = and2_top_formal_verification


# MODULE is the basename of the Python test file

MODULE = test_and2



# include cocotb's make rules to take care of the simulator setup

include $(shell cocotb-config --makefiles)/Makefile.sim



