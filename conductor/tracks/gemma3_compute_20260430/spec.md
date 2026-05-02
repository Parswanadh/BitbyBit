# Track Specification: Gemma-3 SOTA Compute Blocks

## Objective
Implement the compute core of Gemma-3 270M (RMSNorm, RoPE, Gated MLP) while actively weaponizing BitbyBit's "Unfair Advantages" (Ternary Math, Variable Precision ALUs, Zero-Skip Sparsity). The goal is to produce mathematically perfect, cycle-accurate Verilog blocks that verifiably crush traditional GPU throughput/energy metrics.

## Functional Requirements (Exploiting Unfair Advantages)
1. **Variable-Precision RMSNorm (`rmsnorm_vp.v`):**
    - **Advantage Used:** Variable Precision ALUs.
    - **Action:** Dynamically scale internal accumulation width based on the layer depth to save power, using a single-cycle 256-entry reciprocal-sqrt LUT.
2. **Dual-Lane Asymmetrical Gated MLP (`gated_mlp_da.v`):**
    - **Advantage Used:** Ternary Engine & Zero-Skip Sparsity.
    - **Action:** The "Gate" lane must be purely ternary (1.58-bit) without standard multipliers, featuring gate-level zero-skip clock gating to shut down power instantly on sparse activations. The "Up" lane uses INT8. Both run simultaneously via the new elastic memory controller.
3. **Hardware-Native RoPE Unit (`rope_unit_v2.v`):**
    - **Advantage Used:** High-Performance Memory Subsystem.
    - **Action:** Read sine/cosine parameters simultaneously from the Dual-Port LUTs established in Track 1 to perform Query/Key rotation in parallel.

## Acceptance Criteria: The "GPT-2 Parity Standard"
- **Golden Model Equivalence:** We must generate Python testing scripts (`gemma3_golden_models.py`) that produce deterministic test vectors (inputs/expected outputs) for each specific block.
- **Perfect Validation Loop:** Automated PowerShell scripts must compile the Verilog, run the testbenches against the Python vectors, and report `0` regressions and `<1% MSE` precision error.