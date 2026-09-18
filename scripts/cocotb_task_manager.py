import logging
import yaml
import os
import re

# Constants
GROUP_TAG = "group"
FABRIC_TAG = "fabric"
## Testcase attributes
TESTCASE_TAG = "testcases"
TESTCASE_NAME_TAG = "name"
TESTCASE_SETUPONLY_TAG = "setup_only"
TESTCASE_VARIABLE_TAG = "variables"
TESTCASE_FILE_TAG = "files"
TESTCASE_FILE_NAME_TAG = "name"
TESTCASE_FILE_TYPE_TAG = "type"
TESTCASE_FILE_SRC_TAG = "src"
TESTCASE_FILE_DES_TAG = "des"

# Reserved words
CURRENT_GROUP_KEYWORD = "[current_group]"
CURRENT_FABRIC_KEYWORD = "[current_fabric]"
CURRENT_NAME_KEYWORD = "[current_name]"

# Valid file types
VALID_TESTCASE_FILE_TYPE_RTL = "rtl"
VALID_TESTCASE_FILE_TYPE_GL = "gl"
VALID_TESTCASE_FILE_TYPE_PL = "pl"
VALID_TESTCASE_FILE_TYPE_COCOTBMAKFILE = "cocotb_makefile"
VALID_TESTCASE_FILE_TYPE_COCOTBTESTBENCH = "cocotb_testbench"
VALID_TESTCASE_FILE_TYPE_BITSTREAM_BASE = "bitstream_base"
VALID_TESTCASE_FILE_TYPE_BITSTREAM_VALUE = "bitstream_value"
VALID_TESTCASE_FILE_TYPE_COCOTBUTIL = "cocotb_util"
VALID_TESTCASE_FILE_TYPE_LINK = "link"
VALID_TESTCASE_FILE_TYPE_GL_SDF = "gl_sdf"
VALID_TESTCASE_FILE_TYPE_PL_SDF = "pl_sdf"

