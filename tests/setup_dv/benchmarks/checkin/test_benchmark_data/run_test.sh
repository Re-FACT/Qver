#!/bin/bash
# Complete SDF annotation functionality test

echo "==================================================="
echo "Starting SDF Annotation Functionality Test"
echo "Working directory: $(pwd)"
echo "==================================================="

# Change to project root directory
cd /home/ci-user/work_space/0203_issue161/cocotb_utils

echo "Current directory: $(pwd)"

echo "Step 1: Testing GL netlist with SDF annotation..."
echo "Command: python3 scripts/run_cocotb_task.py --config tests/setup_dv/benchmarks/checkin/test_benchmark_data/config.yaml --setup --sdf_annotation --netlist_type gl --task=sdf_gate_level_test"

python3 scripts/run_cocotb_task.py --config tests/setup_dv/benchmarks/checkin/test_benchmark_data/config.yaml --setup --sdf_annotation --netlist_type gl --task=sdf_gate_level_test

if [ $? -eq 0 ]; then
    echo "✓ GL netlist test completed successfully"
    # Check if GL SDF file was linked properly
    if [ -f "./tests/setup_dv/benchmarks/checkin/test_benchmark_data/test_data/gate_level_netlist.sdf" ]; then
        echo "✓ GL SDF file linked correctly"
    else
        echo "✗ Warning: GL SDF file not found"
    fi
else
    echo "✗ GL netlist test failed"
fi

# Clean up for next test
rm -rf sdf_test_env

echo ""
echo "Step 2: Testing PL netlist with SDF annotation..."
echo "Command: python3 scripts/run_cocotb_task.py --config tests/setup_dv/benchmarks/checkin/test_benchmark_data/config.yaml --setup --sdf_annotation --netlist_type pl --task=sdf_gate_level_test"

python3 scripts/run_cocotb_task.py --config tests/setup_dv/benchmarks/checkin/test_benchmark_data/config.yaml --setup --sdf_annotation --netlist_type pl --task=sdf_gate_level_test

if [ $? -eq 0 ]; then
    echo "✓ PL netlist test completed successfully"
    # Check if PL SDF file was linked properly
    if [ -f "./tests/setup_dv/benchmarks/checkin/test_benchmark_data/test_data/post_layout_netlist.sdf" ]; then
        echo "✓ PL SDF file linked correctly"
    else
        echo "✗ Warning: PL SDF file not found"
    fi
else
    echo "✗ PL netlist test failed"
fi

echo ""
echo "==================================================="
echo "SDF Annotation Test Completed"
echo "==================================================="


echo "Test Results Summary:"
echo "- The SDF annotation functionality should correctly link SDF files"
echo "- When --netlist_type gl is specified, gl_sdf files should be processed"
echo "- When --netlist_type pl is specified, pl_sdf files should be processed"
echo "- The --sdf_annotation flag enables SDF file usage in simulations"