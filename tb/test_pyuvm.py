import cocotb
from cocotb.clock import Clock

from pyuvm import uvm_root

from tb.arbiter_test import ArbiterTest


@cocotb.test()
async def pyuvm_arbiter_test(dut):

    print("\n========== START pyUVM TEST ==========")
    print(f"DUT = {dut}")

    # Start DUT clock
    cocotb.start_soon(
        Clock(dut.clk, 10, unit="ns").start()
    )

    # Pass DUT handle to the pyUVM test
    ArbiterTest.dut = dut

    print(f"ArbiterTest.dut = {ArbiterTest.dut}")

    await uvm_root().run_test(
        "ArbiterTest"
    )
