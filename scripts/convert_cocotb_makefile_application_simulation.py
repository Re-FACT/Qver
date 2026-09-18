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
def convert_makefile_for_application_simulation(makefile_path):
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
    verilog_sources_cache = ""
    for line in makefile_f:
        # Skip all the VERILOG_SOURCES
        if line.startswith("VERILOG_SOURCES "):
            verilog_sources_cache += line + "\n"
        elif line.startswith("include "):
            continue
        else:
            cached_content += line

    verilog_sources_cache_composed = f"""ifeq ($(strip $(VERILOG_SOURCES_USER)),) \n \t {verilog_sources_cache} \n else \n \tVERILOG_SOURCES = $(VERILOG_SOURCES_USER) \n endif"""
    cached_content += verilog_sources_cache_composed + "\n"
    cached_content += "include ${MAKEFILE_INC_HOME}/makefile_vcs.inc \n"
    cached_content += "include $(shell cocotb-config --makefiles)/Makefile.sim\n"
    makefile_f.close()
    # Second pass on the makefile: output modified lines
    makefile_f = open(makefile_path, "w")
    makefile_f.write(cached_content)
    makefile_f.close()

    logging.info("Converted makefile '" + makefile_name + "'" + logging_space + "[Done]")


#####################################################################
# Main function
#####################################################################
if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement

    # Parse the options and apply sanity checks
    parser = argparse.ArgumentParser(
        description="Convert makefile for application simulation using cocotb with a given makefile"
    )
    parser.add_argument("--make_file", required=True, help="makefile to be converted")
    args = parser.parse_args()

    # Create copies based on the task list in database
    convert_makefile_for_application_simulation(args.make_file)
    logging.info("Converted Makefiles: " + args.make_file)
