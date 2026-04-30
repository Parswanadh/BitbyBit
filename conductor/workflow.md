# Project Workflow: BitbyBit Tri-Fold Prototype

## Overview
This document outlines the strict development workflow for the BitbyBit showcase prototype. Given the ambitious goal of parallel hardware and software development, this workflow enforces a highly specialized, multi-agent evaluation protocol.

## Core Principles
1.  **Parallel Execution:** Sub-tasks within a phase should be delegated to specialized sub-agents (e.g., `generalist` for Next.js, a code analyzer for RTL) whenever possible to maximize velocity.
2.  **Continuous Documentation:** Every architectural decision, executed script, and file modification MUST be appended to `docs/progress.md` as an ongoing engineering log.
3.  **Verified Commits:** Code must be verified via simulation (`iverilog` for RTL) or tests (Next.js/Python) before committing.
4.  **Test Coverage:** Minimum 80% coverage for new modules.

## Multi-Agent Debate & Alignment Protocol

To ensure the "Highest SOTA Position" is maintained across all three parallel domains (RTL, Frontend, Gemma-3), we enforce a two-tier debate system:

### 1. Strict Autonomous Debates (Continuous)
*   **Trigger:** Active continuously during the execution of tasks.
*   **Action:** When a sub-agent is investigating a problem or proposing a design, it should autonomously consider alternative approaches (internal debate) in the background.
*   **Logging:** These micro-debates are NOT logged unless a critical architectural conflict or a divergence from the SOTA goal is detected. If a conflict occurs, the agent must immediately pause and prompt the user.

### 2. Phase-Gated Debates (Mandatory Checkpoints)
*   **Trigger:** Mandatory at the end of every Phase defined in a track's `plan.md`.
*   **Action:** The primary orchestrator agent MUST halt execution and initiate a formal evaluation of the phase's output. The agent will analyze the integrated progress across all parallel domains against the goals set in `product-guidelines.md`.
*   **Logging:** The outcome and summary of this formal Phase-Gated Debate MUST be appended to a dedicated `docs/debates/` folder and summarized in `docs/progress.md` before the next phase is allowed to begin.

## Phase Completion Verification and Checkpointing Protocol
At the end of every phase, after the Phase-Gated Debate is completed and logged, the orchestrator must verify that all artifacts are committed, the progress log is updated, and the project remains stable before proceeding to the next set of tasks.