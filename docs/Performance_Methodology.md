# BitbyBit GPU Performance Measurement Methodology

## Overview
This document defines the standardized methodology for measuring and reporting performance metrics for the BitbyBit GPU architecture. It ensures that all performance claims are mathematically consistent, verifiable, and reproducible across different test environments and configurations.

## Definitions of Key Metrics

### 1. Imprint Latency
**Definition**: The number of clock cycles from when a valid token input is presented to the GPU's input interface until the first bit of the output prediction is available at the output interface, assuming the GPU's internal state is already initialized with weights loaded and ready for computation.

**Measurement Point**:
- **Start**: Rising edge of clock when `input_token_valid` goes high
- **End**: Rising edge of clock when `output_prediction_valid` goes high for the first time
- **Condition**: Steady-state operation (not first token after reset)

**Units**: Clock cycles

### 2. Dynamic Latency
**Definition**: The total number of clock cycles required to process a complete sequence of tokens through all layers of the transformer model, from first token input to final token output, including all pipeline fill and drain effects.

**Measurement Point**:
- **Start**: Rising edge of clock when first `input_token_valid` goes high
- **End**: Rising edge of clock when last `output_prediction_valid` goes high
- **Condition**: Processing a complete sequence of N tokens through an L-layer model

**Units**: Clock cycles

**Relationship**: Dynamic Latency = (L × N × Average Cycles/Token) + Pipeline Overhead

### 3. Average Cycles/Token
**Definition**: The average number of clock cycles consumed per token processed in steady-state operation, excluding initial pipeline fill and final pipeline drain.

**Measurement Point**: 
- **Method**: Measure total cycles for processing T tokens in steady state, subtract pipeline overhead, divide by T
- **Formula**: (Total Cycles - Pipeline Fill Cycles - Pipeline Drain Cycles) / T
- **Alternative**: Inverse of sustained throughput when frequency is known

**Units**: Clock cycles per token

### 4. Throughput
**Definition**: The rate at which the GPU can process tokens when operating at a specified clock frequency in steady-state condition.

**Measurement Point**:
- **Method**: Count tokens processed over a known time interval during steady-state operation
- **Formula**: (Number of Tokens) / (Time Interval in Seconds)
- **Alternative**: (Clock Frequency in Hz) / (Average Cycles/Token)

**Units**: Tokens per second

### 5. Speedup vs. Baseline
**Definition**: The ratio of performance (throughput or inverse latency) of the BitbyBit GPU to that of a specified baseline implementation.

**Baseline Specification**: 
- **Reference**: ARM Cortex-M4 running at 100MHz
- **Implementation**: Optimized bare-metal C implementation of GPT-2 inference
- **Precision**: Float32 arithmetic
- **Library**: CMSIS-NN where applicable
- **Optimization Level**: -O3

**Measurement Conditions**:
- Same model architecture (GPT-2 Small: 12 layers, 768 embed_dim, 12 heads)
- Same sequence length (128 tokens)
- Same batch size (1)
- Same weight values (quantized to Q8.8 for fair comparison)
- No operating system overhead (bare-metal for both)

**Units**: Dimensionless ratio

## Test Conditions and Configuration

### Model Configuration
All performance measurements shall specify:
- **Architecture**: Transformer decoder-only (GPT-2 or similar)
- **Layers (L)**: Number of transformer blocks
- **Embedding Dimension (D)**: Model width
- **Number of Heads (H)**: For multi-head attention
- **Head Dimension (Dh)**: D/H (must be integer)
- **Feed-Forward Dimension (FFN_Dim)**: Usually 4×D
- **Vocabulary Size**: Size of embedding/output matrix
- **Sequence Length (S)**: Number of tokens processed
- **Batch Size (B)**: Number of sequences processed in parallel

### Weight and Activation Formats
- **Weight Storage Format**: Must be specified (INT4, ternary, or dense INT8)
- **Compute Format**: Q8.8 signed fixed-point (unless otherwise specified)
- **Activation Format**: Q8.8 signed fixed-point
- **Dequantization**: Must specify if weights are decompressed on-chip
- **Scale Factors**: Must be specified for INT4/ternary formats

### Input Conditions
- **Token IDs**: Must be specified (random, deterministic, or specific sequence)
- **Position IDs**: Must be specified (usually 0,1,2,... for each token)
- **Input Validity Pattern**: Must specify if inputs are back-to-back or spaced
- **Temperature**: Must be specified for timing measurements (usually 25°C nominal)
- **Voltage**: Must be specified for timing measurements (usually 1.0V nominal)

