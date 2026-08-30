import cocotb

from pyuvm import uvm_test, ConfigDB
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from tb.arbiter_env import ArbiterEnv
from tb.arbiter_sequence import ArbiterBasicSequence


class ArbiterTest(uvm_test):

    dut = None

    def __init__(self, name="ArbiterTest", parent=None):
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()

        ConfigDB().set(
            self,
            "*",
            "dut",
            ArbiterTest.dut
        )

        self.env = ArbiterEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        # Start clock
        cocotb.start_soon(
            Clock(self.dut.clk, 10, unit="ns").start()
        )

        # Reset
        self.dut.rst.value = 1
        self.dut.req.value = 0
        self.dut.data0.value = 0
        self.dut.data1.value = 0

        await RisingEdge(self.dut.clk)

        # Release reset BEFORE ReadOnly
        self.dut.rst.value = 0

        # Run sequence
        sequence = ArbiterBasicSequence("basic_sequence")

        await sequence.start(
            self.env.agent.sequencer
        )

        self.drop_objection()
