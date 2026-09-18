.. _user_interface:

User Interface
--------------

The script has a command-line user interface which allows users to customize their ICC2 jobs.

A short version of command-line options can be shown by calling the help desk through

.. code-block:: yaml

  python3 scripts/run_cocotb_task.py --help 


.. option:: --help

  Show help desk to list all the options

.. option:: --config <string>

  Specify the task configuration file to perform Cocotb jobs. See file format in `:ref:file_format_task_file` 

.. option:: --setup

  Only setup envoirnment for cocotb tasks. Simulation will be not executed

.. option:: --task <string>

  Specify the names of cocotb tasks to be executed. This allows users to select one or a number of tasks to be run. 
  Use comma as a splitter between tasks, e.g., 

.. code-block:: 

  task1,task2,task3

By default, run all the listed tasks

.. note:: Please do not use the reserved word ``all`` as task name in your task configuration file

.. option:: -j <int> or --jobs <int>

  Specify the maximum number of jobs to be run in parallel

.. option:: --list_tasks

  List all the tasks defined in the task configuration file

.. option:: --simulator <string>

  Specify the simulator to be used when running cocotb tasks. Can be [ ``vcs`` | ``modelsim`` | ``icarus`` ]. By default, it is ``vcs``

.. option:: --params <string> 

  Specify the envoirnment variables to be included. Use comma to split. Use column to define values. For example,

.. code-block::

  cell_lib_home:0,makefile_inc_home:../

.. note:: Wait time is strongly recommended if you are working a server or a machine where disk operation takes a long latency

.. option:: --new_thread_wait_time <int>

  Specify the waiting time before starting a new thread (unit: second)

.. option:: --sim_start_wait_time <int>

  Specify the waiting time between cleaning up previous results and starting a new round of simulation (unit: second)

.. option:: --log_check_wait_time <int>

  Specify the waiting time between ending a simulation and starting log check(unit: second)

.. option:: --clean_previous_run

  Clean results from previous run before any simulation job

.. option::  --dump_waveform <string>

  Enable waveform to be outputted. Specify the format of waveform file, [ ``none`` | ``vcd`` | ``fsdb`` ]
