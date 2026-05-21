# BitbyBit GPU Fixed-Point Specification

## Overview
This document specifies the fixed-point number format used throughout the BitbyBit GPU architecture. All arithmetic operations, memory storage, and data transfers use this format to ensure consistency and determinism across the design.

## Primary Format: Q8.8 Signed Fixed-Point

### Bit Layout
```
Bit 15: Sign bit (0 = positive, 1 = negative)
Bits 14-8: Integer bits (7 bits)
Bits 7-0: Fractional bits (8 bits)
```
Layout: `[S IIIIIII . FFFFFFFF]`

### Range and Precision
- **Minimum Value**: -128.00000000 (0x8000)
- **Maximum Value**: +127.99609375 (0x7FFF)
- **Precision**: 1/256 = 0.00390625
- **Least Significant Bit (LSB) Weight**: 2^-8 = 1/256

### Encoding Examples
| Decimal Value | Hexadecimal | Binary Representation |
|---------------|-------------|----------------------|
| 0.0           | 0x0000      | 0000 0000 0000 0000 |
| 1.0           | 0x0100      | 0000 0001 0000 0000 |
| -1.0          | 0xFF00      | 1111 1111 0000 0000 |
| 1.5           | 0x0180      | 0000 0001 1000 0000 |
| -1.5          | 0xFE80      | 1111 1110 1000 0000 |
| 127.99609375  | 0x7FFF      | 0111 1111 1111 1111 |
| -128.0        | 0x8000      | 1000 0000 0000 0000 |
| 0.00390625    | 0x0001      | 0000 0000 0000 0001 |
| -0.00390625   | 0xFFFF      | 1111 1111 1111 1111 |

## Format Usage by Module

### Compute Units
All compute units operate exclusively in Q8.8 format:
- **MAC Units**: Inputs, outputs, and accumulators use Q8.8
- **Variable Precision ALU**: Can operate in Q4.4, Q8.8, or Q16.0 modes, but defaults to Q8.8 for neural network operations
- **Activation Functions**: GELU, EXP, and inverse square root LUTs accept and produce Q8.8 values
- **Softmax Unit**: Input scores and output probabilities are in Q8.8

### Memory Subsystem
- **Weight Storage**: Stored externally in INT4 format, converted to Q8.8 via fused dequantizer
- **Activation Storage**: Stored in on-chip scratchpad SRAM as Q8.8 values
- **KV Cache**: Keys and values stored as Q8.8 in virtualized pages
- **Bias Values**: Stored as Q8.8 in weight memory

### Interfaces
- **AXI4-Lite Configuration Registers**: Model parameters (embed_dim, num_heads, etc.) stored as integer values (not fixed-point)
- **AXI4-Lite Data Transfers**: Token IDs and position IDs are integer values; embeddings are Q8.8
- **Performance Counters**: Integer counts of events (cycles, MAC operations, etc.)

## Arithmetic Rules

### Addition and Subtraction
- Performed using standard two's complement addition/subtraction
- Overflow detection: Set when carry into sign bit differs from carry out of sign bit
- On overflow: Saturate to maximum or minimum representable value
- Example: 0x7FFF + 0x0001 = 0x7FFF (saturates at max)
- Example: 0x8000 + 0xFFFF = 0x8000 (saturates at min)

### Multiplication
- **Q8.8 × Q8.8 → Q16.16 intermediate result**
- **Truncation to Q8.8**: Take bits [23:8] of the 32-bit product (discard lower 8 fractional bits and upper 16 bits)
- **Alternative**: Round to nearest by adding 0x00008000 before truncation (currently not implemented)
- Overflow in multiplication: Handled by saturation in the final truncation step
- Example: 0x0100 × 0x0100 = 0x00010000 → truncated to 0x0001 (1.0 × 1.0 = 1.0)

### Special Operations
- **Zero Detection**: Value equals 0x0000
- **Sign Extraction**: Bit 15 of the value
- **Absolute Value**: If negative, two's complement; if positive, unchanged
- **Saturation**: Explicitly clamp to 0x7FFF (max) or 0x8000 (min) when exceeding range

## Conversion Rules

### From Integer to Q8.8
```
Q8.8_value = integer_value << 8
```
- Integer value must be in range [-128, 127] to avoid overflow
- Example: 5 → 0x0500, -3 → 0xF D00 (0xFD00)

### From Q8.8 to Integer
```
integer_value = Q8.8_value >> 8   (arithmetic right shift)
```
- Fractional part is truncated (rounded toward zero)
- Example: 0x0180 (1.5) → 0x0001 (1), 0xFE80 (-1.5) → 0xFFFF (-1)

### From Floating-Point to Q8.8
```
Q8.8_value = (int)(float_value * 256.0)
```
- Result saturated to [-128.0, 127.99609375] if out of range
- Example: 3.5 → 3.5 * 256 = 896 → 0x0380
- Example: -1.2 → -1.2 * 256 = -307.2 → -307 → 0xF ED9 (0xFED9)

### From Q8.8 to Floating-Point
```
float_value = Q8.8_value / 256.0
```
- Exact conversion with no loss (within represented precision)
- Example: 0x0180 → 384 / 256.0 = 1.5
- Example: 0xFE80 → -384 / 256.0 = -1.5

## Special Values and Exceptions

### Not-a-Number (NaN)
- Not represented in Q8.8 format
- Undefined operations (e.g., square root of negative) should saturate to zero or appropriate bound

### Infinity
- Not represented; overflow results in saturation to maximum/minimum values

### Denormals
- Not applicable; fixed-point format has uniform precision

## Consistency Requirements

### Module Compliance
All modules must:
1. Accept and produce Q8.8 values on all neural data paths
2. Use saturation arithmetic for overflow conditions
3. Truncate (not round) fractional bits in multiplication unless otherwise specified
4. Treat 0x0000 as numerical zero
5. Treat 0x8000 as minimum value (-128.0)
6. Treat 0x7FFF as maximum value (+127.99609375)

### Verification
- Testbenches must verify format compliance with directed and random tests
- Golden models must use identical Q8.8 arithmetic rules
- Overflow saturation must be checked in all arithmetic units
- Conversion modules (dequantizer, etc.) must produce correctly formatted Q8.8 values

## Known Issues and Fixes
Based on NVIDIA critique review:

### Issue: Inconsistent Q8.8 Interpretation
- Some modules treated Q8.8 as unsigned or used different binary points
- **Fix**: All modules now use signed Q8.8 with binary point between bits 7 and 8

### Issue: Overflow in MAC Units
- 16-bit accumulators could overflow when summing two 15-bit partial products
- **Fix**: Increased accumulator width to 20 bits with saturation to Q8.8 on output

### Issue: Missing Saturation in Arithmetic
- Addition/subtraction could wrap around on overflow
- **Fix**: Added saturation logic to all arithmetic units

### Issue: Incorrect Fixed-Point in LUTs
- EXP and GELU LUTs used incorrect scaling
- **Fix**: LUTs now store Q8.8 values representing the function output for Q8.8 input

## References
1. "Fixed-Point Representation & Fractional Math" by Erick L. Oberstar
2. BitNet b1.58: "1-bit Transformers" (for ternary weight interpretation)
3. IEEE Standard 754™-2008 for Floating-Point Arithmetic (for comparison)