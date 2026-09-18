# 
# Verification Makefile
# =====================
SHELL = bash

PYTHON_EXEC ?= python3
SCRIPT_DIR = ${PWD}/../../../scripts
FABRIC_NAME = dp
BENCHMARK_SUITE_NAME = checkin
NUM_JOBS = 4
SIM = synopsys_vcs
SIM_THREAD_WAIT_TIME = 10
SIM_START_WAIT_TIME = 1
LOG_CHECK_WAIT_TIME = 2
COCOTB_TASKS = all
CLEAN_PREVIOUS_RUN = --clean_previous_run
WAVEFORM = none
COCOTB_TASK_CONFIG_POSTFIX=

# The path to RTL or Gate-level netlists
NETLIST_TYPE= gl

.SILENT:

# Execute every line in its own shell; Required to error out on any error we see!
.ONESHELL:

# Put it first so that "make" without argument is like "make help".
export COMMENT_EXTRACT

# Put it first so that "make" without argument is like "make help".
help:
	@${PYTHON_EXEC} -c "$$COMMENT_EXTRACT"

uncompress_golden_copies:
# Uncompress golden copies of netlists, benchmarks, bitstreams etc. required by a cocotb run
	tar xvf bitstreams.tar.gz;
	currDir=$${PWD} && cd .. && tar xvf netlist.tar.gz && cd $${currDir};

list_preconfig_cocotb_tasks:
# Setup the environment for cocotb tests by creating symbolic links and adapt testbench files
# Available variables:
# 
# - ``FABRIC_NAME=<string>``: see details in :ref:`developer_build_system_variables`
# - ``BENCHMARK_SUITE_NAME=<string>``: see details in :ref:`developer_build_system_variables`
	currDir=$${PWD} && \
	${PYTHON_EXEC} ${SCRIPT_DIR}/run_cocotb_task.py --config tasks/${FABRIC_NAME}/${BENCHMARK_SUITE_NAME}_benchmark_task${COCOTB_TASK_CONFIG_POSTFIX}.yaml --task ${COCOTB_TASKS} -j ${NUM_JOBS} --new_thread_wait_time ${SIM_THREAD_WAIT_TIME} --list_tasks || exit 1; \

setup_preconfig_cocotb: uncompress_golden_copies
# Setup the environment for cocotb tests by creating symbolic links and adapt testbench files
# Available variables:
# 
# - ``FABRIC_NAME=<string>``: see details in :ref:`developer_build_system_variables`
# - ``BENCHMARK_SUITE_NAME=<string>``: see details in :ref:`developer_build_system_variables`
	currDir=$${PWD} && \
	${PYTHON_EXEC} ${SCRIPT_DIR}/run_cocotb_task.py --config tasks/${FABRIC_NAME}/${BENCHMARK_SUITE_NAME}_benchmark_task${COCOTB_TASK_CONFIG_POSTFIX}.yaml --task ${COCOTB_TASKS} -j ${NUM_JOBS} --new_thread_wait_time ${SIM_THREAD_WAIT_TIME} --setup || exit 1; \

run_preconfig_cocotb:
# Setup the environment for cocotb tests by creating symbolic links and adapt testbench files
# Available variables:
# 
# - ``FABRIC_NAME=<string>``: see details in :ref:`developer_build_system_variables`
# - ``BENCHMARK_SUITE_NAME=<string>``: see details in :ref:`developer_build_system_variables`
	currDir=$${PWD} && \
	${PYTHON_EXEC} ${SCRIPT_DIR}/run_cocotb_task.py --config tasks/${FABRIC_NAME}/${BENCHMARK_SUITE_NAME}_benchmark_task${COCOTB_TASK_CONFIG_POSTFIX}.yaml --task ${COCOTB_TASKS} -j ${NUM_JOBS} --new_thread_wait_time ${SIM_THREAD_WAIT_TIME} --simulator ${SIM} --netlist_type ${NETLIST_TYPE} --params MAKEFILE_INC_HOME:${PWD}/../utils/cocotb_makeinc --sim_start_wait_time ${SIM_START_WAIT_TIME} --log_check_wait_time ${LOG_CHECK_WAIT_TIME} ${CLEAN_PREVIOUS_RUN} --dump_waveform ${WAVEFORM} --sdf_annotation || exit 1; \


# Functions to extract comments from Makefiles
define COMMENT_EXTRACT
import re
with open ('Makefile', 'r' ) as f:
    matches = re.finditer('^([a-zA-Z-_]*):.*\n#(.*)', f.read(), flags=re.M)
    for _, match in enumerate(matches, start=1):
        header, content = match[1], match[2]
        print(f"  {header:10} {content}")
endef
