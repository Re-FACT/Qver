#####################################################################
# A script to run a IC Compiler II with a given task configuration
#####################################################################
import os
from os.path import dirname, abspath
import glob
import argparse
import logging
import re
import time
from datetime import timedelta
from datetime import datetime
from xml.dom import minidom
import cocotb_task_manager
import cocotb_task_selection
import cocotb_job_manager

#####################################################################
# Error codes
#####################################################################
error_codes = {"SUCCESS": 0, "ERROR": 1, "FILE_ERROR": 2}

# Constants
ICC2_TCL_FNAME = "run_icc2.tcl"
SIM_NAME_MAP = {
    "synopsys_vcs": "vcs",
    "icarus_verilog": "icarus",
    "mentor_questa": "questa",
    "mentor_modelsim": "modelsim",
    "cadence_incisive": "ius",
    "cadence_xcelium": "xcelium",
}
space_limit = 80  # Maximum space tuned for the screen width

#####################################################################
# Initialize logger
#####################################################################
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


#####################################################################
# Create a simulation job in cocotb
#####################################################################
def create_cocotb_sim_job(
    job_mgr,
    job_name,
    task_mgr,
    tc_id,
    req_nlist_type,
    simulator,
    extra_params,
    clean_prev_run,
    waveform_format,
    sdf_annotation_enabled,
):
    job_mgr.create_job(job_name)
    # Flag to identify if netlist type is valid
    meet_nlist_type = False
    # Set job attributes
    for file_id in task_mgr.testcase_files(tc_id):
        file_src = task_mgr.testcase_file_src(tc_id, file_id)
        file_des = task_mgr.testcase_file_des(tc_id, file_id)
        file_type = task_mgr.testcase_file_type(tc_id, file_id)
        job_mgr.add_file_to_job(job_name, file_src, file_des, file_type)
        if file_type == req_nlist_type:
            meet_nlist_type = True
    # General settings
    job_mgr.set_simulator(job_name, simulator)
    job_mgr.set_netlist_type(job_name, req_nlist_type)
    job_mgr.set_extra_parameters(job_name, extra_params)
    job_mgr.set_clean_previous_run(job_name, clean_prev_run)
    job_mgr.set_waveform_format(job_name, waveform_format)
    job_mgr.set_sdf_annotation_enabled(job_name, sdf_annotation_enabled)
    # Sanity check
    if not meet_nlist_type:
        raise Exception(
            f"Task '{task_mgr.testcase_name(tc_id)}' missing netlist '{req_nlist_type}' as required to run simulation. Please double check your task configuration file!"
        )


