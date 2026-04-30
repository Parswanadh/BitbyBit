# Product Guidelines: BitbyBit Tri-Fold Prototype

## Overview
This document defines the presentation style, technical rigor, and communication guidelines for the BitbyBit showcase prototype. The goal is to project raw engineering depth while ensuring absolute reproducibility for a technical audience (e.g., investors, top-tier engineering hiring managers, and open-source contributors).

## 1. Documentation & Prose Style
*   **Deep-Tech & Academic Tone:** The primary voice is authoritative, objective, and mathematically rigorous. We do not use marketing fluff; we use data.
*   **Cycle-Accurate Focus:** Claims of performance (e.g., "112 Cycles Imprint Latency") must be backed by verifiable cycle-accurate timing diagrams and simulation reports.
*   **Mathematical Foundations:** Explanations of the 5 Major Breakthroughs (Sparsity, Ternary Quantization, Tiled FlashAttention, Online Softmax, Paged KV Cache) must include the underlying equations and hardware implementation logic.
*   **Continuous Tracking (`progress.md`):** A `docs/progress.md` file must be meticulously maintained. Every decision, script generated, and Verilog modification must be documented step-by-step. This acts as a living engineering log.

## 2. Code & Developer Experience (DX)
*   **Reproducibility is Paramount:** Every claim made in the frontend showcase or architecture whitepaper must be reproducible locally by the reviewer.
*   **Comprehensive 'How-To':** The project must maintain clear, copy-pasteable commands for running Icarus Verilog simulations (`iverilog`), generating deterministic Python golden weights, and running the Next.js frontend.
*   **Self-Documenting Code:** Verilog and Python code should be heavily commented, explaining *why* a specific architectural choice was made (e.g., "Using a 256-entry exp LUT here to avoid 5-bucket step function inaccuracies").

## 3. Frontend Showcase Experience (Next.js/Three.js)
*   **Interactive but Authentic:** The visual representation of the GPU die synthesis should directly map to the actual Verilog module structures. Do not fake data flows.
*   **Live Metrics:** The showcase should expose real-time simulated metrics (Throughput, Bottlenecks, Memory Bandwidth) directly to the user interface.
*   **Deep-Dive Tooltips:** High-level visual components should allow the user to click or hover to see the underlying academic rationale or the specific Verilog file responsible for that block.

## 4. Hardware Expansion (Gemma-3 270M)
*   **SOTA Alignment:** The addition of Gemma-3 270M support must be documented as a proof-point of the architecture's scalability and relevance to modern (2025/2026) LLM standards.
*   **Quantization Transparency:** The methodology for converting Gemma-3 weights to the supported Ternary or Q8.8 formats must be explicitly detailed in the developer guides.