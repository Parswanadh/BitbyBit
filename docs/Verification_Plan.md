# BitbyBit GPU Verification Plan

## Overview
This document outlines the comprehensive verification strategy for the BitbyBit GPU architecture. The goal is to ensure functional correctness, timing closure, and performance targets are met before tape-out. The verification approach combines unit testing, integration testing, system-level validation, and performance analysis.

## Verification Environment

### Simulation Tools
- **Primary Simulator**: Icarus Verilog (iverilog) + Verilog Procedural Interface (VPI) for cosimulation
- **Waveform Viewer**: GTKWave
- **Reference Models**: Python + NumPy bit-exact golden models
- **Coverage Tools**: Verilog coverage (if available in simulator)
- **Formal Verification**: Symbiotic/Yosys for critical control paths (planned)

### Testbench Architecture
- **Hierarchical Structure**: Mirrors DUT hierarchy for isolated module testing
- **Cosimulation**: Python testbenches driving Verilog via VPI for complex stimuli
- **Self-Checking**: Automatic comparison against golden models
- **Constrained Random**: SystemVerilog-style random tests with coverage goals
- **Directed Tests**: Corner case and edge case validation

## Verification Levels

### Level 1: Unit Verification
**Goal**: Verify individual modules in isolation with exhaustive and directed tests.

#### Modules to Verify
1. **Primitives Layer**
   - `zero_detect_mult.v`: Zero detection logic, multiplication correctness, saturation
   - `variable_precision_alu.v`: 4/8/16-bit operations, mode switching, flag generation
   - `sparse_memory_ctrl.v`: CSR encoding/decoding, boundary conditions
   - `fused_dequantizer.v`: INT4→INT8 conversion, scale handling
   - `gpu_top.v`: Pipeline control, ready/valid handshaking

2. **Compute Layer**
   - `mac_unit.v`: Multiply-accumulate, zero-skip, accumulator width, saturation
   - `systolic_array.v`: Dataflow correctness, PE interconnect, zero-skip propagation
   - `gelu_activation.v`: LUT lookup, approximation accuracy, max error bounds
   - `softmax_unit.v`: Exp LUT usage, max-subtract stability, normalization
   - `exp_lut_256.v`: Exponential accuracy, input/output range
   - `gelu_lut_256.v`: GELU approximation, negative/positive regions
   - `inv_sqrt_lut_256.v`: Inverse sqrt accuracy, handling of denormals

3. **Transformer Layer**
   - `layer_norm.v`: Mean/variance calculation, normalization, gamma/beta scaling
   - `linear_layer.v`: Weight loading, matrix-vector multiply, bias addition
   - `attention_unit.v`: Q/K/V projections, attention computation, output projection
   - `ffn_block.v`: Two-layer FFN, activation function, residual connections

4. **System Layer**
   - `embedding_lookup.v`: Token+position embedding combination
   - `transformer_block.v`: Full block functionality, residual connections
   - `gpt2_engine.v`: End-to-end inference, argmax output
   - `command_processor.v`: AXI4-Lite interface, opcode handling, FIFO depth
   - `config_regs.v`: Register read/write, default values, field widths
   - `perf_counters.v`: Counter increment, clear-on-read, overflow behavior
   - `reset_sync.v`: Metastability protection, reset pulse synchronization
   - `dma_engine.v`: AXI4 master bursts, address alignment, byte strobes
   - `kv_page_table.v`: Virtual-to-physical mapping, page allocation/deallocation
   - `stack_page_allocator.v`: LIFO allocation, full/empty conditions
   - `scratchpad_banked.v`: Bank conflicts, read/write correctness, burst support

#### Test Types
- **Exhaustive**: Small input spaces (e.g., 4-bit inputs for ALU operations)
- **Directed Corner Cases**: Min/max values, zero, saturation boundaries
- **Random Constrained**: Uniform/random distribution within legal ranges
- **Protocol Checks**: Ready/valid handshaking, burst termination
- **Timing Checks**: Setup/hold times (via SDF if available), clock gating

### Level 2: Integration Verification
**Goal**: Verify groups of modules working together.

#### Integration Points
1. **Compute Primitives → Compute Modules**
   - Zero-detect + MAC → zero-skip MAC unit
   - Variable precision ALU → GELU/Softmax units (control signals)
   - Sparse memory controller → weight loading (CSR format)

2. **Compute Modules → Transformer Blocks**
   - MAC units → systolic array → linear layers
   - Activation functions → FFN and attention post-processing
   - LayerNorm → attention and FFN pre-processing

3. **Transformer Blocks → System Integration**
   - Multiple transformer blocks → pipeline depth verification
   - Embedding lookup → first transformer block
   - Last transformer block → argmax → output interface

4. **Memory Subsystem → Compute Core**
   - Scratchpad access patterns → compute unit readiness
   - DMA loading → weight availability for compute
   - KV cache page table → attention unit access

