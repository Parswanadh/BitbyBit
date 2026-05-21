"""
Simple testbench for exp_lut_256 comparing RTL with golden model.
"""

import sys
import os
import random

# Add the project root to the path so we can import from verification/golden_models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from golden_models.exp_lut_256 import exp_lut_256_golden


def simulate_exp_lut_256_rtl(x_in):
    """
    Simplified RTL simulation model for exp_lut_256.
    """
    # Internal LUT (same as in golden model)
    lut = [
        255,
        251,
        247,
        243,
        240,
        236,
        232,
        229,
        225,
        222,
        218,
        215,
        211,
        208,
        205,
        202,
        199,
        196,
        192,
        189,
        187,
        184,
        181,
        178,
        175,
        173,
        170,
        167,
        165,
        162,
        160,
        157,
        155,
        152,
        150,
        148,
        145,
        143,
        141,
        139,
        136,
        134,
        132,
        130,
        128,
        126,
        124,
        122,
        120,
        119,
        117,
        115,
        113,
        111,
        110,
        108,
        106,
        105,
        103,
        101,
        100,
        98,
        97,
        95,
        94,
        92,
        91,
        90,
        88,
        87,
        85,
        84,
        83,
        82,
        80,
        79,
        78,
        77,
        75,
        74,
        73,
        72,
        71,
        70,
        69,
        68,
        67,
        65,
        64,
        63,
        62,
        62,
        61,
        60,
        59,
        58,
        57,
        56,
        55,
        54,
        53,
        53,
        52,
        51,
        50,
        49,
        49,
        48,
        47,
        46,
        46,
        45,
        44,
        44,
        43,
        42,
        42,
        41,
        40,
        40,
        39,
        38,
        38,
        37,
        37,
        36,
        36,
        36,
        35,
        35,
        34,
        33,
        33,
        32,
        32,
        31,
        31,
        30,
        30,
        30,
        29,
        29,
        28,
        28,
        27,
        27,
        26,
        26,
        26,
        25,
        25,
        24,
        24,
        24,
        23,
        23,
        23,
        22,
        22,
        22,
        21,
        21,
        21,
        20,
        20,
        20,
        19,
        19,
        19,
        19,
        18,
        18,
        18,
        18,
        17,
        17,
        17,
        17,
        16,
        16,
        16,
        16,
        15,
        15,
        15,
        15,
        14,
        14,
        14,
        14,
        14,
        13,
        13,
        13,
        13,
        13,
        12,
        12,
        12,
        12,
        12,
        12,
        12,
        11,
        11,
        11,
        11,
        11,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        8,
        8,
        8,
        8,
        8,
        8,
        8,
        8,
        7,
        7,
        7,
        7,
        7,
        7,
        7,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
    ]

    # Convert Q8.8 input to LUT index (matching RTL)
    # x_in is <= 0 after max-subtraction (as per RTL comment)
    # index = clamp(-x_in >> 2, 0, 255)

    neg_x = -x_in
    shifted = neg_x >> 2  # Arithmetic right shift

    # Clamp to [0, 255]
    if shifted > 255:
        idx = 255
    elif neg_x < 0:  # This means x_in > 0, which shouldn't happen per RTL comment
        idx = 0
    else:
        idx = shifted & 0xFF  # Take lower 8 bits

    # Return LUT value
    return lut[idx]


# Global lut for debug output
lut = [
    255,
    251,
    247,
    243,
    240,
    236,
    232,
    229,
    225,
    222,
    218,
    215,
    211,
    208,
    205,
    202,
    199,
    196,
    192,
    189,
    187,
    184,
    181,
    178,
    175,
    173,
    170,
    167,
    165,
    162,
    160,
    157,
    155,
    152,
    150,
    148,
    145,
    143,
    141,
    139,
    136,
    134,
    132,
    130,
    128,
    126,
    124,
    122,
    120,
    119,
    117,
    115,
    113,
    111,
    110,
    108,
    106,
    105,
    103,
    101,
    100,
    98,
    97,
    95,
    94,
    92,
    91,
    90,
    88,
    87,
    85,
    84,
    83,
    82,
    80,
    79,
    78,
    77,
    75,
    74,
    73,
    72,
    71,
    70,
    69,
    68,
    67,
    65,
    64,
    63,
    62,
    62,
    61,
    60,
    59,
    58,
    57,
    56,
    55,
    54,
    53,
    53,
    52,
    51,
    50,
    49,
    49,
    48,
    47,
    46,
    46,
    45,
    44,
    44,
    43,
    42,
    42,
    41,
    40,
    40,
    39,
    38,
    38,
    37,
    37,
    36,
    36,
    36,
    35,
    35,
    34,
    33,
    33,
    32,
    32,
    31,
    31,
    30,
    30,
    30,
    29,
    29,
    28,
    28,
    27,
    27,
    26,
    26,
    26,
    25,
    25,
    24,
    24,
    24,
    23,
    23,
    23,
    22,
    22,
    22,
    21,
    21,
    21,
    20,
    20,
    20,
    19,
    19,
    19,
    19,
    18,
    18,
    18,
    18,
    17,
    17,
    17,
    17,
    16,
    16,
    16,
    16,
    15,
    15,
    15,
    15,
    14,
    14,
    14,
    14,
    14,
    13,
    13,
    13,
    13,
    13,
    12,
    12,
    12,
    12,
    12,
    12,
    12,
    11,
    11,
    11,
    11,
    11,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    10,
    9,
    9,
    9,
    9,
    9,
    9,
    9,
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    8,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    5,
]


