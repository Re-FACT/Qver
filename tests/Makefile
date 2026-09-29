# 
# Regression Test Makefile
# ========================
# 
PYTHON_EXEC ?= python3
SCRIPT_DIR = ${PWD}/../scripts

.SILENT:

# Put it first so that "make" without argument is like "make help".
export COMMENT_EXTRACT

# Put it first so that "make" without argument is like "make help".
help:
	@${PYTHON_EXEC} -c "$$COMMENT_EXTRACT"

test_setup_cocotb:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test cocotb setup start ===="
	currDir=$${PWD} && cd setup_dv/dv && make setup_preconfig_cocotb && cd $${currDir} || exit 1;
	echo "==== Test cocotb setup finished ===="

test_setup_cocotb_partial_sim:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test cocotb setup with partial simulation start ===="
	currDir=$${PWD} && cd setup_dv/dv && make setup_preconfig_cocotb COCOTB_TASK_CONFIG_POSTFIX=_partial_sim && cd $${currDir} || exit 1;
	echo "==== Test cocotb setup with partial simulation finished ===="

test_list_tasks:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test list tasks start ===="
	currDir=$${PWD} && cd setup_dv/dv && make list_preconfig_cocotb_tasks && cd $${currDir} || exit 1;
	echo "==== Test list tasks end ===="

test_run_cocotb:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test run cocotb simulation flow start ===="
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb && cd $${currDir} || exit 1;
	echo "==== Test run cocotb simulation flow end ===="

test_run_cocotb_selected_task:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test run cocotb simulation flow for selected tasks begin ===="
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 && cd $${currDir} || exit 1;
	echo "==== Test run cocotb simulation flow for selected tasks end ===="

test_run_cocotb_partial_sim:
# This command tests the functionality of setup cocotb dv tasks
	echo "==== Test run cocotb simulation flow for selected tasks with partial simulation start ===="
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASK_CONFIG_POSTFIX=_partial_sim && cd $${currDir} || exit 1;
	echo "==== Test run cocotb simulation flow for selected tasks with partial simulation end ===="

test_run_cocotb_waveform:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb WAVEFORM=fsdb && cd $${currDir} || exit 1;

test_run_cocotb_modelsim:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 SIM=mentor_modelsim && cd $${currDir} || exit 1;

test_run_cocotb_vcs:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 SIM=synopsys_vcs && cd $${currDir} || exit 1;

test_run_cocotb_questa:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 SIM=mentor_questa && cd $${currDir} || exit 1;

test_run_cocotb_incisive:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 SIM=cadence_incisive && cd $${currDir} || exit 1;

test_run_cocotb_xcelium:
# This command tests the functionality of setup cocotb dv tasks
	currDir=$${PWD} && cd setup_dv/dv && make run_preconfig_cocotb COCOTB_TASKS=and2 SIM=cadence_xcelium && cd $${currDir} || exit 1;

all:
	make test_setup_cocotb
	make test_setup_cocotb_partial_sim
	make test_list_tasks
	make test_run_cocotb
	make test_run_cocotb_partial_sim
	make test_run_cocotb_selected_task
#	make test_run_cocotb_waveform
#	make test_run_cocotb_modelsim
#	make test_run_cocotb_vcs
#	make test_run_cocotb_questa
# The two simulators require more tuning 
#	make test_run_cocotb_incisive
#	make test_run_cocotb_xcelium

# Functions to extract comments from Makefiles
define COMMENT_EXTRACT
import re
with open ('Makefile', 'r' ) as f:
    matches = re.finditer('^([a-zA-Z-_]*):.*\n#(.*)', f.read(), flags=re.M)
    for _, match in enumerate(matches, start=1):
        header, content = match[1], match[2]
        print(f"  {header:10} {content}")
endef
