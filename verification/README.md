# Verification Environment

This directory contains the comprehensive verification environment for the BitbyBit Custom GPU project.

## Directory Structure

- `golden_models/` - Bit-exact Python golden models for RTL modules
- `testbenches/` - Testbenches comparing RTL output with golden models
- `random_tests/` - Constrained random test generation
- `timing_analysis/` - Static timing analysis scripts
- `regressions/` - Regression test suites
- `coverage/` - Coverage collection and reporting
- `ci/` - Continuous integration configuration

## Getting Started

### Prerequisites

- Python 3.8+
- Icarus Verilog (for RTL simulation)
- Git

### Running Tests

To run the activation compressor testbench:

```bash
cd verification/testbenches
python activation_compressor_tb_simple.py
```

To run the MAC unit testbench:

```bash
cd verification/testbenches
python mac_unit_tb_simple.py
```

## Test Results

Both testbenches should report "ALL TESTS PASSED" if the golden models match the RTL simulation.

## Adding New Modules

1. Create a golden model in `verification/golden_models/`
2. Create a testbench in `verification/testbenches/`
3. Add the testbench to the regression suite in `verification/regressions/`