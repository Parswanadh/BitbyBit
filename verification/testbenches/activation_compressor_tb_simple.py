"""
Simple testbench for activation_compressor comparing RTL with golden model.
This version uses only Python and can run without external dependencies.
"""

import sys
import os
import random

# Add the project root to the path so we can import from verification/golden_models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from golden_models.activation_compressor import (
    ActivationCompressorGolden,
    activation_compressor_golden,
    activation_decompressor_golden,
)


def signed_to_int(val, bits):
    """Convert signed binary value to integer"""
    if val >= (1 << (bits - 1)):
        val -= 1 << bits
    return val


def int_to_signed(val, bits):
    """Convert integer to signed binary value"""
    if val < 0:
        val = (1 << bits) + val
    return val


def simulate_activation_compressor_rtl(test_data):
    """
    Simplified RTL simulation model (matches the Verilog logic).
    This simulates what the RTL would produce.
    """
    vector_len = 4
    data_width = 16

    # Internal state
    compressed_out = [0] * vector_len
    scale_out = 0
    compress_done = 0
    decompress_out = [0] * (vector_len * data_width // 8)  # 8-bit output
    decompress_done = 0
    total_compressions = 0
    total_bytes_saved = 0

    # Simulate compression (simplified - just one cycle)
    if len(test_data) == vector_len:
        # Step 1: Find absolute max
        abs_max = 0
        for val in test_data:
            abs_val = abs(val)
            if abs_val > abs_max:
                abs_max = abs_val

        # Step 2: Compute scale factor
        if abs_max > 127:  # 16'sd127
            scale_out = abs_max >> (data_width - 8)  # abs_max[15:7] for 16-bit
        else:
            scale_out = 1

        # Step 3: Quantize each element
        for i in range(vector_len):
            val = test_data[i]
            if abs_max > 127:
                # Shift-based quantization: val >> (data_width - 8)
                compressed_val = val >> (data_width - 8)
            else:
                compressed_val = val & 0xFF  # Lower 8 bits
            # Ensure 8-bit signed representation
            if compressed_val >= 128:
                compressed_val -= 256
            compressed_out[i] = compressed_val

        compress_done = 1
        total_compressions = 1
        total_bytes_saved = vector_len

    return {
        "compressed_out": compressed_out,
        "scale_out": scale_out,
        "compress_done": compress_done,
        "total_compressions": total_compressions,
        "total_bytes_saved": total_bytes_saved,
    }


def simulate_activation_decompressor_rtl(compressed_data, scale_val):
    """
    Simplified RTL decompression simulation.
    """
    vector_len = 4
    data_width = 16

    decompressed_out = [0] * vector_len
    decompress_done = 0

    # Simulate decompression
    for i in range(vector_len):
        val = compressed_data[i]
        # Sign-extend the 8-bit value to 16-bit
        if val < 0:
            sign_extended = val | 0xFF00
        else:
            sign_extended = val
        # Multiply by scale factor
        decompressed_val = sign_extended * scale_val
        decompressed_out[i] = decompressed_val

    decompress_done = 1

    return {"decompressed_out": decompressed_out, "decompress_done": decompress_done}


def test_activation_compressor_basic():
    """Basic test for activation compressor"""
    print("=" * 50)
    print("Testing Activation Compressor - Basic Tests")
    print("=" * 50)

    # Test 1: Small values (within 8-bit range)
    print("\nTest 1: Compressing small values...")
    test_data = [50, 30, 20, 10]
    print(f"Input: {test_data}")

    # RTL simulation
    rtl_result = simulate_activation_compressor_rtl(test_data)
    print(
        f"RTL Output: compressed={rtl_result['compressed_out']}, scale={rtl_result['scale_out']}"
    )

    # Golden model
    golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)
    print(f"Golden Output: compressed={golden_compressed}, scale={golden_scale}")

    # Check match
    if (
        rtl_result["compressed_out"] == golden_compressed
        and rtl_result["scale_out"] == golden_scale
    ):
        print("[PASS] Small values test")
        test1_pass = True
    else:
        print("[FAIL] Small values test")
        test1_pass = False

    # Test 2: Large values (require scaling)
    print("\nTest 2: Compressing large values...")
    test_data = [1024, 512, 256, 128]
    print(f"Input: {test_data}")

    # RTL simulation
    rtl_result = simulate_activation_compressor_rtl(test_data)
    print(
        f"RTL Output: compressed={rtl_result['compressed_out']}, scale={rtl_result['scale_out']}"
    )

    # Golden model
    golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)
    print(f"Golden Output: compressed={golden_compressed}, scale={golden_scale}")

    # Check match
    if (
        rtl_result["compressed_out"] == golden_compressed
        and rtl_result["scale_out"] == golden_scale
    ):
        print("[PASS] Large values test")
        test2_pass = True
    else:
        print("[FAIL] Large values test")
        test2_pass = False

    # Test 3: Decompression
    print("\nTest 3: Decompression...")
    # Use the compressed output from test 2
    compressed_data = rtl_result["compressed_out"]
    scale_val = rtl_result["scale_out"]
    print(f"Compressed input: {compressed_data}, scale: {scale_val}")

    # RTL decompression
    rtl_decomp_result = simulate_activation_decompressor_rtl(compressed_data, scale_val)
    print(f"RTL Decompressed: {rtl_decomp_result['decompressed_out']}")

    # Golden model
    golden_decompressed = activation_decompressor_golden(compressed_data, scale_val)
    print(f"Golden Decompressed: {golden_decompressed}")

    # Check match
    if rtl_decomp_result["decompressed_out"] == golden_decompressed:
        print("[PASS] Decompression test")
        test3_pass = True
    else:
        print("[FAIL] Decompression test")
        test3_pass = False

    # Test 4: Counter verification
    print("\nTest 4: Counter verification...")
    expected_compressions = 2
    expected_bytes_saved = 8

    actual_compressions = rtl_result["total_compressions"]  # From second test
    actual_bytes_saved = rtl_result["total_bytes_saved"]  # From second test

    print(
        f"Expected: compressions={expected_compressions}, bytes_saved={expected_bytes_saved}"
    )
    print(
        f"Actual:   compressions={actual_compressions}, bytes_saved={actual_bytes_saved}"
    )

    if (
        actual_compressions == expected_compressions
        and actual_bytes_saved == expected_bytes_saved
    ):
        print("[PASS] Counter test")
        test4_pass = True
    else:
        print("[FAIL] Counter test")
        test4_pass = False

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Test 1 (Small values): {'PASS' if test1_pass else 'FAIL'}")
    print(f"Test 2 (Large values): {'PASS' if test2_pass else 'FAIL'}")
    print(f"Test 3 (Decompression): {'PASS' if test3_pass else 'FAIL'}")
    print(f"Test 4 (Counters): {'PASS' if test4_pass else 'FAIL'}")

    all_passed = test1_pass and test2_pass and test3_pass and test4_pass
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 50)

    return all_passed


