# Track Specification: Fix Gemma-3 Q8.8 Extraction Script

## Overview
The `export_gemma3_q88.py` script crashed during the Phase 1 verification of the Swarm Analysis track with a `TypeError: Got unsupported ScalarType BFloat16`. It also lacked the necessary MSE calculation logic. This track aims to fix the script so it can successfully quantize the model and calculate the MSE.

## Functional Requirements
1. **Fix BFloat16 Conversion:** Cast tensors from `bfloat16` to `float32` before converting to NumPy arrays.
2. **Add MSE Calculation:** Calculate the Mean Squared Error (MSE) between the original float values and the dequantized Q8.8 values across all weights, and print it at the end of the script.

## Acceptance Criteria
- Running `python custom_gpu_project/scripts/export_gemma3_q88.py` must succeed without `TypeError`.
- The script must print the Quantization Mean Squared Error (MSE) at the end of the execution.