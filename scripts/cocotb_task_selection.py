import time
import logging

ALL_TASKS_SELECTED = "all"


# Class of a Cocotb task selection
# Task selection accepts a string that defines a list of selected tasks, including designs and steps
# The format is
#  taskA,taskB
# Note that keyword all may be applied to select all tasks, design and steps!
class CocotbTaskSelection:
    def __init__(self):
        # Internal data
        self.__tasks_ = {}
        self.__is_dirty_ = True  # Remain dirty is there is no predefined tasks!
        # Constants
        self.__SELECT_ALL_ = ALL_TASKS_SELECTED
        self.__TASK_DELIMA_ = ","

    # Return the number of selected jobs
    def num_selected(self):
        cnt = 0
        for k_task in self.__tasks_:
            if self.is_task_selected(k_task):
                cnt += 1
        return cnt

    # Return the total number of jobs
    def total(self):
        cnt = 0
        for k_task in self.__tasks_:
            cnt += 1
        return cnt

    # Load from predefined tasks which are the based on selected tasks
    def add_predefined_task(self, task_name):
        self.__tasks_[task_name] = False
        # No longer dirty
        self.__is_dirty_ = False

    # Mark all tasks as selected
    def __select_all_tasks(self):
        for k_task in self.__tasks_:
            self.__tasks_[k_task] = True

    # Load from an string
    def read_task_selection_str(self, task_str):
        if self.__is_dirty_:
            raise Exception("Read task selection requires tasks to be predefined first!")
        # all select keyword has no. 1 priority
        if task_str == self.__SELECT_ALL_:
            self.__select_all_tasks()
            return 0
        selected_tasks = task_str.split(self.__TASK_DELIMA_)
        # Now parsing
        for s_task in selected_tasks:
            if s_task not in self.__tasks_.keys():
                raise Exception(f"Invalid task '{s_task}' which is not predefined!")
            self.__tasks_[s_task] = True

    def is_task_selected(self, s_task):
        if s_task not in self.__tasks_:
            raise Exception(f"Invalid task '{s_task}' which is not predefined!")
        return self.__tasks_[s_task]

    # Print a list of designs under the selected task
    def list_tasks(self, selected_only=False):
        extra_msg = ""
        if selected_only:
            extra_msg = "selected "
        logging.info(f"List all the {extra_msg} tasks:")
        for curr_task in self.__tasks_.keys():
            # Check if the task is selected or not
            if selected_only and not self.is_task_selected(curr_task):
                continue
            logging.info(f"\t{curr_task}")
