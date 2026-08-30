# pyUVM Arbiter Verification Example

A complete **Python-based UVM-style verification environment** for a simple Verilog arbiter using:

* **pyUVM**
* **cocotb 2.x**
* **Icarus Verilog**
* **Python 3**
* **Make**

The project demonstrates how to build a structured UVM verification environment in Python, including transactions, sequences, sequencers, drivers, monitors, analysis ports, scoreboards, environments, tests, objections, ConfigDB, TLM connections, reset handling, and clock synchronization.

---

# 📌 1. Project Overview

The Design Under Test (DUT) is a simple 2-user arbiter.

The arbiter:

* Accepts requests from two users.
* Gives **User 0 priority** when both users request simultaneously.
* Generates a one-hot grant signal.
* Routes the selected user's data onto a shared bus.
* Clears the grant when there are no requests.
* Uses synchronous reset.

### Arbitration Rules

| `req` | Expected `gnt` | Expected `bus_out` |
| ----- | -------------- | ------------------ |
| `00`  | `00`           | `0x00`             |
| `01`  | `01`           | `data0`            |
| `10`  | `10`           | `data1`            |
| `11`  | `01`           | `data0`            |

When both users request simultaneously (`req = 11`), **User 0 wins**.

---

# 🚀 2. Quick Start

If the required tools are already installed:

```bash
git clone <YOUR_REPOSITORY_URL>
cd UVMExample

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

make
```

A successful run should finish with:

```text
========================================
       ARBITER SCOREBOARD REPORT
========================================
Checks : 5
Errors : 0
RESULT : PASS
========================================

TESTS=1 PASS=1 FAIL=0
```

---

# 🛠️ 3. Prerequisites

Before running the project, install the following tools.

## Python

Python 3.10+ is recommended.

Check your version:

```bash
python3 --version
```

Example:

```text
Python 3.12.x
```

---

## Icarus Verilog

Check whether Icarus Verilog is installed:

```bash
iverilog -V
```

The project was tested with:

```text
Icarus Verilog 12.0
```

### Ubuntu / Debian / WSL

Install using:

```bash
sudo apt update
sudo apt install iverilog
```

Verify:

```bash
iverilog -V
```

---

## Make

Check:

```bash
make --version
```

Install if necessary:

```bash
sudo apt install make
```

---

# 🐍 4. Create the Python Virtual Environment

It is recommended to use a virtual environment so that Python dependencies do not interfere with system packages.

From the repository root:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

You should see something similar to:

```text
(.venv) user@machine:~/UVMExample$
```

---

# 📦 5. Install Python Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

The project requires at least:

```text
cocotb
pyuvm
```

You can verify the installation:

```bash
python -c "import cocotb; print('cocotb:', cocotb.__version__)"
```

and:

```bash
python -c "import pyuvm; print('pyUVM installed successfully')"
```

---

# 📋 6. Create `requirements.txt`

If the repository does not already contain one, create it with:

```bash
cat > requirements.txt <<'EOF'
cocotb>=2.0,<3.0
pyuvm>=4.0,<5.0
EOF
```

Then install:

```bash
pip install -r requirements.txt
```

---

# 📁 7. Repository Structure

The recommended repository structure is:

```text
UVMExample/
│
├── README.md
├── UVM_CONCEPTS_README.md
├── UVM_ERRORS_AND_FIXES.md
├── Makefile
├── requirements.txt
│
├── src/
│   └── arbiter.v
│
├── tb/
│   ├── test_pyuvm.py
│   ├── arbiter_test.py
│   ├── arbiter_env.py
│   ├── arbiter_agent.py
│   ├── arbiter_driver.py
│   ├── arbiter_monitor.py
│   ├── arbiter_sequence.py
│   ├── arbiter_transaction.py
│   └── arbiter_scoreboard.py
│
└── .gitignore
```

Generated files such as `sim_build/`, `results.xml`, Python cache files, and the virtual environment should not be committed.

---

# ▶️ 8. Run the Verification

From the repository root:

```bash
make
```

The Makefile:

1. Compiles the Verilog DUT.
2. Builds the simulator executable.
3. Starts Icarus Verilog.
4. Loads cocotb.
5. Starts the pyUVM test.
6. Generates transactions.
7. Drives the DUT.
8. Monitors DUT activity.
9. Sends observed transactions to the scoreboard.
10. Checks expected versus actual behavior.
11. Reports the final verification result.

---

# 🧹 9. Clean the Simulation

To remove generated simulation files:

```bash
make clean
```

If the Makefile does not provide a clean target, manually remove generated files:

```bash
rm -rf sim_build results.xml
```

Then rerun:

```bash
make
```

---

# 🔍 10. Expected Verification Flow

The test exercises the following request patterns:

```text
req = 00
req = 01
req = 10
req = 11
```

The verification architecture processes each transaction through:

```text
Sequence
   ↓
Sequencer
   ↓
Driver
   ↓
DUT
   ↓
Monitor
   ↓
Analysis Port
   ↓
Scoreboard
   ↓
PASS / FAIL
```

