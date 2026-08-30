from pyuvm import uvm_agent

from tb.arbiter_sequencer import ArbiterSequencer
from tb.arbiter_driver import ArbiterDriver


class ArbiterAgent(uvm_agent):

    def __init__(self, name="ArbiterAgent", parent=None):
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()

        self.sequencer = ArbiterSequencer(
            "sequencer",
            self
        )

        self.driver = ArbiterDriver(
            "driver",
            self
        )

    def connect_phase(self):
        super().connect_phase()

        self.driver.seq_item_port.connect(
            self.sequencer.seq_item_export
        )
