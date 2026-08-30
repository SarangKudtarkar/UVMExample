import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer


@cocotb.test()
async def arbiter_basic_test(dut):

    # Start clock
    cocotb.start_soon(
        Clock(dut.clk, 10, unit="ns").start()
    )

    # --------------------------------
    # Reset
    # --------------------------------
    dut.rst.value = 1
    dut.req.value = 0
    dut.data0.value = 0
    dut.data1.value = 0

    await RisingEdge(dut.clk)
    await ReadOnly()

    # Wait until we are allowed to drive again
    await Timer(1, unit="ns")

    # Release reset
    dut.rst.value = 0

    # --------------------------------
    # Test 1: No request
    # --------------------------------
    dut.req.value = 0

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.gnt.value == 0
    assert dut.bus_out.value == 0

    await Timer(1, unit="ns")

    # --------------------------------
    # Test 2: User 0 requests
    # --------------------------------
    dut.req.value = 1
    dut.data0.value = 0xAA
    dut.data1.value = 0x55

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.gnt.value == 1
    assert dut.bus_out.value == 0xAA

    await Timer(1, unit="ns")

    # --------------------------------
    # Test 3: User 1 requests
    # --------------------------------
    dut.req.value = 2
    dut.data0.value = 0xAA
    dut.data1.value = 0x55

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.gnt.value == 2
    assert dut.bus_out.value == 0x55

    await Timer(1, unit="ns")

    # --------------------------------
    # Test 4: Both users request
    # --------------------------------
    dut.req.value = 3
    dut.data0.value = 0xA5
    dut.data1.value = 0x5A

    await RisingEdge(dut.clk)
    await ReadOnly()

    # User 0 has priority
    assert dut.gnt.value == 1
    assert dut.bus_out.value == 0xA5
