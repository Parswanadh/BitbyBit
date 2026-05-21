# Memory Architecture for BitbyBit GPU

## Overview
This document describes the memory subsystem of the BitbyBit GPU, focusing on the scratchpad SRAM organization, banking strategy, conflict avoidance, and memory access patterns for tensor operations.

## Scratchpad Organization
The scratchpad is a banked SRAM designed to hold intermediate activations and weights during tensor operations. It is organized into multiple banks to allow parallel access and reduce conflicts.

### Banked SRAM Structure
- **Number of Banks**: 8 banks (configurable via parameter)
- **Bank Size**: Each bank has a depth of 512 words (16 bits per word), totaling 4K words (8KB) across all banks
- **Data Width**: 16 bits per word (Q8.8 fixed-point format)
- **Address Mapping**: 
  - Bank select: Upper bits of address (log2(NUM_BANKS))
  - Bank address: Lower bits of address

### Conflict Avoidance Mechanism
To avoid bank conflicts during tensor operations:
1. **Tensor Mapping Strategy**: Different tensor dimensions are mapped to different banks based on access patterns
2. **Padding**: Strides are padded to ensure consecutive accesses map to different banks
3. **Dynamic Allocation**: A memory controller assigns tensor segments to banks to minimize conflicts

## Memory Access Patterns for Tensor Operations

### Q/K/V Projections
- **Input**: Activation matrix [seq_len, embed_dim]
- **Weights**: Projection matrices [embed_dim, embed_dim] for Q, K, V
- **Access Pattern**: 
  - Activations read sequentially along seq_len dimension
  - Weights accessed with stride embed_dim
- **Bank Mapping**: 
  - Activation rows mapped to consecutive banks
  - Weight columns mapped to avoid conflicts with activation reads

### Attention Computation
- **QK^T**: Matrix multiply [seq_len, num_heads*head_dim] x [num_heads*head_dim, seq_len]
- **Softmax**: Row-wise softmax on QK^T
- **Weighted Sum**: [seq_len, seq_len] x [seq_len, num_heads*head_dim]
- **Access Pattern**:
  - QK^T requires reading rows of Q and columns of K
  - Softmax requires row-wise access
  - Weighted sum requires reading rows of attention scores and columns of V
- **Bank Mapping**:
  - Q and K matrices mapped to separate bank groups
  - V matrix mapped to avoid conflicts with attention score reads

### Feed-Forward Network (FFN)
- **First Layer**: [seq_len, embed_dim] x [embed_dim, ffn_dim] + bias + ReLU
- **Second Layer**: [seq_len, ffn_dim] x [ffn_dim, embed_dim] + bias
- **Access Pattern**:
  - Similar to projection layers but with different dimensions
  - ReLU activation creates sparsity (zeros) that can be exploited
- **Bank Mapping**:
  - Input and weight matrices mapped to minimize conflicts
  - Intermediate results (hidden layer) stored in separate bank group

## AXI4-Lite/AXI4 Interfaces
The memory subsystem exposes two primary interfaces:
1. **AXI4-Lite Slave**: For configuration and low-bandwidth control
2. **AXI4 Master**: For high-bandwidth DMA transfers to/from external memory

### AXI4-Lite Interface
- **Address Width**: 32 bits
- **Data Width**: 32 bits
- **Registers**:
  - Scratchpad base address
  - Bank configuration
  - Memory controller status
  - Performance counters

### AXI4 Master Interface (DMA)
- **Burst Support**: INCR, WRAP bursts up to 256 beats
- **Data Width**: 64 bits (4x 16-bit words per beat)
- **Address Generation**: Linear and 2D stride patterns supported
- **Timing Optimization**:
  - Read/write issuing separated to avoid bus turnaround delays
  - Outstanding read/write requests limited to 4 to prevent bus saturation
  - Bank-aware address translation to maximize row hits

## Integration with Transformer Operations
The memory controller is responsible for:
1. Mapping tensor operations to scratchpad banks
2. Scheduling DMA transfers to hide latency
3. Providing conflict-free access patterns to compute units
4. Managing data reuse to minimize external memory bandwidth

### Dataflow in Accelerated Transformer Block
1. **Input Activations**: Loaded from external memory via DMA into scratchpad
2. **LayerNorm**: Reads activations, writes normalized output to scratchpad
3. **Attention**:
   - Q/K/V projections read from scratchpad, write results back
   - Attention scores computed and stored in scratchpad
   - Weighted sum reads attention scores and V, writes output
4. **FFN**:
   - First layer reads normalized activations, writes hidden layer
   - Second layer reads hidden layer, writes final output
5. **Output**: Final activations stored in scratchpad for next layer or output via DMA

## Configuration Parameters
All memory subsystem parameters are configurable via AXI4-Lite:
- `NUM_BANKS`: Number of SRAM banks (default: 8)
- `BANK_DEPTH`: Words per bank (default: 512)
- `SCRATCHPAD_BASE`: Base address in external memory for DMA
- `BANK_INTERLEAVE`: Enable/disable bank interleaving (default: enabled)

## Verification
Memory subsystem verification includes:
1. Bank conflict detection under various access patterns
2. Correctness of AXI4-Lite register interface
3. DMA transfer correctness and timing
4. Bit-exact comparison with golden models for tensor operations
5. Timing analysis to ensure Fmax targets are met