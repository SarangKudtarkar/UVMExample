from pyuvm import uvm_env

from tb.arbiter_agent import ArbiterAgent
from tb.arbiter_monitor import ArbiterMonitor
from tb.arbiter_scoreboard import ArbiterScoreboard


class ArbiterEnv(uvm_env):

    def __init__(self, name="ArbiterEnv", parent=None):
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()

        self.agent = ArbiterAgent(
            "agent",
            self
        )

        self.monitor = ArbiterMonitor(
            "monitor",
            self
        )

        self.scoreboard = ArbiterScoreboard(
            "scoreboard",
            self
        )

    def connect_phase(self):
        super().connect_phase()

        self.monitor.ap.connect(
            self.scoreboard.analysis_export
        )

