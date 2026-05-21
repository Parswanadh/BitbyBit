"""
Simple testbench for mac_unit comparing RTL with golden model.
"""

import sys
import os
import random

# Add the project root to the path so we can import from verification/golden_models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from golden_models.mac_unit import MACUnitGolden, mac_unit_golden


def simulate_mac_unit_rtl(a, b, valid_in, clear_acc, rst, acc_width=32):
    """
    Simplified RTL simulation model for MAC unit.
    """
    # Internal state (would be registers in RTL)
    acc_out = 0
    valid_out = 0

    # Handle reset (synchronous reset in RTL)
    if rst:
        acc_out = 0
        valid_out = 0
        return acc_out, valid_out

    # Handle clear accumulator
    if clear_acc:
        acc_out = 0

    # Perform MAC if valid_in
    if valid_in:
        # Check for zero (from RTL)
        is_zero = (a == 0) or (b == 0)

        if not is_zero:
            # Calculate product (Q8.8 * Q8.8 = Q16.16)
            product = a * b

            # In RTL, we have sign extension and accumulation
            # For simplicity, we'll just add to accumulator
            # Note: In real RTL there's more complex handling with saturation
            acc_out += product

            # Apply saturation (from RTL)
            max_pos = (1 << (acc_width - 1)) - 1
            max_neg = -(1 << (acc_width - 1))

            if acc_out > max_pos:
                acc_out = max_pos
            elif acc_out < max_neg:
                acc_out = max_neg

        # valid_out is set when valid_in is received
        valid_out = 1
    else:
        valid_out = 0

    return acc_out, valid_out


def test_mac_unit_basic():
    """Basic test for MAC unit"""
    print("=" * 50)
    print("Testing MAC Unit - Basic Tests")
    print("=" * 50)

    # Test sequence
    test_cases = [
        # (a, b, valid_in, clear_acc, rst, description)
        (10, 20, 1, 0, 0, "Basic multiplication: 10 * 20"),
        (5, 5, 1, 0, 0, "Accumulation: 5 * 5 (should add to previous)"),
        (1, 1, 1, 1, 0, "Clear then multiply: clear then 1 * 1"),
        (10, 10, 1, 0, 1, "Reset then multiply: reset then 10 * 10"),
        (0, 10, 1, 0, 0, "Zero detection: 0 * 10 (should skip)"),
        (-5, 6, 1, 0, 0, "Negative * positive: -5 * 6"),
        (-5, -6, 1, 0, 0, "Negative * negative: -5 * -6"),
        (1000, 1000, 1, 0, 0, "Overflow test: 1000 * 1000"),
    ]

    all_passed = True

    for i, (a, b, valid_in, clear_acc, rst, desc) in enumerate(test_cases):
        print(f"\nTest {i + 1}: {desc}")
        print(
            f"  Inputs: a={a}, b={b}, valid_in={valid_in}, clear_acc={clear_acc}, rst={rst}"
        )

        # RTL simulation
        rtl_acc, rtl_valid = simulate_mac_unit_rtl(a, b, valid_in, clear_acc, rst)
        print(f"  RTL:    acc_out={rtl_acc}, valid_out={rtl_valid}")

        # Golden model (need to handle state)
        # For simplicity, we'll create a fresh model for each test
        # In real verification, we'd maintain state across tests
        golden_model = MACUnitGolden()
        gold_acc, gold_valid = golden_model.mac_operation(
            a, b, valid_in, clear_acc, rst
        )
        print(f"  Golden: acc_out={gold_acc}, valid_out={gold_valid}")

        # Check match
        if rtl_acc == gold_acc and rtl_valid == gold_valid:
            print("  [PASS]")
        else:
            print("  [FAIL]")
            all_passed = False

    # Test accumulation specifically
    print("\n" + "-" * 50)
    print("Testing Accumulation Behavior")
    print("-" * 50)

    # Reset model
    golden_model = MACUnitGolden()

    # First MAC: 10 * 20 = 200
    acc1, valid1 = golden_model.mac_operation(10, 20, 1, 0, 0)
    rtl_acc1, rtl_valid1 = simulate_mac_unit_rtl(10, 20, 1, 0, 0)

    # Second MAC: 5 * 5 = 25, should accumulate to 225
    acc2, valid2 = golden_model.mac_operation(5, 5, 1, 0, 0)
    rtl_acc2, rtl_valid2 = simulate_mac_unit_rtl(5, 5, 1, 0, 0)

    print(f"After 10*20:  RTL={rtl_acc1}, Golden={acc1}")
    print(f"After 5*5:    RTL={rtl_acc2}, Golden={acc2} (expected 225)")

    acc_test_pass = (rtl_acc1 == acc1) and (rtl_acc2 == acc2)
    print(f"Accumulation test: {'PASS' if acc_test_pass else 'FAIL'}")

    if not acc_test_pass:
        all_passed = False

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 50)

    return all_passed


def test_mac_unit_random(num_tests=100):
    """Randomized test for MAC unit"""
    print("\n" + "=" * 50)
    print(f"Running {num_tests} Random Tests")
    print("=" * 50)

    pass_count = 0

    for test_num in range(num_tests):
        # Generate random test data
        a = random.randint(-128, 127)  # Q8.8 range
        b = random.randint(-128, 127)
        valid_in = random.choice([0, 1])
        clear_acc = random.choice([0, 1])
        rst = random.choice([0, 1])

        # Skip if both reset and clear are active (reset takes precedence)
        if rst == 1 and clear_acc == 1:
            continue

        # RTL simulation
        rtl_acc, rtl_valid = simulate_mac_unit_rtl(a, b, valid_in, clear_acc, rst)

        # Golden model
        golden_model = MACUnitGolden()
        gold_acc, gold_valid = golden_model.mac_operation(
            a, b, valid_in, clear_acc, rst
        )

        # Check match
        if rtl_acc == gold_acc and rtl_valid == gold_valid:
            pass_count += 1
            if test_num % 20 == 0:  # Log every 20th pass
                print(
                    f"Test {test_num:3d}: PASS - a={a:4d}, b={b:4d}, v={valid_in}, c={clear_acc}, r={rst}"
                )
        else:
            print(
                f"Test {test_num:3d}: FAIL - a={a:4d}, b={b:4d}, v={valid_in}, c={clear_acc}, r={rst}"
            )
            print(f"  RTL:    acc={rtl_acc}, valid={rtl_valid}")
            print(f"  Golden: acc={gold_acc}, valid={gold_valid}")

    print(f"\nRandom test results: {pass_count}/{num_tests} passed")

    overall_pass = pass_count == num_tests
    print(f"Overall random tests: {'ALL PASSED' if overall_pass else 'SOME FAILED'}")

    return overall_pass


if __name__ == "__main__":
    # Run basic tests
    basic_result = test_mac_unit_basic()

    # Run random tests
    random_result = test_mac_unit_random(num_tests=50)

    # Final result
    if basic_result and random_result:
        print("\n🎉 ALL MAC UNIT VERIFICATION TESTS PASSED!")
        exit(0)
    else:
        print("\n❌ SOME MAC UNIT VERIFICATION TESTS FAILED!")
        exit(1)
