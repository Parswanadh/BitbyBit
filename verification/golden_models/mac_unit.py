"""
Bit-exact golden model for mac_unit module.
"""


class MACUnitGolden:
    def __init__(self, data_width=16, acc_width=32):
        self.data_width = data_width
        self.acc_width = acc_width
        self.acc_out = 0
        self.valid_out = 0

    def mac_operation(self, a, b, valid_in, clear_acc, rst):
        """
        Perform MAC operation matching RTL behavior.

        Args:
            a, b: signed integers (Q8.8 format)
            valid_in: boolean indicating valid input
            clear_acc: boolean to clear accumulator
            rst: boolean reset

        Returns:
            tuple: (acc_out, valid_out)
        """
        # Handle reset
        if rst:
            self.acc_out = 0
            self.valid_out = 0
            return self.acc_out, self.valid_out

        # Handle clear accumulator
        if clear_acc:
            self.acc_out = 0
            # valid_out will be set based on valid_in below

        # Perform MAC if valid_in
        if valid_in:
            # Check for zero
            is_zero = (a == 0) or (b == 0)

            if not is_zero:
                # Calculate product
                product = a * b  # This gives Q16.16 result

                # Sign-extend product to accumulator width
                # For Q8.8 * Q8.8 = Q16.16, we need to extend to Q32.32 conceptually
                # But since acc_width=32, we're dealing with integer representation
                product_ext = product  # Already sign-extended in Python

                # Calculate sum
                sum_result = self.acc_out + product_ext

                # Overflow detection (saturating arithmetic)
                max_pos = (1 << (self.acc_width - 1)) - 1
                max_neg = -(1 << (self.acc_width - 1))

                if sum_result > max_pos:
                    self.acc_out = max_pos  # Saturate to max positive
                elif sum_result < max_neg:
                    self.acc_out = max_neg  # Saturate to max negative
                else:
                    self.acc_out = sum_result

            # valid_out is set when valid_in is received (regardless of zero)
            self.valid_out = 1
        else:
            self.valid_out = 0

        return self.acc_out, self.valid_out

    def get_state(self):
        return self.acc_out, self.valid_out

    def reset(self):
        self.acc_out = 0
        self.valid_out = 0


def mac_unit_golden(a, b, valid_in, clear_acc, rst, data_width=16, acc_width=32):
    """
    Functional golden model for MAC unit (single-shot).

    Args:
        a, b: signed integers (Q8.8 format)
        valid_in: boolean indicating valid input
        clear_acc: boolean to clear accumulator
        rst: boolean reset
        data_width: width of input data (default 16 for Q8.8)
        acc_width: width of accumulator (default 32)

    Returns:
        tuple: (acc_out, valid_out)
    """
    mac = MACUnitGolden(data_width, acc_width)
    return mac.mac_operation(a, b, valid_in, clear_acc, rst)


if __name__ == "__main__":
    # Simple test
    print("Testing MAC unit golden model...")

    # Test 1: Basic MAC operation
    print("\nTest 1: Basic MAC")
    acc, valid = mac_unit_golden(10, 20, valid_in=1, clear_acc=0, rst=0)
    print(f"10 * 20 = 200, acc={acc}, valid={valid}")

    # Test 2: Another MAC operation (accumulation)
    acc, valid = mac_unit_golden(5, 5, valid_in=1, clear_acc=0, rst=0)
    print(f"5 * 5 = 25, acc={acc} (should be 225), valid={valid}")

    # Test 3: Clear accumulator
    acc, valid = mac_unit_golden(1, 1, valid_in=1, clear_acc=1, rst=0)
    print(f"Clear then 1 * 1 = 1, acc={acc}, valid={valid}")

    # Test 4: Reset
    acc, valid = mac_unit_golden(10, 10, valid_in=1, clear_acc=0, rst=1)
    print(f"Reset then 10 * 10 = 100, acc={acc}, valid={valid}")

    # Test 5: Zero detection
    acc, valid = mac_unit_golden(0, 10, valid_in=1, clear_acc=0, rst=0)
    print(f"0 * 10 = 0 (should skip), acc={acc}, valid={valid}")

    # Test 6: Negative numbers
    acc, valid = mac_unit_golden(-5, 6, valid_in=1, clear_acc=0, rst=0)
    print(f"-5 * 6 = -30, acc={acc}, valid={valid}")

    acc, valid = mac_unit_golden(-5, -6, valid_in=1, clear_acc=0, rst=0)
    print(f"-5 * -6 = 30, acc={acc}, valid={valid}")

    # Test 7: Overflow
    acc, valid = mac_unit_golden(1000, 1000, valid_in=1, clear_acc=0, rst=0)
    print(f"1000 * 1000 = 1,000,000 (should overflow), acc={acc}, valid={valid}")
