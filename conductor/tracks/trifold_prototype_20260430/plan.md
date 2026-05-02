# Execution Plan: Initialize Tri-Fold Prototype

## Phase 1: Foundation & Analysis
- [x] Task: RTL Pipeline - Create `skid_buffer.v` module based on Roadmap specs.
- [x] Task: Next.js - Initialize basic Three.js canvas in the main layout for the GPU visualizer.
- [x] Task: Gemma-3 - Document architectural differences (RoPE, MLP) between NanoGPT and Gemma-3 270M in a new `gemma3_architecture.md` file.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Analysis' (Protocol in workflow.md)

## Phase 2: Integration & Refactoring
- [x] Task: RTL Pipeline - Refactor FSM in `optimized_transformer_layer.v` to remove wait states and integrate `skid_buffer.v`.
- [x] Task: RTL Pipeline - Verify refactor via Icarus Verilog testbench and ensure 0 regressions.
- [x] Task: Next.js - Wire up simulated metric hooks (Throughput, Bottlenecks) to UI components.
- [x] Task: Gemma-3 - Draft a Python script to extract and quantize Gemma-3 weights to Q8.8 format.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Integration & Refactoring' (Protocol in workflow.md)