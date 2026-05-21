"""
Bit-exact golden model for exp_lut_256 module.
"""


class ExpLUT256Golden:
    def __init__(self):
        # Initialize the LUT with the same values as in the RTL
        self.lut = [
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

    def exp_lut_operation(self, x_in):
        """
        Perform LUT lookup matching RTL behavior.

        Args:
            x_in: signed 16-bit integer (Q8.8 format, expected <= 0)

        Returns:
            exp_out: 8-bit unsigned integer (Q0.8 format [1,255])
        """
        # Convert Q8.8 input to LUT index
        # x_in is <= 0 after max-subtraction (as per RTL comment)
        # index = clamp(-x_in >> 2, 0, 255)

        neg_x = -x_in
        shifted = (
            neg_x >> 2
        )  # Arithmetic right shift (equivalent to >>> in Verilog for positive numbers)

        # Clamp to [0, 255]
        if shifted > 255:
            idx = 255
        elif neg_x < 0:  # This means x_in > 0, which shouldn't happen per RTL comment
            idx = 0
        else:
            idx = shifted & 0xFF  # Take lower 8 bits

        # Return LUT value
        return self.lut[idx]


def exp_lut_256_golden(x_in):
    """
    Functional golden model for exp_lut_256 (single-shot).

    Args:
        x_in: signed 16-bit integer (Q8.8 format, expected <= 0)

    Returns:
        exp_out: 8-bit unsigned integer (Q0.8 format [1,255])
    """
    lut_model = ExpLUT256Golden()
    return lut_model.exp_lut_operation(x_in)


if __name__ == "__main__":
    # Simple test
    print("Testing exp_lut_256 golden model...")

    # Test cases from the LUT definition
    test_cases = [
        (0, 255),  # exp(0) = 1 -> 255*1 = 255
        (-64, 251),  # exp(-1) ~ 0.367 -> 255*0.367 ~ 94, but LUT[1] = 251 (see comment)
        (-128, 225),  # exp(-2) ~ 0.135 -> 255*0.135 ~ 34
        (-256, 199),  # exp(-4) ~ 0.018 -> 255*0.018 ~ 4.6
        (-512, 94),  # exp(-8) ~ 0.0003 -> 255*0.0003 ~ 0.08 -> clamped to 1
        (-1024, 5),  # exp(-16) very small -> clamped to minimum 1
        (-1025, 5),  # Should clamp to 0 index -> LUT[0] = 255? Wait, let's check...
    ]

    print("Note: The LUT implements round(255 * exp(-k/64)) where k = -x_in >> 2")
    print("So x_in = 0 -> k = 0 -> LUT[0] = 255")
    print("   x_in = -64 -> k = 16 -> LUT[16] = 145")
    print()

    for x_in, expected in test_cases:
        result = exp_lut_256_golden(x_in)
        # Calculate expected k value for debugging
        neg_x = -x_in
        shifted = neg_x >> 2
        if shifted > 255:
            idx = 255
        elif neg_x < 0:
            idx = 0
        else:
            idx = shifted & 0xFF

        print(
            f"x_in = {x_in:4d} -> neg_x = {neg_x:4d} -> shifted = {shifted:4d} -> idx = {idx:3d} -> LUT[{idx}] = {result:3d} (expected ~{expected})"
        )