#####################################################################
# Main function
#####################################################################
if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement

    # Parse the options and apply sanity checks
    parser = argparse.ArgumentParser(description="Run a cocotb task for preconfigured simulation")
    parser.add_argument("--config", required=True, help="The task configuration file")
    parser.add_argument("--setup", action="store_true", help="Setup environment for cocotb tasks")
    parser.add_argument(
        "--task",
        default=cocotb_task_selection.ALL_TASKS_SELECTED,
        help=f"Specify the names of cocotb tasks to be executed. This allows users to select one or a number of tasks to be run. Use comma as a splitter between tasks, e.g., task1,task2,task3. By default, run all the listed tasks (equivalent to --task={cocotb_task_selection.ALL_TASKS_SELECTED}).",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default="2",
        help="The maximum number of jobs to be run in parallel",
    )
    parser.add_argument(
        "--list_tasks",
        action="store_true",
        help="List all the defined task names",
    )
    parser.add_argument(
        "--simulator",
        default=list(SIM_NAME_MAP.keys())[0],
        choices=list(SIM_NAME_MAP.keys()),
        help="Specify the HDL simulator to be used in cocotb. By default, we consider the Synopsys VCS",
    )
    parser.add_argument(
        "--netlist_type",
        default="rtl",
        help="Specify the type of netlists in simulation: [rtl|gl]",
    )
    parser.add_argument(
        "--params",
        default="",
        help="Specify the envoirnment variables to be included. Use comma to split. Use column to define values. For example, cell_lib_home:0,makefile_inc_home:../",
    )
    parser.add_argument(
        "--new_thread_wait_time",
        type=int,
        default="10",
        help="Specify the waiting time before starting a new thread (unit: second)",
    )
    parser.add_argument(
        "--sim_start_wait_time",
        type=int,
        default="10",
        help="Specify the waiting time between cleaning up previous results and starting a new round of simulation (unit: second)",
    )
    parser.add_argument(
        "--log_check_wait_time",
        type=int,
        default="10",
        help="Specify the waiting time between ending a simulation and starting log check(unit: second)",
    )
    parser.add_argument(
        "--clean_previous_run",
        action="store_true",
        help="Clean results from previous run before any simulation job",
    )
    parser.add_argument(
        "--dump_waveform",
        type=str,
        default="none",
        choices=["none", "vcd", "fsdb"],
        help="Enable waveform to be outputted. Specify the format of waveform file, [ none | vcd | fsdb ]",
    )
    parser.add_argument(
        "--sdf_annotation",
        action="store_true",
        help="Enable SDF annotation for gate-level or post-layout simulations",
    )
    # Log runtime
    start_time = time.time()

    args = parser.parse_args()

    num_errors = 0

    # Read task configuration
    task_mgr = cocotb_task_manager.CocotbTaskManager()
    task_mgr.load(args.config)

    job_mgr = cocotb_job_manager.CocotbJobManager()
    # Preload task selection
    task_sel = cocotb_task_selection.CocotbTaskSelection()
    for tc_id in task_mgr.testcases():
        task_sel.add_predefined_task(task_mgr.testcase_name(tc_id))
    task_sel.read_task_selection_str(args.task)
    # Report a stats for selected jobs
    logging.info(f"Selected {task_sel.num_selected()}/{task_sel.total()} jobs")
    # Early exit on queries about list_designs and list_steps
    if args.list_tasks:
        task_sel.list_tasks()
        exit(error_codes["SUCCESS"])
    # Setup job manager
    job_mgr.set_new_thread_wait_time(args.new_thread_wait_time)
    job_mgr.set_sim_start_wait_time(args.sim_start_wait_time)
    job_mgr.set_log_check_wait_time(args.log_check_wait_time)
    # Create a separated runtime directory and run
    for tc_id in task_mgr.testcases():
        job_name = task_mgr.testcase_name(tc_id)
        # Filter out the unselected task steps
        curr_job_selected = task_sel.is_task_selected(job_name)
        if not curr_job_selected:
            continue
        job_name_str = job_name
        if not args.setup and task_mgr.testcase_setup_only(tc_id):
            logging.info(
                f"Skip job '{job_name_str}' for simulation as defined in task configuration file"
            )
            continue
        logging.info(f"Selected job '{job_name_str}'")
        create_cocotb_sim_job(
            job_mgr,
            job_name,
            task_mgr,
            tc_id,
            args.netlist_type,
            SIM_NAME_MAP[args.simulator],
            args.params,
            args.clean_previous_run,
            args.dump_waveform,
            args.sdf_annotation,
        )
    # Run setup job
    if args.setup:
        job_mgr.run_setup_all(args.jobs, True)
        num_errors += job_mgr.num_errors()
        if num_errors:
            logging.info(f"Cocotb setup job finished with {num_errors} errors")
        else:
            logging.info(f"Cocotb setup job finished successfully")

    # Run DC and check errors
    #    if args.setup or args.parse_report_only:
    if args.setup:
        logging.info("User selects to skip running simulation.")
    else:
        # Run simulation job
        job_mgr.run_cocotb_all(args.jobs, False)
        num_errors += job_mgr.num_errors()
        if num_errors:
            logging.info(f"Cocotb simulation job finished with {num_errors} errors")
        else:
            logging.info(f"Cocotb simulation job finished successfully")
        # if args.output_job_status:
        #    job_mgr.write_job_status(args.output_job_status)

    #    if args.parse_report_only:
    #        logging.info(f"Generating Cocotb simulation report summary...")
    #        logging.info(f"Done")

    end_time = time.time()
    time_diff = timedelta(seconds=(end_time - start_time))

    time_str = "Running Cocotb flow took " + str(time_diff)
    logging.info(time_str)

    if num_errors == 0:
        exit(error_codes["SUCCESS"])
    else:
        exit(error_codes["ERROR"])