# Class of a Cocotb task manager
class CocotbTaskManager:
    def __init__(self):
        # Internal data
        self.__db_ = {}
        self.__is_dirty_ = True  # By default it should be dirty. After loading data and pass sanity checks, it becomes clean
        self.__VALID_TESTCASE_FILE_TYPES_ = [
            VALID_TESTCASE_FILE_TYPE_RTL,
            VALID_TESTCASE_FILE_TYPE_GL,
            VALID_TESTCASE_FILE_TYPE_PL,
            VALID_TESTCASE_FILE_TYPE_COCOTBMAKFILE,
            VALID_TESTCASE_FILE_TYPE_COCOTBTESTBENCH,
            VALID_TESTCASE_FILE_TYPE_BITSTREAM_BASE,
            VALID_TESTCASE_FILE_TYPE_BITSTREAM_VALUE,
            VALID_TESTCASE_FILE_TYPE_COCOTBUTIL,
            VALID_TESTCASE_FILE_TYPE_LINK,
            VALID_TESTCASE_FILE_TYPE_GL_SDF,
            VALID_TESTCASE_FILE_TYPE_PL_SDF,
        ]

    def __is_key_exist(self, key, path):
        if key in path:
            return True
        return False

    def __replace_reserved_words(self, fname, testcase_idx):
        temp_fname = fname
        temp_fname = temp_fname.replace(CURRENT_GROUP_KEYWORD, self.group())
        temp_fname = temp_fname.replace(CURRENT_FABRIC_KEYWORD, self.fabric())
        temp_fname = temp_fname.replace(CURRENT_NAME_KEYWORD, self.testcase_name(testcase_idx))
        return temp_fname

    def __replace_variables(self, fname, testcase_idx):
        temp_fname = fname
        for var in self.testcase_variables(testcase_idx):
            val = self.testcase_variable_value(testcase_idx, var)
            val_kw = f"[{var}]"
            temp_fname = temp_fname.replace(val_kw, val)
        return temp_fname

    def __check_testcase_index(self, testcase_idx):
        if testcase_idx not in self.testcases():
            raise Exception(
                f"Testcase index '{testcase_idx}' which is out of range of testcases [0, {len(self.testcases())})!"
            )

    def __check_testcase_file_index(self, testcase_idx, file_idx):
        self.__check_testcase_index(testcase_idx)
        if file_idx not in self.testcase_files(testcase_idx):
            raise Exception(
                f"File index '{file_idx}' which is out of range of files [0, {len(self.testcase_files(testcase_idx))}) in testcase '{self.testcase_name(testcase_idx)}'!"
            )

    # get the selected benchmark suite group
    def group(self):
        self.__check_valid()
        return self.__db_[GROUP_TAG]

    # get the selected fabric
    def fabric(self):
        self.__check_valid()
        return self.__db_[FABRIC_TAG]

    # Get the testcase tasks
    def testcases(self):
        self.__check_valid()
        if TESTCASE_TAG in self.__db_.keys():
            return range(len(self.__db_[TESTCASE_TAG]))
        return range(0)

    # Get the name of a testcase
    def testcase_name(self, testcase_idx):
        self.__check_valid()
        self.__check_testcase_index(testcase_idx)
        return self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_NAME_TAG]

    # Get the name of a testcase
    def testcase_setup_only(self, testcase_idx):
        self.__check_valid()
        self.__check_testcase_index(testcase_idx)
        if TESTCASE_SETUPONLY_TAG in self.__db_[TESTCASE_TAG][testcase_idx]:
            return self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_SETUPONLY_TAG]
        return False

    # Get the variables of a step of a pd task
    def testcase_variables(self, testcase_idx):
        self.__check_valid()
        self.__check_testcase_index(testcase_idx)
        if TESTCASE_VARIABLE_TAG in self.__db_[TESTCASE_TAG][testcase_idx]:
            return self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_VARIABLE_TAG].keys()
        return []

    # Get the variables of a step of a pd task
    def testcase_variable_value(self, testcase_idx, var_name):
        self.__check_valid()
        self.__check_testcase_index(testcase_idx)
        if var_name not in self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_VARIABLE_TAG]:
            raise Exception(
                f"Invalid variable name '{var_name}' which is not defined in the testcase '{self.testcase_name(testcase_idx)}'!"
            )
        fname = self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_VARIABLE_TAG][var_name]
        fname = self.__replace_reserved_words(fname, testcase_idx)
        return fname

    # Return the list of files defined under a given testcase
    def testcase_files(self, testcase_idx):
        self.__check_valid()
        self.__check_testcase_index(testcase_idx)
        if TESTCASE_FILE_TAG in self.__db_[TESTCASE_TAG][testcase_idx]:
            return range(len(self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_FILE_TAG]))
        # It is illegal to define empty file list!
        raise Exception(
            f"Empty file list under the testcase '{self.testcase_name(testcase_idx)}'! Each testcase requires a list of files!"
        )
        return range(0)

    # Get the name of file defined under a given testcase
    def testcase_file_name(self, testcase_idx, file_idx):
        self.__check_valid()
        # Check ranges
        self.__check_testcase_file_index(testcase_idx, file_idx)
        return self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_FILE_TAG][file_idx][
            TESTCASE_FILE_NAME_TAG
        ]

    # Get the type of file defined under a given testcase
    def testcase_file_type(self, testcase_idx, file_idx):
        self.__check_valid()
        # Check ranges
        self.__check_testcase_file_index(testcase_idx, file_idx)
        ftype = self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_FILE_TAG][file_idx][
            TESTCASE_FILE_TYPE_TAG
        ]
        # Check if file type is valid or not
        if ftype not in self.__VALID_TESTCASE_FILE_TYPES_:
            raise Exception(
                f"Invalid file type '{ftype}' under the testcase '{self.testcase_name(testcase_idx)}'! Expect {self.__VALID_TESTCASE_FILE_TYPES_}!"
            )
        return ftype

    # Get the source path of file defined under a given testcase
    def testcase_file_src(self, testcase_idx, file_idx):
        self.__check_valid()
        # Check ranges
        self.__check_testcase_file_index(testcase_idx, file_idx)
        fpath = self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_FILE_TAG][file_idx][
            TESTCASE_FILE_SRC_TAG
        ]
        # Check if file type is valid or not
        fpath = self.__replace_reserved_words(fpath, testcase_idx)
        fpath = self.__replace_variables(fpath, testcase_idx)
        return fpath

    # Get the destination path of file defined under a given testcase
    def testcase_file_des(self, testcase_idx, file_idx):
        self.__check_valid()
        # Check ranges
        self.__check_testcase_file_index(testcase_idx, file_idx)
        fpath = self.__db_[TESTCASE_TAG][testcase_idx][TESTCASE_FILE_TAG][file_idx][
            TESTCASE_FILE_DES_TAG
        ]
        # Check if file type is valid or not
        fpath = self.__replace_reserved_words(fpath, testcase_idx)
        fpath = self.__replace_variables(fpath, testcase_idx)
        return fpath

    # Internal method to check if data is valid, throw exeception when invalid. Useful for accessors
    def __check_valid(self):
        if self.__is_dirty_ == True:
            raise Exception("Try to access data when internal data is still dirty. Load data first")

    def is_valid(self):
        return not (self.__is_dirty_)

    # Load data from yaml file
    def load(self, yaml_filename):
        self.__db_ = {}  # Ensure a clean start
        with open(yaml_filename, "r") as stream:
            try:
                self.__db_ = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                logging.error(exc)
        # TODO: May need a validator before flip the flag!
        self.__is_dirty_ = False

    # Clear all the data
    def clear(self):
        self.__init__()
