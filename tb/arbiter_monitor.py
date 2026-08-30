from pyuvm import uvm_monitor, ConfigDB, uvm_analysis_port
from cocotb.triggers import RisingEdge, ReadOnly


class ArbiterMonitor(uvm_monitor):

    def __init__(self, name="ArbiterMonitor", parent=None):
        super().__init__(name, parent)

        self.ap = uvm_analysis_port("ap", self)

    def build_phase(self):
        super().build_phase()

        self.dut = ConfigDB().get(
            self,
            "",
            "dut"
        )

    async def run_phase(self):

        while True:

            # Wait for the clock edge
            await RisingEdge(self.dut.clk)

            # Wait until all signal updates are visible
            await ReadOnly()

            item = type("ArbiterMonitorItem", (), {})()

            item.req = int(self.dut.req.value)
            item.data0 = int(self.dut.data0.value)
            item.data1 = int(self.dut.data1.value)
            item.gnt = int(self.dut.gnt.value)
            item.bus_out = int(self.dut.bus_out.value)

            print(
                f">>> MONITOR: "
                f"req={item.req:02b}, "
                f"data0=0x{item.data0:02X}, "
                f"data1=0x{item.data1:02X}, "
                f"gnt={item.gnt:02b}, "
                f"bus_out=0x{item.bus_out:02X}"
            )

            self.ap.write(item)
