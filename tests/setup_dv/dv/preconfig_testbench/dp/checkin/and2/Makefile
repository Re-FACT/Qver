# Makefile



# defaults

SIM ?= icarus
include ${MAKEFILE_INC_HOME}/makefile_vcs.inc


TOPLEVEL_LANG ?= verilog

WAVES=1

VERILOG_SOURCES += and2_top_formal_verification.v
VERILOG_SOURCES += ${NETLIST_TYPE}/fabric_netlists.v


# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file

TOPLEVEL = and2_top_formal_verification


# MODULE is the basename of the Python test file

COCOTB_TEST_MODULES = test_and2

# --- THE COCOTB TWEAK FOR HANDLING X/Z ---
export COCOTB_RESOLVE_X=ZEROS

# include cocotb's make rules to take care of the simulator setup

include $(shell cocotb-config --makefiles)/Makefile.sim



