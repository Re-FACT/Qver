#####################################################################
# A script to adapt Cocotb Makefile from testing RTL to testing FPGA fabric
#####################################################################
import os
from os.path import dirname, abspath
import argparse
import logging
import subprocess
import hashlib
import yaml
import shutil
import re

#####################################################################
# Error codes
#####################################################################
error_codes = {"SUCCESS": 0, "ERROR": 1, "OPTION_ERROR": 2, "FILE_ERROR": 3}

#####################################################################
# Initialize logger
#####################################################################
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


#####################################################################
# Convert a Makefile by modifying lines with keywords
#####################################################################
def convert_makefile(makefile_path, top_module_postfix):
    max_filename_len = 40
    makefile_name = os.path.basename(makefile_path)
    logging_space = "." * (max_filename_len - len(makefile_name))
    # If there is already a file, remove and create
    if not os.path.isfile(makefile_path):
        logging.error("Makefile '" + makefile_path + "' does not exist!")
        exit(error_codes["ERROR"])

    # Get top-level module from the makefile
    top_module = ""
    with open(makefile_path, "r") as makefile_f:
        for line in makefile_f:
            if line.startswith("TOPLEVEL "):
                searchObj = re.search(r"TOPLEVEL(\s+)=(\s+)(.*)", line)
                top_module = searchObj.group(3)
    if not top_module:
        logging.error("Makefile '" + makefile_path + "' does not have a top module defined!")
        exit(error_codes["ERROR"])
    logging.debug("Found top module: " + top_module)

    # First pass on the makefile: cache lines and modify
    makefile_f = open(makefile_path, "r")
    add_verilog_source = True
    cached_content = ""
    for line in makefile_f:
        # Add dedicated makefile inc
        if line.startswith("SIM "):
            line = line.strip()
            line += "\n" + "include ${MAKEFILE_INC_HOME}/makefile_vcs.inc"

        if line.startswith("TOPLEVEL "):
            line = line.strip()
            line += top_module_postfix

        # Skip all the VERILOG_SOURCES
        if line.startswith("VERILOG_SOURCES "):
            line = line.strip()
            searchObj = re.search(r"VERILOG_SOURCES(\s+)\+=(\s+)(.*)", line)
            verilog_fname = searchObj.group(3)
            logging.debug("Found a verilog source file: " + verilog_fname)

            # Only add postfix to top-level module
            if verilog_fname == top_module + ".v":
                line = re.sub(r"\.v$", "", line)
                line += top_module_postfix + ".v"
            else:
                # Skip any other lines defining verilog sources
                continue
            # Add RTL links depending on netlist
            if add_verilog_source:
                line += "\n" + "VERILOG_SOURCES += ${NETLIST_TYPE}/fabric_netlists.v"
                add_verilog_source = False

        cached_content += line + "\n"

    makefile_f.close()

    # Second pass on the makefile: output modified lines
    makefile_f = open(makefile_path, "w")
    makefile_f.write(cached_content)
    makefile_f.close()

    logging.info("Converted makefile '" + makefile_name + "'" + logging_space + "[Done]")


#####################################################################
# Adapt the Makefile one by one from a task list
#####################################################################
def convert_makefiles(task_db, top_module_postfix):
    for src_file in task_db.keys():
        makefile_file_abspath = os.getcwd() + "/" + task_db[src_file]
        convert_makefile(makefile_file_abspath, top_module_postfix)


#####################################################################
# Read task list from a yaml file
#####################################################################
def read_yaml_to_task_database(yaml_filename):
    task_db = {}
    with open(yaml_filename, "r") as stream:
        try:
            task_db = yaml.load(stream, Loader=yaml.FullLoader)
            logging.info("Found " + str(len(task_db)) + " tasks to create symbolic links")
        except yaml.YAMLError as exc:
            logging.error(exc)
            exit(error_codes["FILE_ERROR"])

    return task_db


#####################################################################
# Write result database to a yaml file
#####################################################################
def write_result_database_to_yaml(result_db, yaml_filename):
    with open(yaml_filename, "w") as yaml_file:
        yaml.dump(result_db, yaml_file, default_flow_style=False)


#####################################################################
# Main function
#####################################################################
if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement

    # Parse the options and apply sanity checks
    parser = argparse.ArgumentParser(
        description="Convert makefile for cocotb with a given list defined in configuration file"
    )
    parser.add_argument("--config_file", required=True, help="Configuration file in YAML format")
    parser.add_argument(
        "--top_module_postfix",
        default="_top_formal_verification",
        help="The postfix to be added to the top module in each Makefile",
    )
    args = parser.parse_args()

    # Create a database for tasks
    task_db = {}
    task_db = read_yaml_to_task_database(args.config_file)

    # Create copies based on the task list in database
    convert_makefiles(task_db, args.top_module_postfix)
    logging.info("Converted " + str(len(task_db)) + " Makefiles")
