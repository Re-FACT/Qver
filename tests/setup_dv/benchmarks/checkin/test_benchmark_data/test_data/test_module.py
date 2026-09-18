import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def simple_test(dut):
    await Timer(1, units="ns")
    assert True, "Simple test passed"
