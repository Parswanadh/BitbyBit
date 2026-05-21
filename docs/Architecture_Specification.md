# BitbyBit GPU Architecture Specification

## Overview
This document provides a detailed specification of the BitbyBit custom GPU architecture for Transformer inference. The architecture is designed from scratch in Verilog-2005 and implements all core operations needed for running Transformer models like NanoGPT and Gemma-style models at the edge.

## Key Features
- **16 Verilog modules** across 4 design layers
- **Q8.8 fixed-point** arithmetic throughout (no floating point)
- **Zero-skip optimization** — skips zero-weight multiplications for energy efficiency
- **Variable-precision ALU** — processes 4-bit, 8-bit, or 16-bit data
- **Pipelined transformer blocks** — LayerNorm → Attention → FFN with residual connections
- **AXI4-Lite command interface** for host CPU communication
- **AXI4 Master DMA engine** for off-chip memory access
- **Multi-bank Scratchpad SRAM** for low-latency intermediate storage
- **Paged KV Cache Management** for virtualized context windows

## Architecture Layers

### Layer 1 — Core Compute Primitives
The fundamental building blocks that every computation flows through:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| `zero_detect_mult.v` | Multiply with zero bypass | Skips MAC operations when either operand is zero |
| `variable_precision_alu.v` | Multi-precision ALU | 4×4-bit, 2×8-bit, or 1×16-bit parallel operations |
| `sparse_memory_ctrl.v` | CSR sparse storage | Compressed Sparse Row format for weight matrices |
| `fused_dequantizer.v` | INT4→INT8 converter | Zero-latency in-pipeline dequantization |
| `gpu_top.v` | Pipeline controller | Coordinates all 4 primitives with ready/valid handshaking |

### Layer 2 — Compute Modules
Neural-network–specific compute units built from Layer 1 primitives:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| `mac_unit.v` | Multiply-Accumulate | Dot product building block with zero-skip capability |
| `systolic_array.v` | NxN matrix multiply | Weight-stationary dataflow with zero-skip support |
| `gelu_activation.v` | GELU activation | Piecewise-linear Q8.8 approximation using LUT |
| `softmax_unit.v` | Softmax normalization | LUT-based exp with max-subtract for numerical stability |
| `exp_lut_256.v` | Exponential lookup table | 256-entry LUT for softmax computation |
| `gelu_lut_256.v` | GELU lookup table | 256-entry LUT for GELU activation |
| `inv_sqrt_lut_256.v` | Inverse square root LUT | 256-entry LUT for LayerNorm normalization |

### Layer 3 — Transformer Blocks
Complete transformer layer components:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| `layer_norm.v` | Layer normalization | Mean/variance computation with γ/β scaling |
| `linear_layer.v` | Dense matrix-vector | y = Wx + b with weight loading from SRAM |
| `attention_unit.v` | Multi-head attention | Q/K/V projections + output projection |
| `ffn_block.v` | Feed-forward network | Linear→GELU→Linear pipeline with residual connection |

### Layer 4 — System Integration
The complete inference engine with system-level components:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| `embedding_lookup.v` | Token + position embedding | Combined token and position embedding lookup |
| `transformer_block.v` | Full decoder block | LN→Attn→Residual→LN→FFN→Residual structure |
| `gpt2_engine.v` | GPT-2 inference engine | N-layer pipeline with argmax output |
| `command_processor.v` | AXI4-Lite interface | FIFO-based command queue with opcodes |
| `config_regs.v` | Configuration registers | Runtime GPU configuration via AXI4-Lite |
| `perf_counters.v` | Performance counters | 8 hardware counters (cycles, MACs, stalls, etc.) |
| `reset_sync.v` | Reset synchronizer | 2-FF reset synchronizer for safe async-to-sync |
| `dma_engine.v` | AXI4 Master DMA | Bulk weight transfers from off-chip memory |
| `kv_page_table.v` | KV page table | Virtual-to-physical mapping for KV cache |
| `stack_page_allocator.v` | Stack-based page allocator | Hardware stack for KV cache page allocation |
| `scratchpad_banked.v` | Multi-bank scratchpad | 4KB SRAM divided into 8 banks to reduce conflicts |

## Datapath Description

### Token Processing Flow
1. **Input**: Token ID and position ID from host CPU via AXI4-Lite
2. **Embedding**: Combined token and position embedding lookup (Q8.8 format)
3. **Per Layer** (N times):
   - Pre-attention Layer Normalization
   - Multi-head self-attention:
     * Q/K/V linear projections
     * Tiled FlashAttention computation (4x4 tiles)
     * Streaming online softmax
     * Weighted value aggregation
     * Output projection
   - Residual connection addition
   - Pre-FFN Layer Normalization
   - Feed-forward network:
     * First linear projection (4× expansion)
     * GELU activation
     * Second linear projection (back to model dimension)
   - Residual connection addition
4. **Output**: Final layer normalization followed by argmax to predict next token

### Memory Subsystem
- **Weight Storage**: Off-chip in external DDR memory, loaded via DMA
- **Activation Storage**: On-chip scratchpad SRAM (4KB, 8-banked)
- **KV Cache**: Virtualized via page table with physical pages in scratchpad
- **Weight Format**: INT4 with on-chip dequantization to INT8
- **Activation Format**: Q8.8 signed fixed-point throughout compute

### Control Subsystem
- **Command Processor**: Accepts opcodes from host (RESET, LOAD_WEIGHTS, RUN_INFERENCE, etc.)
- **Configuration Registers**: Set model parameters (embed_dim, num_heads, seq_len, etc.)
- **Performance Counters**: Track cycles, MAC operations, stalls, zero-skip events
- **Interrupt Generation**: Signals completion to host CPU

## Interface Specification

### AXI4-Lite Slave Interface (Control)
- **Address Width**: 32 bits
- **Data Width**: 32 bits
- **Registers**:
  - 0x00: Command register (write-only)
  - 0x04: Status register (read-only)
  - 0x08-0x3F: Configuration registers (embed_dim, num_heads, etc.)
  - 0x40-0x7F: Performance counters (read-only, clear-on-read)

### AXI4 Master Interface (DMA)
- **Address Width**: 32 bits
- **Data Width**: 32 bits
- **Burst Support**: INCR4, INCR8, INCR16
- **Purpose**: Weight matrix transfers from external memory to weight SRAM

### External Memory Interface
- **Weight Memory**: External DDR3/DDR4 for model weights
- **Scratchpad**: On-chip SRAM (no external interface needed)
- **No off-chip activation storage** - all intermediate values remain on-chip

## Clock and Reset
- **Clock**: Single clock domain (clk)
- **Reset**: Active-high asynchronous reset (rst_n) with synchronization
- **Maximum Frequency**: Target 300MHz in TSMC 28nm process
- **Power Domains**: Single voltage domain with clock gating for zero-skipped units

## Technology Parameters
- **Process**: Target TSMC 28nm HPC+
- **Die Area**: ~8mm² (estimated)
- **Gate Count**: ~2.5M gates (estimated)
- **Memory**: 4KB scratchpad SRAM + weight storage in external memory
- **I/O**: AXI4-Lite (control), AXI4 (DMA), JTAG (debug)