def test_exp_lut_256_basic():
    """Basic test for exp_lut_256"""
    print("=" * 60)
    print("Testing exp_lut_256 - Basic Tests")
    print("=" * 60)

    # Test cases covering the full range
    test_cases = [
        # (x_in, description)
        (0, "Zero input"),
        (-64, "-64 (k=16)"),
        (-128, "-128 (k=32)"),
        (-256, "-256 (k=64)"),
        (-512, "-512 (k=128)"),
        (-1024, "-1024 (k=256)"),
        (-1025, "-1025 (should clamp to k=255)"),
        (-2000, "-2000 (should clamp to k=255)"),
        (64, "64 (positive - should clamp to k=0 per RTL comment)"),
        (100, "100 (positive - should clamp to k=0)"),
    ]

    all_passed = True

    for x_in, desc in test_cases:
        print(f"\nTest: {desc}")
        print(f"  Input x_in = {x_in}")

        # RTL simulation
        rtl_result = simulate_exp_lut_256_rtl(x_in)
        print(f"  RTL Output: exp_out = {rtl_result}")

        # Golden model
        golden_result = exp_lut_256_golden(x_in)
        print(f"  Golden Output: exp_out = {golden_result}")

        # Check match
        if rtl_result == golden_result:
            print("  [PASS]")
        else:
            print("  [FAIL]")
            all_passed = False

        # Show the calculation for debugging
        neg_x = -x_in
        shifted = neg_x >> 2
        if shifted > 255:
            idx = 255
        elif neg_x < 0:
            idx = 0
        else:
            idx = shifted & 0xFF
        print(
            f"    Debug: neg_x={neg_x}, shifted={shifted}, idx={idx}, LUT[{idx}]={lut[idx]}"
        )

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 60)

    return all_passed


def test_exp_lut_256_random(num_tests=100):
    """Randomized test for exp_lut_256"""
    print("\n" + "=" * 60)
    print(f"Running {num_tests} Random Tests")
    print("=" * 60)

    pass_count = 0

    for test_num in range(num_tests):
        # Generate random test data covering a wide range
        # Include both negative and positive values to test clamping
        if random.random() < 0.7:  # 70% negative (normal operation)
            x_in = random.randint(-2048, 0)  # Wide negative range
        else:  # 30% positive (testing clamping)
            x_in = random.randint(0, 2048)  # Positive values

        # RTL simulation
        rtl_result = simulate_exp_lut_256_rtl(x_in)

        # Golden model
        golden_result = exp_lut_256_golden(x_in)

        # Check match
        if rtl_result == golden_result:
            pass_count += 1
            if test_num % 20 == 0:  # Log every 20th pass
                print(
                    f"Test {test_num:3d}: PASS - x_in={x_in:5d} -> exp_out={rtl_result}"
                )
        else:
            print(f"Test {test_num:3d}: FAIL - x_in={x_in:5d}")
            print(f"  RTL:    exp_out={rtl_result}")
            print(f"  Golden: exp_out={golden_result}")

            # Show the calculation for debugging
            neg_x = -x_in
            shifted = neg_x >> 2
            if shifted > 255:
                idx = 255
            elif neg_x < 0:
                idx = 0
            else:
                idx = shifted & 0xFF
            print(f"    Debug: neg_x={neg_x}, shifted={shifted}, idx={idx}")

    print(f"\nRandom test results: {pass_count}/{num_tests} passed")

    overall_pass = pass_count == num_tests
    print(f"Overall random tests: {'ALL PASSED' if overall_pass else 'SOME FAILED'}")

    return overall_pass


if __name__ == "__main__":
    # Run basic tests
    basic_result = test_exp_lut_256_basic()

    # Run random tests
    random_result = test_exp_lut_256_random(num_tests=50)

    # Final result
    if basic_result and random_result:
        print("\n🎉 ALL EXP_LUT_256 VERIFICATION TESTS PASSED!")
        exit(0)
    else:
        print("\n❌ SOME EXP_LUT_256 VERIFICATION TESTS FAILED!")
        exit(1)
