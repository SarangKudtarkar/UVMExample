from pyuvm import uvm_driver, ConfigDB
from cocotb.triggers import RisingEdge, Timer


class ArbiterDriver(uvm_driver):

    def __init__(self, name="ArbiterDriver", parent=None):
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()

        self.dut = ConfigDB().get(
            self,
            "",
            "dut"
        )

        print(f">>> DRIVER DUT = {self.dut}")

    async def run_phase(self):

        print(">>> DRIVER run_phase START")

        while True:

            print(">>> DRIVER waiting for item")

            item = await self.seq_item_port.get_next_item()

            print(f">>> DRIVER got item: {item}")

            # Drive BEFORE the active clock edge
            self.dut.req.value = item.req
            self.dut.data0.value = item.data0
            self.dut.data1.value = item.data1

            print(">>> DRIVER waiting for clock")

            await RisingEdge(self.dut.clk)

            # Allow sequential DUT logic/NBA updates to settle
            await Timer(1, unit="ns")

            print(">>> DRIVER item_done")

            self.seq_item_port.item_done()