### Clock and Timing Specifications
- **Target Frequency**: The clock frequency at which the design is expected to operate
- **Measured Frequency**: Actual frequency achieved in timing analysis
- **Clock Uncertainty**: Jitter and skew considerations
- **Measurement Method**: 
  - Pre-layout: Static timing analysis (STA) reports
  - Post-layout: STA with extracted parasitics
  - Silicon: Ring oscillator or frequency counter measurement
- **Duty Cycle**: Assumed 50% unless otherwise specified
- **Clock Source**: Ideal clock assumed unless jitter specified

### Measurement Techniques
#### Cycle-Accurate Simulation
- **Tool**: Icarus Verilog with $timeunit/$timeprecision set to 1ps
- **Method**: Count clock cycles between start and end events using $display or VCD analysis
- **Warmup**: Discard first N tokens to reach steady state (N ≥ 2×pipeline depth)
- **Measurement Window**: Minimum 100 tokens for stable averages
- **Seed Control**: Fixed random seeds for reproducible results

#### Static Timing Analysis
- **Tool**: Primetime or equivalent
- **Corners**: Typical (TT) at 25°C, 1.0V unless otherwise specified
- **Paths**: Register-to-register paths only (exclude I/O unless specified)
- **Uncertainty**: Include clock jitter (typically 10-20ps) and margin
- **Report**: Worst-case negative slack (WCNS) and worst-case positive slack (WCPS)

#### Hardware Measurement
- **Equipment**: Logic analyzer or oscilloscope with sufficient bandwidth
- **Probes**: Minimal capacitance (<1pF) to avoid loading effects
- **Triggering**: On start and end events as defined above
- **Averaging**: Minimum 1000 cycles to reduce jitter effects
- **Calibration**: Equipment calibrated within last 24 hours

## Mathematical Consistency Checks

### Fundamental Relationships
All reported metrics must satisfy these mathematical relationships:

1. **Throughput and Cycles/Token**:
   ```
   Throughput (tokens/sec) = Clock Frequency (Hz) / Average Cycles/Token
   Average Cycles/Token = Clock Frequency (Hz) / Throughput (tokens/sec)
   ```

2. **Latency and Cycles/Token**:
   ```
   Dynamic Latency (cycles) = L × S × Average Cycles/Token + Pipeline Overhead
   Imprint Latency (cycles) ≤ Average Cycles/Token (for first token in steady state)
   ```

3. **Pipeline Depth Estimation**:
   ```
   Pipeline Overhead ≈ Pipeline Depth × (L + S - 2)
   Pipeline Depth ≥ Imprint Latency (minimum stages from input to first output)
   ```

### Consistency Validation Procedure
For any reported performance data, the following checks must be performed:

1. **Internal Consistency**:
   - Verify that reported throughput, frequency, and cycles/token satisfy fundamental relationship
   - Verify that dynamic latency is consistent with layers, sequence length, and cycles/token
   - Verify that imprint latency is reasonable given pipeline depth estimates

2. **Boundary Condition Checks**:
   - Imprint latency must be ≥ logic depth of fastest path from input to first output
   - Average cycles/token must be ≥ maximum combinational delay in any compute unit
   - Throughput must be ≤ peak issue rate of compute resources (e.g., MAC units/cycle)

3. **Comparison Validity**:
   - Baseline comparison must use same model, sequence length, and batch size
   - Precision differences must be accounted for (e.g., float32 vs Q8.8)
   - Implementation differences must be documented (e.g., library usage, optimization level)

## Reporting Requirements

### Mandatory Disclosures
All performance reports must include:

1. **Full Model Specification**:
   - L, D, H, Dh, FFN_Dim, Vocab Size
   - Sequence Length and Batch Size
   - Weight format and decompression details

2. **Test Environment**:
   - Simulation tool and version (or silicon step)
   - Clock frequency (target and measured)
   - Temperature and voltage conditions
   - Measurement technique (simulation, STA, silicon)
   - Random seed(s) used
   - Warmup and measurement window sizes

3. **Metric Definitions**:
   - Exact definitions of imprint latency, dynamic latency, etc.
   - Measurement points and conditions
   - Any deviations from standard definitions

