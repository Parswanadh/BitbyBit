# Track Specification: Comprehensive Swarm Verification and Planning

## Overview
This track initiates a massive parallel multi-agent swarm to analyze the current progress of the Tri-Fold Prototype (RTL, Next.js, and Gemma-3 scripts). It enforces a strict, zero-regression "perfect validation" standard before initiating a Research & Analyst Swarm to draft the optimal, full-stack roadmap via a formal debate process.

## Functional Requirements
1. **Parallel Verification Swarm (QA) with Perfect Validation:**
    - **RTL QA:** Must run all `iverilog` testbenches (including `nanogpt_q4_tb.v`). Validation is only "perfect" if output exactly matches the Python golden model and 0 timing regressions are introduced by the `skid_buffer.v`.
    - **Frontend QA:** Must execute Next.js build (`next build`), ESLint (`next lint`), and Vitest suites. Validation is only "perfect" if 0 errors or warnings are emitted and the Three.js canvas renders without WebGL context failures.
    - **Data QA:** Must run `export_gemma3_q88.py` on a stub model and calculate the quantization error (MSE). Validation is only "perfect" if the error is within the mathematically acceptable bounds for Q8.8 format.
2. **Parallel Research & Analyst Swarm:**
    - The Hardware Analyst must define the architectural blueprint for implementing new Verilog blocks (RMSNorm, RoPE, Gated MLP) required for Gemma-3.
    - The Integration Analyst must propose how the Next.js UI will interactively visualize the execution of these new blocks.
    - The Performance Analyst must identify potential bottlenecks in the proposed design to ensure the 2.67M Tokens/sec target is maintained or exceeded.
3. **Mandatory Swarm Debate System:**
    - Before finalizing the roadmap, the Research & Analyst Swarm MUST conduct a formal debate evaluating the trade-offs between Hardware Expansion complexity, UI interactivity, and Performance targets. This debate must be logged.
4. **Outcome:** A comprehensive `docs/next_best_plan.md` document synthesizing the agreed-upon roadmap.

## Acceptance Criteria
- All three QA agents must achieve their respective "perfect validation" states. If any fail, the swarm must halt and generate bug fix tickets.
- The `docs/debates/` folder must contain a formal alignment debate summarizing the swarms' strategic compromise.
- A final, actionable `next_best_plan.md` is produced, balancing Hardware Expansion, Full-Stack Integration, and Performance Optimization.