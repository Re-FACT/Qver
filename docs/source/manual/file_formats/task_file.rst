.. _file_format_task_file:

Task File (.yaml)
=================

- The task file aims to provide a standard way for users to create a Cocotb task run. 
- The task file is the key input file for users to craft, before running a Cocotb task.

An example of file is shown as follows.

.. literalinclude:: cocotb_task_example.yaml
  :language: yaml


General Syntax
--------------

These are all required syntax, which helps users to define template of tasks.

.. option:: group="<string>"

  An unique name for the benchmark suite. Once defined, any later content that contains string of ``[current_group]`` will be replaced with the group name.

.. option:: fabric="<string>"

  An unique name for the fabric. Once defined, any later content that contains string of ``[current_fabric]`` will be replaced with the fabric name.

.. option:: setup_only="<bool>"

  Do not run simulation for this task. This is used when a benchmark is still buggy. By default, it is set to false. This is an optional syntax

Testcases
---------

Each cocotb testcase should be defined under this section

.. option:: name="<string>"

  Specify the unique name for this testcase.

.. option:: variables="<list>"

  List all the variables which will be utilized by the files. For example, 

.. code-block::

  # You define a variable under variables, it can be used when defining any file path
  variables:
    netlist_path: "../netlist"
  files:
    - name: rtl
      type: rtl
      src: "[netlist_path]/rtl"

Files
-----

All the related files to the testcase should be defined under section ``file``

.. option:: name="<string>"

  Specify the unique name for the file

.. option:: src="<string>"

  Specify the source file path, from which the file will be linked or copied.

.. option:: des="<string>"

  Specify the destination file path, to which the file will be linked or copied.

.. option:: type="<string>"

  Specify the type of the file. Can be [ ``rtl`` | ``gl`` | ``pl`` | ``cocotb_makefile`` | ``cocotb_testbench`` | ``bitstream_base`` | ``bitstream_value`` | ``cocotb_util`` | ``link`` ]. Depending on the file type, different operations will be applied.

  - ``cocotb_makefile`` defines where the runtime directory of the testcase locates. The makefile will be copied from source path and adapted for FPGA scenario. 
  - ``cocotb_testbench`` defines where the python-based cocotb testbench locates. The testbench will be copied from source path and adapted for FPGA scenario.
  - All the other file types will result in symbolic links from the source path to the destination path.

  Note that for each testcase, at least one type of netlist among ``rtl``, ``gl``, and ``pl`` should be defined. If user specifies to run a testcase based on a specific type of netlist, e.g., ``gl``, the testcase must contain a ``gl`` file. Otherwise, error will be flagged.

  All the unique file types should be defined for a testcase. For example, there should be one and only one file in the list whose type is ``rtl``.

  The only exception is the ``link`` which can be defined multiple times