---

# 🧪 11. Test Cases

## Test 1 — No Request

```text
req = 00
```

Expected:

```text
gnt     = 00
bus_out = 00
```

---

## Test 2 — User 0 Request

```text
req   = 01
data0 = AA
data1 = 55
```

Expected:

```text
gnt     = 01
bus_out = AA
```

---

## Test 3 — User 1 Request

```text
req   = 10
data0 = AA
data1 = 55
```

Expected:

```text
gnt     = 10
bus_out = 55
```

---

## Test 4 — Both Users Request

```text
req   = 11
data0 = A5
data1 = 5A
```

Expected:

```text
gnt     = 01
bus_out = A5
```

User 0 wins because it has priority.

---

# 🏗️ 12. Verification Architecture

```text
                    ┌─────────────────────┐
                    │     ArbiterTest     │
                    │      uvm_test       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ArbiterEnv      │
                    │      uvm_env        │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
              ┌───────────┐        ┌─────────────┐
              │   Agent   │        │ Scoreboard  │
              └─────┬─────┘        └──────▲──────┘
                    │                     │
          ┌─────────┼─────────┐           │
          │         │         │           │
          ▼         ▼         ▼           │
     ┌────────┐ ┌─────────┐ ┌─────────┐   │
     │Sequence│ │Sequencer│ │ Driver  │   │
     └────────┘ └─────────┘ └────┬────┘   │
                                  │        │
                                  ▼        │
                              ┌───────┐    │
                              │  DUT  │    │
                              └───┬───┘    │
                                  │        │
                                  ▼        │
                              ┌────────┐   │
                              │Monitor │───┘
                              └────────┘
```

---

# 🧩 13. UVM Concepts Covered

## UVM Test

`uvm_test` is responsible for controlling the verification scenario.

Demonstrated concepts:

* Test creation
* Environment creation
* ConfigDB setup
* Sequence execution
* Objection management

---

## UVM Environment

`uvm_env` provides the container for the verification components.

```text
ArbiterEnv
├── Agent
└── Scoreboard
```

---

## UVM Agent

The agent groups the DUT communication components:

```text
ArbiterAgent
├── Sequencer
├── Driver
└── Monitor
```

---

## Sequence Item / Transaction

The transaction represents one arbiter operation.

It contains:

```text
req
data0
data1
gnt
bus_out
```

Input fields:

```text
req
data0
data1
```

Output/observed fields:

```text
gnt
bus_out
```

---

## Sequence

The sequence generates stimulus transactions.

The current test exercises all four request combinations:

```text
00
01
10
11
```

---

## Sequencer

The sequencer transfers transactions from the sequence to the driver.

```text
Sequence
   ↓
Sequencer
   ↓
Driver
```

---

## Driver

The driver converts transactions into DUT signal activity.

It:

1. Receives a transaction.
2. Drives DUT inputs.
3. Waits for the clock.
4. Completes the transaction.

The driver uses:

```python
item_done()
```

to indicate completion.

---

## Monitor

The monitor is passive.

It:

* Samples DUT signals.
* Creates observed transactions.
* Sends them to the scoreboard.

```text
DUT
 ↓
Monitor
 ↓
Analysis Port
 ↓
Scoreboard
```

---

## Analysis Port

The monitor publishes transactions using:

```python
uvm_analysis_port
```

This allows observed transactions to be broadcast to analysis components.

---

## Analysis Export

The scoreboard exposes:

```python
uvm_analysis_export
```

and implements:

```python
def write(self, item):
    ...
```

The monitor connects its analysis port to this export.

---

## TLM Connection

The monitor and scoreboard communicate using a UVM Transaction-Level Modeling connection.

Conceptually:

```python
self.monitor.ap.connect(
    self.scoreboard.analysis_export
)
```

---

## Scoreboard

The scoreboard independently calculates the expected result and compares it against the DUT output.

For example:

```text
req = 11

Expected:
gnt     = 01
bus_out = A5

Actual:
gnt     = 01
bus_out = A5

PASS
```

---

## Reference Model

The scoreboard contains the expected arbitration behavior:

```text
if req[0]:
    gnt = 01
else if req[1]:
    gnt = 10
else:
    gnt = 00
```

The expected bus value follows the grant.

---

## UVM Phases

The project demonstrates:

### `build_phase`

Creates and configures components.

### `connect_phase`

Connects TLM interfaces.

### `run_phase`

Performs time-consuming simulation activities.

---

## UVM Objections

The test uses objections to keep the run phase alive while the sequence executes.

Conceptually:

```text
raise objection
       ↓
run sequence
       ↓
drop objection
```

---

## ConfigDB

ConfigDB is used to make the DUT handle available to lower-level components.

Conceptually:

```text
Test
 ↓
ConfigDB
 ↓
Driver / Environment
 ↓
DUT
```

This avoids unnecessary direct coupling between components.

---

## Reset Handling

The test drives reset before normal operation.