#### Test Types
- **Dataflow Verification**: End-to-end data paths with known inputs/outputs
- **Performance Verification**: Cycle counting for operations, throughput measurement
- **Resource Verification**: Register usage, memory utilization, conflict detection
- **Error Injection**: Single-bit flips, protocol violations, timeout simulation

### Level 3: System-Level Verification
**Goal**: Verify complete system running real workloads.

#### Test Programs
1. **Unit Tests**: 
   - Single token inference through full pipeline
   - Fixed known vectors (identity weights, zero inputs, etc.)
   - Small models (2-layer, 4-embed-dim) for exhaustive output checking

2. **Functional Tests**:
   - NanoGPT (15M parameters) with deterministic weights
   - Gemma-2B style models (scaled down for verification)
   - Attention-only tests (verify QK^T and softmax)
   - FFN-only tests (verify GELU and projections)

3. **Performance Tests**:
   - Cycle-accurate timing for layer operations
   - Memory bandwidth utilization measurements
   - Zero-skip effectiveness measurement
   - Pipeline stall analysis

4. **Regression Tests**:
   - Previous release validation
   - Known bug fixes verification
   - Configuration parameter sweeps

#### Validation Methodology
- **Bit-Exact Comparison**: Verilog output vs. Python golden model (cycle-by-cycle)
- **Statistical Comparison**: For approximate operations (softmax, GELU)
- **Functional Comparison**: Top-k accuracy, perplexity measurements
- **Boundary Testing**: Maximum sequence lengths, batch sizes, model sizes

## Performance Verification

### Key Metrics to Verify
1. **Latency Metrics**
   - Imprint Latency: Time from token input to first output bit ready
   - Dynamic Latency: Time for complete N-layer inference
   - Average Cycles/Token: Steady-state throughput metric

2. **Throughput Metrics**
   - Tokens/second at target frequency (100MHz, 200MHz, 300MHz)
   - Effective compute utilization (MACs/cycle)
   - Memory bandwidth utilization (% of peak)

3. **Efficiency Metrics**
   - Energy per token (estimated from gate count and switching activity)
   - Zero-skip percentage (actual vs. predicted)
   - Weight compression ratio achieved

### Measurement Methodology
- **Cycle Counting**: Performance counters in design (MAC ops, stalls, etc.)
- **Trace Analysis**: VCD waveform analysis for critical paths
- **Statistical Sampling**: Run-time averaging over many tokens
- **Boundary Condition Testing**: Minimum/maximum latency paths

### Test Conditions Documentation
All performance measurements shall specify:
- **Model Configuration**: Layers, embed_dim, num_heads, seq_len
- **Weight Values**: Deterministic seed or known good values
- **Input Sequence**: Specific token IDs or random seed
- **Clock Frequency**: Target and actual frequency measured
- **Temperature/Voltage**: Nominal conditions (25°C, 1.0V)
- **Measurement Technique**: Cycle counter vs. waveform analysis
- **Warmup Cycles**: Number of tokens to reach steady state
- **Measurement Window**: Number of tokens over which average is taken

## Coverage Goals

### Code Coverage
- **Line Coverage**: >95% for all RTL files
- **Branch Coverage**: >90% for all RTL files
- **Condition Coverage**: >85% for all RTL files
- **FSM Coverage**: 100% states and transitions for all state machines
- **Toggle Coverage**: >80% for signals in critical datapaths

### Functional Coverage
- **Input Ranges**: Full range of Q8.8 values exercised for compute units
- **Control Sequences**: All valid command sequences tested
- **Memory Access Patterns**: Strided, random, and sequential access patterns
- **Error Conditions**: Overflow, underflow, invalid addresses, protocol violations
- **Corner Cases**: Min/max values, zero, denormals (where applicable)

## Regression Testing

### Automated Regression Suite
- **Nightly Runs**: Full test suite on commit to main branch
- **Weekly Runs**: Extended tests including random and long-running tests
- **Pre-Release**: Comprehensive suite including performance benchmarks
- **Continuous Integration**: GitHub Actions or similar for PR validation

