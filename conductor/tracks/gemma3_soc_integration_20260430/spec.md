# Track Specification: Gemma-3 Full SoC Integration

## Objective
Unify the verified compute modules (RMSNorm, RoPE, Gated MLP, Mixed Memory Controller) into the `gpu_system_top_v2.v` SoC wrapper. This track aims to enable full-system execution of Gemma-3 270M, achieving our 2.67M Tokens/sec throughput at the system level.

## Functional Requirements
1. **Top-Level Wrapper Refactor:** Instantiation of verified modules into `gpu_system_top_v2.v`.
2. **Instruction Set Expansion:** Extend `command_processor.v` opcodes to map onto the new Gemma-3 compute units.
3. **Data Path Routing:** Ensure the `mem_controller_mixed` correctly feeds all three compute modules through the elastic pipeline.
4. **Full-Stack Visualization:** Wire the real-time hardware status of these modules to the Next.js `GemmaExecutionFlow` UI components.

## Acceptance Criteria
- **Simulation:** Full system-level simulation (`nanogpt_q4_tb.v` extended to support Gemma-3 ops) must pass with 0 regressions.
- **Integration:** The 3D UI must reflect accurate, live status of the integrated compute blocks during inference.
- **Parity:** Mathematical output for full-layer inference must stay within <1% MSE of the Python golden reference.
