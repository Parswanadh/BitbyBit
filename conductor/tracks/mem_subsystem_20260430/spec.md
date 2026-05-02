# Track Specification: High-Performance Memory Subsystem

## Objective
To implement the foundational hardware memory infrastructure required to support advanced Gemma-3 features (RoPE, Gated MLP) while maintaining the SOTA 2.67M Tokens/sec throughput. This track focuses on creating a "fluid" datapath through elastic handshaking and mixed-precision fetching.

## Functional Requirements
1. **Asynchronous Elastic Pipeline (Skid Buffers):**
    - Implement the `skid_buffer.v` module with a robust `ready/valid` handshake protocol.
    - These buffers must be instantiated between all major compute stages (e.g., RoPE to Attention, Attention to FFN) to decouple stage latencies and eliminate global stalls.
2. **Dual-Ported Mixed-Precision LUTs:**
    - Develop `dual_port_lut.v` specifically for RoPE Sine/Cosine lookups.
    - The memory controller must support "burst-mode" mixed-precision fetching, allowing for the simultaneous loading of 4-bit, 8-bit, and 16-bit parameters in a single memory cycle.
3. **Ternary-Packed Fetching:**
    - Implement a specialized fetch logic that can "unpack" 8 ternary weights (2-bit each) from a single 16-bit memory word to maximize SRAM bandwidth.

## Acceptance Criteria
- **Simulation:** All memory unit testbenches must pass with 0 structural hazards during simultaneous read/write access.
- **Throughput:** Cycle-accurate simulation must prove that the elastic pipeline maintains the 2.67M Tokens/sec target even when introducing variable-latency math blocks.
- **Verification:** `iverilog` logs must show successful `ready/valid` handshaking under backpressure scenarios.

## Out of Scope
- Implementation of the actual Gemma-3 math blocks (RMSNorm, RoPE, etc.) occurs in the subsequent track. This track is strictly for the *memory and control infrastructure*.
