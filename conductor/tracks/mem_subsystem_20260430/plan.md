# Execution Plan: Formal Verification & SRAM Scaling (Ultra-Granular)

## Phase 1: Research, Blueprinting & Formal Setup (4 Tasks)
- [x] Task: Research - Define the 128-banked tiling strategy for 20MB SRAM and crossbar interconnect architecture.
- [x] Task: Research - Draft formal specifications for the `skid_buffer` deadlock-free handshakes using SystemVerilog Assertions (SVA).
- [x] Task: Formal Setup - Configure the Formal Verification environment (e.g., SymbiYosys) to run against `skid_buffer.v`.
- [x] Task: Debate - Phase-Gated Debate: Approve architectural feasibility of banked SRAM vs. latency requirements.

## Phase 2: Formalization & Primitive Refactor (6 Tasks)
- [ ] Task: Formal - Implement SVA properties for `skid_buffer` liveness and safety.
- [ ] Task: Formal - Run formal proof to confirm zero-deadlock state space.
- [ ] Task: RTL - Refactor `scratchpad.v` into `tiled_sram_bank_128.v` (128 banks of 160KB).
- [ ] Task: RTL - Implement the Crossbar Interconnect `bank_arbiter.v` to manage bank conflicts.
- [ ] Task: Validation - Create a Randomized Conflict Testbench (`tb/memory/bank_arbiter_tb.v`).
- [ ] Task: Debate - Phase-Gated Debate: Evaluate deadlock proof results and arbitration latency.

## Phase 3: Controller & Arbitration Logic (6 Tasks)
- [ ] Task: RTL - Implement the Bank-Conflict Detector logic inside the `mem_controller`.
- [ ] Task: RTL - Implement the multi-banked read/write logic for mixed-precision fetching.
- [ ] Task: Validation - Develop `scripts/verify_banked_sram.ps1` to automate conflict testing with 1000+ randomized transaction sequences.
- [ ] Task: Integration - Hook the new `mem_controller` to the `gated_mlp_da` and `rmsnorm_vp` modules.
- [ ] Task: Validation - Run full system regression to ensure 0 structural hazards during peak bank load.
- [ ] Task: Debate - Phase-Gated Debate: Verification of arbitration and conflict detection efficiency.

## Phase 4: Full SoC Integration & Stress Testing (6 Tasks)
- [ ] Task: RTL - Final SoC integration of the banked SRAM and arbiter into `gpu_system_top_v2.v`.
- [ ] Task: RTL - Update AXI-Lite command registers to expose bank-level performance counters (stalls per bank).
- [ ] Task: Validation - Launch "Stress-Load" Test Swarm: Run 5000+ cycles of concurrent read/write transactions between different compute units.
- [ ] Task: Performance - Verify system throughput maintains 2.67M Tokens/sec under heavy bank contention.
- [ ] Task: Validation - Achieve 100% PASS for randomized "Perfect Validation" loop.
- [ ] Task: Debate - Phase-Gated Debate: Performance evaluation under memory contention.

## Phase 5: Synthesis, Benchmarking & SOTA Claims (4 Tasks)
- [ ] Task: Synthesis - Generate area/power reports for the 20MB SRAM macro.
- [ ] Task: Analysis - Finalize `PERFORMANCE_CLAIMS_REPORT.md` with physical synthesis area metrics.
- [ ] Task: SOTA Alignment - Draft final research report proving BitbyBit's advantage over standard HBM-reliant GPU architectures.
- [ ] Task: Debate - Final Alignment Debate & Track Synthesis.
