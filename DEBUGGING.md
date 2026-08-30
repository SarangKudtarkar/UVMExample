# Debugging Guide

## Error 1 — Driver Stuck at `waiting for clock`

**Problem:** The driver waited for a clock edge, but the clock was not running correctly in the testbench flow.
**Fix:** Start `Clock(dut.clk, 10, unit="ns")` using `cocotb.start_soon()` before driving transactions.
**Result:** Driver progressed through all sequence items and the simulation reached 30–40 ns successfully.

## Error 2 — `Attempting settings a value during the ReadOnly phase`

**Problem:** `dut.rst.value = 0` was executed immediately after `await ReadOnly()`, when Cocotb prevented signal writes.
**Fix:** Move signal assignments to a writable simulation phase, using `Timer()`/`RisingEdge()` before driving signals.
**Result:** Reset and subsequent stimulus could be driven without a Cocotb runtime exception.

## Error 3 — `uvm_analysis_export object has no attribute 'connect'`

**Problem:** The scoreboard incorrectly attempted to call `.connect()` on its `uvm_analysis_export`.
**Fix:** In pyUVM, connect the monitor's `uvm_analysis_port` to the scoreboard export: `monitor.ap.connect(scoreboard.analysis_export)`.
**Result:** The analysis TLM connection was created in the environment's `connect_phase()`.

## Error 4 — `analysis_export must implement 'write()'`

**Problem:** The analysis export was connected to a scoreboard object that did not provide the required `write()` interface.
**Fix:** Add `write(self, item)` to the scoreboard so it can receive transactions from the analysis port.
**Result:** The scoreboard successfully received and printed monitored transactions.

## Error 5 — `scoreboard must be a subclass of uvm_export_base`

**Problem:** The monitor's analysis port was connected directly to the scoreboard component instead of its analysis export.
**Fix:** Create `uvm_analysis_export("analysis_export", self)` inside the scoreboard and connect the port to that export.
**Result:** pyUVM accepted the TLM connection and simulation proceeded into the run phase.

## Error 6 — Scoreboard reported incorrect GNT/BUS values

**Problem:** The monitor sampled signals before the sequential DUT outputs had updated after the clock edge.
**Fix:** Sample the DUT after the clock/update phase so `gnt` and `bus_out` represent the current transaction.
**Result:** Expected values matched the RTL: `00→00`, `01→01/AA`, `10→10/55`, and `11→01/A5`.

## Error 7 — Scoreboard appeared to validate the previous transaction

**Problem:** The monitor observed stale registered outputs because `gnt` is updated with a nonblocking assignment at the clock edge.
**Fix:** Add an appropriate Cocotb scheduling delay after `RisingEdge()` before reading DUT outputs.
**Result:** Monitor and scoreboard observed the updated grant and bus values correctly.

## Final Verification

**Result:** `Checks : 5`, `Errors : 0`, `RESULT : PASS`.
**Cocotb:** `TESTS=1 PASS=1 FAIL=0`, with a simulation time of approximately `41 ns`.
**Status:** The pyUVM + Cocotb + Icarus Verilog testbench is working correctly.
