from pyuvm import uvm_sequence_item


class ArbiterSeqItem(uvm_sequence_item):

    def __init__(self, name="ArbiterSeqItem"):
        super().__init__(name)

        self.req = 0
        self.data0 = 0
        self.data1 = 0

        # DUT outputs captured by monitor
        self.gnt = 0
        self.bus_out = 0

    def __str__(self):
        return (
            f"req={self.req:02b}, "
            f"data0=0x{self.data0:02X}, "
            f"data1=0x{self.data1:02X}, "
            f"gnt={self.gnt:02b}, "
            f"bus_out=0x{self.bus_out:02X}"
        )
