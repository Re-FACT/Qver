#####################################################################
# A script to adapt Cocotb testbench to force bitstream
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

TAB_STR = " " * 4

#####################################################################
# Initialize logger
#####################################################################
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


#####################################################################
# Convert a Cocotb test file by modifying lines with keywords
#####################################################################
def convert_cocotb_testbench(
    src_testbench_path,
    des_testbench_path,
    rtl_bitstream_filename,
    base_bitstream_filename,
    cocotb_util_lib,
):
    max_filename_len = 40
    des_testbench_fname = os.path.basename(des_testbench_path)
    logging_space = "." * (max_filename_len - len(des_testbench_fname))
    # If there is already a file, remove and create
    if not os.path.isfile(src_testbench_path):
        logging.error("Cocotb testbench '" + src_testbench_path + "' does not exist!")
        exit(error_codes["ERROR"])

    # First pass on the makefile: cache lines and modify
    testbench_f = open(src_testbench_path, "r")
    cached_content = ""
    first_import = True
    force_bitstream_code = False
    for line in testbench_f:
        if line.startswith("import ") and first_import:
            # Include util library
            line += "import " + cocotb_util_lib + "\n"
            line += "import os" + "\n"
            first_import = False

        # Only force bitstream to the cocotb test code block
        if line.startswith("@cocotb.test"):
            force_bitstream_code = True
        if line.startswith("async def ") and force_bitstream_code:
            # Call force bitstream function
            line += TAB_STR + "if \"rtl\" == os.environ['NETLIST_TYPE']:" + "\n"
            line += (
                TAB_STR * 2
                + cocotb_util_lib
                + '.cocotb_force_bitstream_to_dut_from_xml(dut, "'
                + rtl_bitstream_filename
                + '", "'
                + base_bitstream_filename
                + '", "rtl")'
                + "\n"
            )
            line += TAB_STR + "elif \"gl\" == os.environ['NETLIST_TYPE']:" + "\n"
            line += (
                TAB_STR * 2
                + cocotb_util_lib
                + '.cocotb_force_bitstream_to_dut_from_xml(dut, "'
                + rtl_bitstream_filename
                + '", "'
                + base_bitstream_filename
                + '", "gl")'
                + "\n"
            )
            line += TAB_STR + "elif \"pl\" == os.environ['NETLIST_TYPE']:" + "\n"
            line += (
                TAB_STR * 2
                + cocotb_util_lib
                + '.cocotb_force_bitstream_to_dut_from_xml(dut, "'
                + rtl_bitstream_filename
                + '", "'
                + base_bitstream_filename
                + '", "pl")'
                + "\n"
            )
            # Reset flag
            force_bitstream_code = False

        cached_content += line

    testbench_f.close()

    # Second pass on the makefile: output modified lines
    testbench_f = open(des_testbench_path, "w")
    testbench_f.write(cached_content)
    testbench_f.close()

    logging.info(
        "Converted cocotb testbench '" + des_testbench_fname + "'" + logging_space + "[Done]"
    )


#####################################################################
# Adapt the cocotb testbench one by one from a task list
#####################################################################
def convert_cocotb_testbenches(
    task_db, rtl_bitstream_filename, base_bitstream_filename, cocotb_util_lib
):
    for src_file in task_db.keys():
        cocotb_testbench_srcfile_abspath = os.getcwd() + "/" + src_file
        cocotb_testbench_desfile_abspath = os.getcwd() + "/" + task_db[src_file]
        convert_cocotb_testbench(
            cocotb_testbench_srcfile_abspath,
            cocotb_testbench_desfile_abspath,
            rtl_bitstream_filename,
            base_bitstream_filename,
            cocotb_util_lib,
        )


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
        description="Convert cocotb testbench by adding bitstream force support with a given list defined in configuration file"
    )
    parser.add_argument("--config_file", required=True, help="Configuration file in YAML format")
    parser.add_argument(
        "--rtl_bitstream_filename",
        default="fabric_bitstream.xml",
        help="The file name of RTL bitstreams which should be included in cocotb testbench",
    )
    parser.add_argument(
        "--base_bitstream_filename",
        default="fabric_bitstream_base.xml",
        help="The file name of base bitstreams which should be included in cocotb testbench",
    )
    parser.add_argument(
        "--cocotb_util_lib",
        default="cocotb_force_bitstream",
        help="The python library name that is designed to force bitstreams",
    )
    args = parser.parse_args()

    # Create a database for tasks
    task_db = {}
    task_db = read_yaml_to_task_database(args.config_file)

    # Create copies based on the task list in database
    convert_cocotb_testbenches(
        task_db, args.rtl_bitstream_filename, args.base_bitstream_filename, args.cocotb_util_lib
    )
    logging.info("Converted " + str(len(task_db)) + " cocotb tests")