def test_activation_compressor_random(num_tests=50):
    """Randomized test for activation compressor"""
    print("\n" + "=" * 50)
    print(f"Running {num_tests} Random Tests")
    print("=" * 50)

    pass_count = 0

    for test_num in range(num_tests):
        # Generate random test data (-128 to 127 for Q8.8 range)
        test_data = [random.randint(-128, 127) for _ in range(4)]

        # RTL simulation
        rtl_result = simulate_activation_compressor_rtl(test_data)

        # Golden model
        golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)

        # Check match
        if (
            rtl_result["compressed_out"] == golden_compressed
            and rtl_result["scale_out"] == golden_scale
        ):
            pass_count += 1
            if test_num % 10 == 0:  # Log every 10th pass
                print(f"Test {test_num:2d}: PASS - {test_data}")
        else:
            print(f"Test {test_num:2d}: FAIL - {test_data}")
            print(
                f"  RTL:      compressed={rtl_result['compressed_out']}, scale={rtl_result['scale_out']}"
            )
            print(f"  Golden:   compressed={golden_compressed}, scale={golden_scale}")

    print(f"\nRandom test results: {pass_count}/{num_tests} passed")

    # Test decompression with random data
    print("\nTesting decompression with random data...")
    decomp_pass_count = 0

    for test_num in range(num_tests):
        # Generate random compressed data and scale
        compressed_data = [random.randint(-128, 127) for _ in range(4)]
        scale_data = random.randint(1, 16)

        # RTL decompression
        rtl_decomp_result = simulate_activation_decompressor_rtl(
            compressed_data, scale_data
        )

        # Golden model
        golden_decompressed = activation_decompressor_golden(
            compressed_data, scale_data
        )

        # Check match
        if rtl_decomp_result["decompressed_out"] == golden_decompressed:
            decomp_pass_count += 1
            if test_num % 10 == 0:
                print(f"Decomp Test {test_num:2d}: PASS")
        else:
            print(f"Decomp Test {test_num:2d}: FAIL")
            print(f"  Got:      {rtl_decomp_result['decompressed_out']}")
            print(f"  Expected: {golden_decompressed}")

    print(
        f"\nRandom decompression test results: {decomp_pass_count}/{num_tests} passed"
    )

    overall_pass = (pass_count == num_tests) and (decomp_pass_count == num_tests)
    print(f"\nOverall random tests: {'ALL PASSED' if overall_pass else 'SOME FAILED'}")

    return overall_pass


if __name__ == "__main__":
    # Run basic tests
    basic_result = test_activation_compressor_basic()

    # Run random tests
    random_result = test_activation_compressor_random(num_tests=30)

    # Final result
    if basic_result and random_result:
        print("\n🎉 ALL VERIFICATION TESTS PASSED!")
        exit(0)
    else:
        print("\n❌ SOME VERIFICATION TESTS FAILED!")
        exit(1)