### Test Organization
- **unit_tests/**: Individual module tests
- **integration_tests/**: Multi-module tests
- **system_tests/**: Full chip tests with realistic workloads
- **performance_tests/**: Benchmark and timing validation
- **regression_tests/**: Previously fixed bug validation

### Metrics Tracking
- **Pass/Fail Rate**: Overall and per-test-category
- **Coverage Trends**: Code and functional coverage over time
- **Performance Trends**: Key metrics (latency, throughput) over revisions
- **Bug Rate**: Defects found per KLOC or per test hour

## Sign-Off Criteria

### Functional Sign-Off
1. **Zero Known Critical Bugs**: No severity-1 or severity-2 defects open
2. **Regression Suite Pass**: 100% pass rate on nightly regression suite
3. **Coverage Goals Met**: All code and functional coverage targets achieved
4. **Bit-Exact Validation**: All modules show bit-exact agreement with golden models
5. **Protocol Compliance**: All interfaces comply with AXI4-Lite/AXI4 specifications

### Performance Sign-Off
1. **Latency Targets Met**: 
   - Imprint latency ≤ 112 cycles (at 100MHz target)
   - Dynamic latency ≤ 341 cycles for 12-layer inference
   - Average cycles/token ≤ 130.0
2. **Throughput Targets Met**:
   - ≥ 2.67M tokens/sec at 100MHz
   - Speedup ≥ 38.5x vs. ARM Cortex-M4 reference
3. **Resource Utilization**:
   - Gate count within 20% of estimates
   - Memory usage within 10% of allocations
   - Timing slack ≥ 10% at target frequency
4. **Power Estimates**:
   - Dynamic power within 30% of estimates
   - Leakage power within 50% of estimates (process dependent)

### Documentation Sign-Off
1. **All Specifications Complete**: Architecture, fixed-point, memory, verification docs
2. **User Guides Updated**: Getting started, API reference, examples
3. **Release Notes**: Known issues, limitations, and workarounds documented
4. **Licensing Verified**: All IP properly licensed for intended use

## Risk Assessment and Mitigation

### High Risks
1. **Timing Closure Failure**
   - **Mitigation**: Early static timing analysis, pipelining critical paths, logic replication
   - **Verification**: Gate-level simulation with SDF back-annotation

2. **Functional Bug in Control Logic**
   - **Mitigation**: Formal verification of FSMs, extensive directed testing
   - **Verification**: Randomized control sequence testing with coverage

3. **Performance Shortfall**
   - **Mitigation**: Early performance modeling, bottleneck identification
   - **Verification**: Cycle-accurate modeling before RTL completion

4. **Memory System Inefficiency**
   - **Mitigation**: Analytical modeling of access patterns, bank conflict simulation
   - **Verification**: Traffic-driven validation with realistic workloads

### Medium Risks
1. **Power Overestimation**
   - **Mitigation**: Activity factor analysis, clock gating validation
   - **Verification**: Post-layout power extraction with representative vectors

2. **Interface Misintegration**
   - **Mitigation**: Protocol checkers, monitor assertions in testbenches
   - **Verification**: Interface-level testing with VIP (if available)

3. **Scalability Limitations**
   - **Mitigation**: Parameterized design testing with multiple configurations
   - **Verification**: Configuration sweep in regression suite

## Tools and Resources

### Required Tools
- **Simulator**: Icarus Verilog 12.0+ or equivalent
- **Waveform Viewer**: GTKWave 3.3+ or equivalent
- **Python**: 3.8+ with NumPy for reference models
- **Build System**: GNU Make or similar for test automation
- **Version Control**: Git for testbench and script management

### Optional Tools (Recommended)
- **Formal Verification**: Yosys/Symbiotic for property checking
- **Coverage Tool**: Built-in simulator coverage or external tool
- **Power Analyzer**: For post-layout power estimation
- **Static Linter**: Verilator or SpyGlass for lint-free RTL

### Testbench Utilities
- **Clock Generation**: Configurable frequency, duty cycle, jitter
- **Reset Generation**: Programmable pulse width, synchronous/asynchronous
- **Memory Models**: Simple RAM/ROM models for testbenches
- **Bus Functional Models**: AXI4-Lite/AXI4 BFMs for interface testing
- **Scoreboards**: Automatic expected value tracking and comparison
- **Coverage Collectors**: Functional coverage tracking for directed tests

## Schedule and Milestones

### Phase 1: Unit Verification (Weeks 1-3)
- **Milestone 1.1**: All primitive modules verified (≥95% line coverage)
- **Milestone 1.2**: All compute modules verified (≥90% line coverage)
- **Milestone 1.3**: All transformer modules verified (≥90% line coverage)
- **Milestone 1.4**: All system modules verified (≥85% line coverage)

### Phase 2: Integration Verification (Weeks 4-5)
- **Milestone 2.1**: Compute primitives → compute modules integration verified
- **Milestone 2.2**: Compute modules → transformer blocks integration verified
- **Milestone 2.3**: Transformer blocks → system integration verified
- **Milestone 2.4**: Memory subsystem → compute core integration verified

### Phase 3: System-Level Verification (Weeks 6-7)
- **Milestone 3.1**: NanoGPT inference verified bit-exact with golden model
- **Milestone 3.2**: Gemma-style model inference verified (scaled down)
- **Milestone 3.3**: Performance targets validated (latency, throughput)
- **Milestone 3.4**: Regression suite established and passing

### Phase 4: Sign-Off Preparation (Week 8)
- **Milestone 4.1**: Coverage goals achieved and documented
- **Milestone 4.2**: All known issues resolved or documented
- **Milestone 4.3**: Sign-off criteria met and reviewed
- **Milestone 4.4**: Final verification report completed

## References
1. "SystemVerilog for Verification" by Chris Spear and Greg Tumbush
2. "Verification Methodology Manual for SystemVerilog" (Accellera)
3. "Principles of Verifiable RTL Design" by Ben Cohen et al.
4. AMBA® AXI and ACE Protocol Specification (ARM)
5. UVM (Universal Verification Methodology) 1.2