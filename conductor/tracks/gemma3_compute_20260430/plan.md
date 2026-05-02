# Execution Plan: Gemma-3 SOTA Compute Blocks

## Phase 1: Parallel Research & Golden Model Generation
- [x] Task: Agent 1 (Python) - Research and write `scripts/gemma3_rmsnorm_golden.py` to generate precise test vectors (Q8.8) for RMSNorm verification.
- [x] Task: Agent 2 (Python) - Research and write `scripts/gemma3_rope_golden.py` to generate interleaved Query/Key rotation vectors.
- [x] Task: Agent 3 (Python) - Research and write `scripts/gemma3_gated_mlp_golden.py` focusing on Ternary Gate and INT8 Up projections.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Parallel Research & Golden Model Generation' (Protocol in workflow.md)

## Phase 2: Parallel SOTA RTL Implementation
- [x] Task: Agent 1 (RTL) - Implement `rmsnorm_vp.v` and its testbench, maximizing the use of Variable Precision ALUs.
- [x] Task: Agent 2 (RTL) - Implement `rope_unit_v2.v` and its testbench, hooking directly into the Dual-Port LUT primitives.
- [x] Task: Agent 3 (RTL) - Implement `gated_mlp_da.v` and its testbench, aggressively applying Ternary multiplexers and Zero-Skip clock gating logic.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Parallel SOTA RTL Implementation' (Protocol in workflow.md)

## Phase 3: Automated Validation & Testing Loops
- [ ] Task: Agent 1 (Validation) - Create `scripts/verify_gemma3_blocks.ps1`. This script must run all testbenches, compare outputs to the Python golden vectors, and enforce "Perfect Validation" (PASS/FAIL).
- [ ] Task: Validation - Run the script and iterate on the RTL code until all three modules achieve a 100% PASS rate against the golden models.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Automated Validation & Testing Loops' (Protocol in workflow.md)

## Phase 4: SOTA Benchmarking & Advantage Proof
- [ ] Task: Performance Agent - Analyze the cycle counts from the `gated_mlp_da_tb.v` and calculate the energy saved strictly due to the Ternary logic and Zero-Skip sparsity vs standard FP16 logic.
- [ ] Task: Output Agent - Append these findings to `CLAIMABLE_OUTPUTS_STRATEGY.md` with verifiable data.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: SOTA Benchmarking & Advantage Proof' (Protocol in workflow.md)

## Phase 5: Final Alignment Debate & Synthesis
- [ ] Task: Swarm Consensus - Conduct a formal Phase-Gated debate ensuring the Gemma-3 blocks meet the "Best in the World" criteria before full SoC integration.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Alignment Debate & Synthesis' (Protocol in workflow.md)