4. **Mathematical Validation**:
   - Demonstration of internal consistency checks
   - Derivation of reported metrics from raw measurements
   - Identification of any assumptions made

5. **Limitations and Assumptions**:
   - Known sources of error or uncertainty
   - Conditions under which metrics may vary
   - Exclusions from measurement (e.g., first-token overhead)

### Preferred Reporting Format
Performance data should be reported in tables with the following structure:

| Metric | Value | Conditions | Validation Notes |
|--------|-------|------------|------------------|
| Imprint full-model latency | 112 cycles/token | @100MHz, mini imprint TB | Throughput = 100e6/112 = **892,857 tok/s** |
| Base full-model latency | 358 cycles/token | @100MHz, mini base TB | Throughput = 100e6/358 = **279,329 tok/s** |
| Imprint speedup vs base | 3.196× | Same TB family | 358/112; matrix workload mean |
| MEDUSA effective throughput | 2,678,571 tok/s | 3 draft heads × imprint | **Not** single-path sustained IPC |
| GPT-2 steady-state (legacy doc) | 130.0 cy/token | Different measurement | 769,230 tok/s @ 100MHz — do not mix with imprint |
| Dynamic Latency (128 tok) | 341 cycles total | Pipeline window metric | ~21.9 cy/token average over sequence |

**Reconciled rule:** `throughput = clock_hz / cycles_per_token`. The old **2.67M tok/s @ 100MHz** headline equals **MEDUSA effective** on the imprint path (3 × 892,857), not 130 cycles/token.

## Verification of Performance Claims

### Required Evidence
To accept a performance claim, the following evidence must be available:

1. **For Latency Claims**:
   - Cycle-accurate simulation waveforms showing start/end events
   - Static timing analysis report confirming frequency target
   - Gate-level simulation with SDF back-annotation (preferred)
   - Silicon measurement data (if available)

2. **For Throughput Claims**:
   - Sustained cycle count over measurement window
   - Confirmation of steady-state operation (constant IPC)
   - Bandwidth utilization calculations to rule out memory limits
   - Resource utilization (MAC units, memory ports) showing no saturation

3. **For Speedup Claims**:
   - Identical methodology applied to baseline and BitbyBit
   - Detailed baseline implementation description
   - Accounting for all differences (process node, frequency, etc.)
   - Sensitivity analysis showing impact of assumptions

### Reproducibility Package
All performance claims should be accompanied by:
- Exact testbench source code
- Configuration scripts and parameters
- Weight generation scripts with fixed seeds
- Reference golden model implementation
- Instructions for reproducing the measurement
- Expected output signatures for verification

## Known Issues and Open Questions

### Resolved Documentation Mapping (2026-05-22)

| Claim source | Meaning | @ 100 MHz |
|--------------|---------|-----------|
| 112 cycles | Imprint **full mini-model** cycles/token | 892,857 tok/s |
| 358 cycles | Base **full mini-model** cycles/token | 279,329 tok/s |
| 2.67M tok/s | **MEDUSA effective** (3× imprint) | 2,678,571 tok/s — label as speculative |
| 130 cycles/token | Legacy GPT-2 **steady-state** doc metric | 769,230 tok/s — separate from imprint TB |
| 341 cycles / 128 tokens | Dynamic latency over sequence | ~21.9 cy/token (different window) |

Authoritative sim evidence: `custom_gpu_project/sim/phase3_benchmark_proof_pack.json`.  
Derivation code: `custom_gpu_project/scripts/perf_metrics.py`.  
Claims report: `custom_gpu_project/docs/PERFORMANCE_CLAIMS_REPORT.md`.

### Measurement Challenges
1. **First-Token Effects**: Imprint latency measurements must exclude pipeline fill
2. **Last-Token Effects**: Dynamic latency measurements must properly drain pipeline
3. **Steady-State Determination**: Sufficient warmup cycles to reach equilibrium
4. **Measurement Perturbation**: Instrumentation not affecting timing (non-intrusive probes)
5. **Correlation vs Causation**: Ensuring performance changes are due to intended modifications

## References
1. "Principles of Computer Architecture" by Miles Murdocca and Vincent Heuring
2. "Computer Architecture: A Quantitative Approach" by Hennessy and Patterson
3. "EEMBC Autobench Suite Methodology" for embedded benchmarking
4. "SPEC CPU2017 Run and Reporting Rules" for performance measurement standards
5. ARM Cortex-M4 Technical Reference Manual for baseline specifications