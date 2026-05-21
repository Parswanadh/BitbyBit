"""
Regression test runner for all verification testbenches.
"""

import sys
import os
import subprocess
import time


def run_testbench(testbench_path, testbench_name):
    """Run a single testbench and return success status."""
    print(f"\n{'=' * 60}")
    print(f"Running {testbench_name}")
    print(f"{'=' * 60}")

    start_time = time.time()

    try:
        # Change to the testbench directory
        testbench_dir = os.path.dirname(testbench_path)
        testbench_file = os.path.basename(testbench_path)

        # Run the testbench
        result = subprocess.run(
            [sys.executable, testbench_file],
            cwd=testbench_dir,
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
        )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Print output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        # Check if test passed
        success = "ALL TESTS PASSED" in result.stdout or (
            "ALL" in result.stdout and "PASSED" in result.stdout
        )

        print(
            f"\n{testbench_name}: {'PASS' if success else 'FAIL'} ({elapsed_time:.2f}s)"
        )
        return success

    except subprocess.TimeoutExpired:
        print(f"{testbench_name}: FAIL (timeout after 30s)")
        return False
    except Exception as e:
        print(f"{testbench_name}: FAIL (exception: {e})")
        return False


def main():
    """Run all verification testbenches."""
    print("BitbyBit Custom GPU - Verification Regression Suite")
    print("=" * 60)

    # Get the verification testbenches directory (one level up from regressions)
    verif_tb_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "testbenches"
    )

    # List of testbenches to run
    testbenches = [
        ("activation_compressor_tb_simple.py", "Activation Compressor"),
        ("mac_unit_tb_simple.py", "MAC Unit"),
        ("exp_lut_256_tb_simple.py", "exp_lut_256"),
        # Add more testbenches here as they are created
    ]

    # Run all testbenches
    results = []
    start_time = time.time()

    for testbench_file, testbench_name in testbenches:
        testbench_path = os.path.join(verif_tb_dir, testbench_file)
        if os.path.exists(testbench_path):
            success = run_testbench(testbench_path, testbench_name)
            results.append((testbench_name, success))
        else:
            print(f"\n{testbench_name}: SKIP (file not found)")
            results.append((testbench_name, False))

    end_time = time.time()
    total_time = end_time - start_time

    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION REGRESSION SUMMARY")
    print("=" * 60)

    passed = 0
    failed = 0

    for testbench_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{testbench_name:<25} {status}")
        if success:
            passed += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Total:  {len(results):<2}  Passed: {passed:<2}  Failed: {failed:<2}")
    print(f"Time:   {total_time:.2f} seconds")
    print("=" * 60)

    # Return appropriate exit code
    if failed == 0:
        print("\nALL VERIFICATION TESTS PASSED!")
        return 0
    else:
        print(f"\n{failed} VERIFICATION TEST(S) FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
