from pyuvm import uvm_scoreboard, uvm_analysis_export


class ArbiterScoreboardExport(uvm_analysis_export):

    def __init__(self, name, parent, scoreboard):
        super().__init__(name, parent)
        self.scoreboard = scoreboard

    def write(self, item):
        self.scoreboard.write(item)


class ArbiterScoreboard(uvm_scoreboard):

    def __init__(self, name="ArbiterScoreboard", parent=None):
        super().__init__(name, parent)

        self.analysis_export = ArbiterScoreboardExport(
            "analysis_export",
            self,
            self
        )

        self.check_count = 0
        self.error_count = 0

    def write(self, item):

        self.check_count += 1

        # --------------------------------
        # Calculate expected grant
        # --------------------------------
        if item.req == 0:
            expected_gnt = 0

        elif item.req & 0b01:
            # User 0 has priority
            expected_gnt = 1

        elif item.req & 0b10:
            expected_gnt = 2

        else:
            expected_gnt = 0

        # --------------------------------
        # Calculate expected bus
        # --------------------------------
        if expected_gnt == 1:
            expected_bus = item.data0

        elif expected_gnt == 2:
            expected_bus = item.data1

        else:
            expected_bus = 0

        # --------------------------------
        # Check grant
        # --------------------------------
        if item.gnt != expected_gnt:
            self.error_count += 1

            print(
                f"!!! SCOREBOARD ERROR: "
                f"req={item.req:02b}, "
                f"expected gnt={expected_gnt:02b}, "
                f"actual gnt={item.gnt:02b}"
            )

        else:
            print(
                f">>> GNT PASS: "
                f"req={item.req:02b}, "
                f"gnt={item.gnt:02b}"
            )

        # --------------------------------
        # Check bus
        # --------------------------------
        if item.bus_out != expected_bus:
            self.error_count += 1

            print(
                f"!!! SCOREBOARD ERROR: "
                f"req={item.req:02b}, "
                f"expected bus=0x{expected_bus:02X}, "
                f"actual bus=0x{item.bus_out:02X}"
            )

        else:
            print(
                f">>> BUS PASS: "
                f"req={item.req:02b}, "
                f"bus=0x{item.bus_out:02X}"
            )

    def report_phase(self):
        print("")
        print("========================================")
        print("       ARBITER SCOREBOARD REPORT")
        print("========================================")
        print(f"Checks : {self.check_count}")
        print(f"Errors : {self.error_count}")

        if self.error_count == 0:
            print("RESULT : PASS")
        else:
            print("RESULT : FAIL")

        print("========================================")
