"""
Testbench for activation_compressor with VPI/PyCoCosimulation for bit-exact comparison.
This testbench compares RTL output with golden model output.
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.clock import Clock
import random
import sys
import os

# Add golden model to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../golden_models"))
from activation_compressor import ActivationCompressorGolden


async def reset_dut(dut):
    """Apply reset to DUT"""
    dut.rst.value = 1
    dut.clk.value = 0
    dut.compress_valid.value = 0
    dut.decompress_valid.value = 0
    dut.data_in.value = 0
    dut.compressed_in.value = 0
    dut.scale_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)


async def wait_for_compress_done(dut, timeout=20):
    """Wait for compress_done signal with timeout"""
    for _ in range(timeout):
        if dut.compress_done.value:
            return True
        await RisingEdge(dut.clk)
    return False


async def wait_for_decompress_done(dut, timeout=20):
    """Wait for decompress_done signal with timeout"""
    for _ in range(timeout):
        if dut.decompress_done.value:
            return True
        await RisingEdge(dut.clk)
    return False


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


@cocotb.test()
async def test_activation_compressor_basic(dut):
    """Basic test for activation compressor"""

    # Start clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    cocotb.start_soon(clock.start())

    # Reset DUT
    await reset_dut(dut)

    # Create golden model
    golden_model = ActivationCompressorGolden(vector_len=4, data_width=16)

    # Test 1: Small values (within 8-bit range)
    dut._log.info("Test 1: Compressing small values...")
    test_data = [50, 30, 20, 10]

    # Apply input
    dut.data_in.value = 0
    for i, val in enumerate(test_data):
        dut.data_in.value |= int_to_signed(val, 16) << (i * 16)
    dut.compress_valid.value = 1
    await RisingEdge(dut.clk)
    dut.compress_valid.value = 0

    # Wait for completion
    if not await wait_for_compress_done(dut):
        dut._log.error("Compression did not complete")
        return False

    # Capture outputs
    compressed_out = []
    for i in range(4):
        val = signed_to_int((dut.compressed_out.value >> (i * 8)) & 0xFF, 8)
        compressed_out.append(val)
    scale_out = dut.scale_out.value & 0xFF

    # Compare with golden model
    golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)

    success = True
    if compressed_out != golden_compressed:
        dut._log.error(
            f"Compression mismatch: got {compressed_out}, expected {golden_compressed}"
        )
        success = False
    if scale_out != golden_scale:
        dut._log.error(f"Scale mismatch: got {scale_out}, expected {golden_scale}")
        success = False

    if success:
        dut._log.info(
            f"[PASS] Small values: compressed={compressed_out}, scale={scale_out}"
        )

    # Test 2: Large values (require scaling)
    dut._log.info("Test 2: Compressing large values...")
    test_data = [1024, 512, 256, 128]

    # Apply input
    dut.data_in.value = 0
    for i, val in enumerate(test_data):
        dut.data_in.value |= int_to_signed(val, 16) << (i * 16)
    dut.compress_valid.value = 1
    await RisingEdge(dut.clk)
    dut.compress_valid.value = 0

    # Wait for completion
    if not await wait_for_compress_done(dut):
        dut._log.error("Compression did not complete")
        return False

    # Capture outputs
    compressed_out = []
    for i in range(4):
        val = signed_to_int((dut.compressed_out.value >> (i * 8)) & 0xFF, 8)
        compressed_out.append(val)
    scale_out = dut.scale_out.value & 0xFF

    # Compare with golden model
    golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)

    if compressed_out != golden_compressed:
        dut._log.error(
            f"Compression mismatch: got {compressed_out}, expected {golden_compressed}"
        )
        success = False
    if scale_out != golden_scale:
        dut._log.error(f"Scale mismatch: got {scale_out}, expected {golden_scale}")
        success = False

    if success:
        dut._log.info(
            f"[PASS] Large values: compressed={compressed_out}, scale={scale_out}"
        )

    # Test 3: Decompression
    dut._log.info("Test 3: Decompression...")
    # Use the compressed output from test 2 as input
    dut.compressed_in.value = 0
    for i, val in enumerate(compressed_out):
        dut.compressed_in.value |= int_to_signed(val, 8) << (i * 8)
    dut.scale_in.value = scale_out & 0xFF
    dut.decompress_valid.value = 1
    await RisingEdge(dut.clk)
    dut.decompress_valid.value = 0

    # Wait for completion
    if not await wait_for_decompress_done(dut):
        dut._log.error("Decompression did not complete")
        return False

    # Capture outputs
    decompressed_out = []
    for i in range(4):
        val = signed_to_int((dut.decompressed_out.value >> (i * 16)) & 0xFFFF, 16)
        decompressed_out.append(val)

    # Compare with golden model
    golden_decompressed = activation_decompressor_golden(compressed_out, scale_out)

    if decompressed_out != golden_decompressed:
        dut._log.error(
            f"Decompression mismatch: got {decompressed_out}, expected {golden_decompressed}"
        )
        success = False
    else:
        dut._log.info(
            f"[PASS] Decompression: original={test_data}, decompressed={decompressed_out}"
        )

    # Test 4: Counter verification
    dut._log.info("Test 4: Counter verification...")
    expected_compressions = 2  # We did two compression operations
    expected_bytes_saved = 8  # 4 bytes per compression * 2 operations

    actual_compressions = dut.total_compressions.value
    actual_bytes_saved = dut.total_bytes_saved.value

    if actual_compressions != expected_compressions:
        dut._log.error(
            f"Compression counter mismatch: got {actual_compressions}, expected {expected_compressions}"
        )
        success = False
    if actual_bytes_saved != expected_bytes_saved:
        dut._log.error(
            f"Bytes saved counter mismatch: got {actual_bytes_saved}, expected {expected_bytes_saved}"
        )
        success = False

    if success:
        dut._log.info(
            f"[PASS] Counters: compressions={actual_compressions}, bytes_saved={actual_bytes_saved}"
        )

    # Final result
    if success:
        dut._log.info("============================================")
        dut._log.info("  ALL TESTS PASSED")
        dut._log.info("============================================")
    else:
        dut._log.error("============================================")
        dut._log.error("  SOME TESTS FAILED")
        dut._log.error("============================================")

    return success


def activation_decompressor_golden(
    compressed_in, scale_in, vector_len=4, data_width=16
):
    """
    Functional golden model for activation decompression (single-shot).

    Args:
        compressed_in: list of 8-bit integers (signed)
        scale_in: 8-bit scale factor
        vector_len: length of input vector
        data_width: width of output data (should be 16)

    Returns:
        list: decompressed Q8.8 values (signed)
    """
    # Sign-extend the 8-bit value to 16-bit and multiply by scale factor
    decompressed_out = []
    for val in compressed_in:
        # Sign-extend the 8-bit value to 16-bit
        if val < 0:
            sign_extended = val | 0xFF00
        else:
            sign_extended = val
        # Multiply by scale factor
        decompressed_val = sign_extended * scale_in
        decompressed_out.append(decompressed_val)

    return decompressed_out


@cocotb.test()
async def test_activation_compressor_random(dut):
    """Randomized test for activation compressor"""

    # Start clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    cocotb.start_soon(clock.start())

    # Reset DUT
    await reset_dut(dut)

    # Create golden model
    golden_model = ActivationCompressorGolden(vector_len=4, data_width=16)

    # Run multiple random tests
    num_tests = 100
    pass_count = 0

    for test_num in range(num_tests):
        # Generate random test data (-128 to 127 for Q8.8 range)
        test_data = [random.randint(-128, 127) for _ in range(4)]

        # Apply input
        dut.data_in.value = 0
        for i, val in enumerate(test_data):
            dut.data_in.value |= int_to_signed(val, 16) << (i * 16)
        dut.compress_valid.value = 1
        await RisingEdge(dut.clk)
        dut.compress_valid.value = 0

        # Wait for completion
        if not await wait_for_compress_done(dut, timeout=50):
            dut._log.error(f"Test {test_num}: Compression did not complete")
            continue

        # Capture outputs
        compressed_out = []
        for i in range(4):
            val = signed_to_int((dut.compressed_out.value >> (i * 8)) & 0xFF, 8)
            compressed_out.append(val)
        scale_out = dut.scale_out.value & 0xFF

        # Compare with golden model
        golden_compressed, golden_scale, _, _ = activation_compressor_golden(test_data)

        test_passed = True
        if compressed_out != golden_compressed:
            dut._log.error(
                f"Test {test_num}: Compression mismatch: got {compressed_out}, expected {golden_compressed}"
            )
            test_passed = False
        if scale_out != golden_scale:
            dut._log.error(
                f"Test {test_num}: Scale mismatch: got {scale_out}, expected {golden_scale}"
            )
            test_passed = False

        if test_passed:
            pass_count += 1
            if test_num % 20 == 0:  # Log every 20th pass to reduce output
                dut._log.info(f"Test {test_num}: PASS")
        else:
            dut._log.error(f"Test {test_num}: FAIL - data={test_data}")
            dut._log.error(f"  Got: compressed={compressed_out}, scale={scale_out}")
            dut._log.error(
                f"  Expected: compressed={golden_compressed}, scale={golden_scale}"
            )

    dut._log.info(f"Random test results: {pass_count}/{num_tests} passed")

    # Also test decompression with random data
    pass_count_decomp = 0
    for test_num in range(num_tests):
        # Generate random compressed data and scale
        compressed_data = [random.randint(-128, 127) for _ in range(4)]
        scale_data = random.randint(1, 16)

        # Apply input for decompression
        dut.compressed_in.value = 0
        for i, val in enumerate(compressed_data):
            dut.compressed_in.value |= int_to_signed(val, 8) << (i * 8)
        dut.scale_in.value = scale_data & 0xFF
        dut.decompress_valid.value = 1
        await RisingEdge(dut.clk)
        dut.decompress_valid.value = 0

        # Wait for completion
        if not await wait_for_decompress_done(dut, timeout=50):
            dut._log.error(f"Decompression test {test_num}: Did not complete")
            continue

        # Capture outputs
        decompressed_out = []
        for i in range(4):
            val = signed_to_int((dut.decompressed_out.value >> (i * 16)) & 0xFFFF, 16)
            decompressed_out.append(val)

        # Compare with golden model
        golden_decompressed = activation_decompressor_golden(
            compressed_data, scale_data
        )

        if decompressed_out == golden_decompressed:
            pass_count_decomp += 1
            if test_num % 20 == 0:
                dut._log.info(f"Decompression test {test_num}: PASS")
        else:
            dut._log.error(f"Decompression test {test_num}: FAIL")
            dut._log.error(f"  Got: {decompressed_out}")
            dut._log.error(f"  Expected: {golden_decompressed}")

    dut._log.info(
        f"Random decompression test results: {pass_count_decomp}/{num_tests} passed"
    )

    # Final check
    if pass_count == num_tests and pass_count_decomp == num_tests:
        dut._log.info("============================================")
        dut._log.info("  ALL RANDOM TESTS PASSED")
        dut._log.info("============================================")
        return True
    else:
        dut._log.error("============================================")
        dut._log.error("  SOME RANDOM TESTS FAILED")
        dut._log.error("============================================")
        return False