The reset state is verified:

```text
gnt     = 00
bus_out = 00
```

---

## Clock Synchronization

The DUT updates its grant on:

```verilog
posedge clk
```

The driver therefore synchronizes transactions with:

```python
await RisingEdge(dut.clk)
```

---

## Directed Testing

The test explicitly covers:

```text
00
01
10
11
```

This verifies:

* No requester
* User 0 requester
* User 1 requester
* Simultaneous request
* Priority behavior

---

# 🐛 14. Debugging Lessons

During development, several issues were encountered and resolved.

Important lessons include:

### Cocotb ReadOnly Error

Attempting to modify DUT signals after entering the `ReadOnly` phase caused:

```text
RuntimeError:
Attempting settings a value during the ReadOnly phase.
```

The fix was to perform signal assignments during a writable simulation phase rather than immediately after `ReadOnly`.

---

### Analysis Export Connection Error

An initial implementation attempted to call:

```python
self.analysis_export.connect(...)
```

However, the pyUVM analysis export does not provide the same connection API as an analysis port.

The correct direction is:

```text
Monitor Analysis Port
        ↓
Scoreboard Analysis Export
```

using:

```python
self.monitor.ap.connect(
    self.scoreboard.analysis_export
)
```

---

### Missing `write()` Error

The analysis export initially failed because the receiving object did not implement:

```python
write()
```

The scoreboard was corrected to provide:

```python
def write(self, item):
    ...
```

This allowed the analysis port to deliver transactions correctly.

---

### Scoreboard Timing Error

Initially, the scoreboard sampled the DUT before the registered `gnt` output had updated.

This caused errors such as:

```text
expected gnt=01
actual gnt=00
```

The monitor was corrected to sample after the appropriate clock event so that the scoreboard observes the updated DUT state.

---

### Stale Simulation Build

When RTL or testbench files change, it can sometimes be useful to remove generated simulation artifacts:

```bash
rm -rf sim_build results.xml
```

Then rebuild:

```bash
make
```

---

# 📊 15. Final Verification Result

The final test successfully checks five monitored transactions, including reset/no-request behavior and all request combinations.

Expected final report:

```text
========================================
       ARBITER SCOREBOARD REPORT
========================================
Checks : 5
Errors : 0
RESULT : PASS
========================================

TESTS=1 PASS=1 FAIL=0
```

This confirms that the DUT behavior matches the expected arbitration model.

---

# 📚 16. Detailed Documentation

Additional documentation is available in:

### UVM Concepts

See:

```text
UVM_CONCEPTS_README.md
```

for a detailed explanation of the UVM concepts demonstrated by this project.

### Errors and Fixes

See:

```text
UVM_ERRORS_AND_FIXES.md
```

for the errors encountered during development, their root causes, and the fixes applied.

---

# 🔧 17. Useful Commands

### Activate environment

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run simulation

```bash
make
```

### Clean generated files

```bash
make clean
```

or:

```bash
rm -rf sim_build results.xml
```

### Check Python

```bash
python3 --version
```

### Check Icarus Verilog

```bash
iverilog -V
```

### Check installed pyUVM

```bash
python -c "import pyuvm; print('pyUVM OK')"
```

### Check installed cocotb

```bash
python -c "import cocotb; print(cocotb.__version__)"
```

---

# 🌱 18. Future Improvements

Possible extensions include:

* Constrained-random stimulus
* Randomized data
* Random request patterns
* Functional coverage
* Additional assertions
* Multiple UVM tests
* Regression testing
* Waveform generation
* Round-robin arbitration
* Additional requesters
* Configurable arbitration policies
* More extensive reset testing
* Error injection
* Functional coverage reporting

---

# 🎯 19. Learning Objectives

After studying this project, you should understand the basic flow of a Python-based UVM verification environment:

```text
Transaction
     ↓
Sequence
     ↓
Sequencer
     ↓
Driver
     ↓
RTL DUT
     ↓
Monitor
     ↓
Analysis Port
     ↓
Scoreboard
     ↓
Expected vs Actual
     ↓
PASS / FAIL
```

The project is intended as a practical introduction to **UVM concepts using Python rather than SystemVerilog**.

---

# 📜 20. License

Add your preferred open-source license here, for example:

```text
MIT License
```

---

# ⭐ 21. Summary

This repository demonstrates a complete pyUVM verification flow for a synchronous Verilog arbiter.

It covers:

* Python-based verification
* pyUVM
* cocotb
* Icarus Verilog
* UVM test
* UVM environment
* UVM agent
* Transactions
* Sequences
* Sequencers
* Drivers
* Monitors
* Analysis ports
* Analysis exports
* TLM connections
* Scoreboards
* Reference models
* ConfigDB
* UVM phases
* Objections
* Reset
* Clock synchronization
* Directed testing
* Functional checking
* Debugging and verification methodology

Run:

```bash
make
```

and the expected result is:

```text
RESULT : PASS
TESTS=1 PASS=1 FAIL=0
```
