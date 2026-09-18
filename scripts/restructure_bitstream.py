#####################################################################
# A script to restructure fabric bitstream XML file based on rules
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
import xml.etree.ElementTree as ET
import time
from datetime import timedelta

#####################################################################
# Error codes
#####################################################################
error_codes = {"SUCCESS": 0, "ERROR": 1, "OPTION_ERROR": 2, "FILE_ERROR": 3}

XML_ROOT_NODE = "fabric_bitstream"
RESTRUCTURE_LEVEL = 1
INSERT_LEVEL = 1
FPGA_CORE_INST = "fpga_core_inst"

#####################################################################
# Initialize logger
#####################################################################
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


#####################################################################
# Restructure a bitstream from an input file and output to a file based
# on a given set of rules
#####################################################################
def restructure_bitstream(rule_db, input_bitstream_file, output_bitstream_file):
    start_time = time.time()

    max_filename_len = 80
    input_bitstream_fname = os.path.basename(input_bitstream_file)
    logging_space = "." * (max_filename_len - len(input_bitstream_fname))

    logging.info("Restructuring '" + input_bitstream_fname + "'" + logging_space)

    # If there is already a file, remove and create
    if not os.path.isfile(input_bitstream_fname):
        logging.error("Input bitstream file '" + input_bitstream_fname + "' does not exist!")
        exit(error_codes["ERROR"])

    # Parse the input bitstream file
    bitstream_tree = ET.parse(input_bitstream_fname)

    # Walk through the bitstream tree and apply rules
    root = bitstream_tree.getroot()
    for region in root:
        for bit in region:
            # get the path
            orig_path = bit.get("path")
            orig_modules = orig_path.split(".")
            # We only apply rules to the second element
            for key in rule_db:
                if key == orig_modules[RESTRUCTURE_LEVEL]:
                    orig_modules[RESTRUCTURE_LEVEL] = rule_db[key]
            # insert an intermediate module
            orig_modules.insert(INSERT_LEVEL, FPGA_CORE_INST)
            # update the path
            bit.set("path", ".".join(orig_modules))

    # Output the restructured bitstream
    output_bitstream_fname = os.path.basename(output_bitstream_file)
    bitstream_tree.write(output_bitstream_fname)

    logging_space = "." * (max_filename_len - len(output_bitstream_fname))
    logging.info("Restructured '" + output_bitstream_fname + "'" + logging_space + "[Done]")

    # Print time stats
    end_time = time.time()
    time_diff = timedelta(seconds=(end_time - start_time))
    time_str = " took " + str(time_diff)
    logging.info("Restructuring " + time_str)


#####################################################################
# Read task list from a yaml file
#####################################################################
def read_yaml_to_rule_database(yaml_filename):
    rule_db = {}
    with open(yaml_filename, "r") as stream:
        try:
            rule_db = yaml.load(stream, Loader=yaml.FullLoader)
            logging.info("Found " + str(len(rule_db)) + " rule to restructure bitstreams")
        except yaml.YAMLError as exc:
            logging.error(exc)
            exit(error_codes["FILE_ERROR"])

    return rule_db


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
        description="Restructure a bitstream file with a given set of rules defined in configuration file"
    )
    parser.add_argument("--rule_file", required=True, help="Configuration file in YAML format")
    parser.add_argument(
        "--input_bitstream_file",
        default="fabric_bitstream.xml",
        help="The path to input bitstream file",
    )
    parser.add_argument(
        "--restructured_bitstream_file",
        default="restructured_fabric_bitstream.xml",
        help="The path to output restructured bitstream file",
    )
    args = parser.parse_args()

    # Create a database for rules
    rule_db = {}
    rule_db = read_yaml_to_rule_database(args.rule_file)

    # Create copies based on the task list in database
    restructure_bitstream(rule_db, args.input_bitstream_file, args.restructured_bitstream_file)
