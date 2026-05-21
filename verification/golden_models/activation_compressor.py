"""
Bit-exact golden model for activation_compressor module.
"""


class ActivationCompressorGolden:
    def __init__(self, vector_len=4, data_width=16):
        self.vector_len = vector_len
        self.data_width = data_width
        self.total_compressions = 0
        self.total_bytes_saved = 0

    def compress(self, data_in):
        """
        Compress Q8.8 (16-bit) activations to 8-bit + scale factor.

        Args:
            data_in: list of integers representing Q8.8 values (signed)

        Returns:
            tuple: (compressed_out, scale_out)
                compressed_out: list of 8-bit integers
                scale_out: 8-bit scale factor
        """
        if len(data_in) != self.vector_len:
            raise ValueError(f"Expected {self.vector_len} values, got {len(data_in)}")

        # Step 1: Find absolute max
        abs_max = 0
        for val in data_in:
            abs_val = abs(val)
            if abs_val > abs_max:
                abs_max = abs_val

        # Step 2: Compute scale factor
        if abs_max > 127:  # 16'sd127
            scale_out = abs_max >> (self.data_width - 8)  # abs_max[15:7] for 16-bit
        else:
            scale_out = 1

        # Step 3: Quantize each element
        compressed_out = []
        for val in data_in:
            if abs_max > 127:
                # Shift-based quantization: val >> (data_width - 8)
                compressed_val = val >> (self.data_width - 8)
            else:
                compressed_val = val & 0xFF  # Lower 8 bits
            # Ensure 8-bit signed representation
            if compressed_val >= 128:
                compressed_val -= 256
            compressed_out.append(compressed_val)

        # Update counters
        self.total_compressions += 1
        self.total_bytes_saved += self.vector_len

        return compressed_out, scale_out

    def decompress(self, compressed_in, scale_in):
        """
        Decompress 8-bit + scale factor back to Q8.8 (16-bit).

        Args:
            compressed_in: list of 8-bit integers (signed)
            scale_in: 8-bit scale factor

        Returns:
            list: decompressed Q8.8 values (signed)
        """
        if len(compressed_in) != self.vector_len:
            raise ValueError(
                f"Expected {self.vector_len} values, got {len(compressed_in)}"
            )

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

    def get_counters(self):
        return self.total_compressions, self.total_bytes_saved

    def reset_counters(self):
        self.total_compressions = 0
        self.total_bytes_saved = 0


def activation_compressor_golden(data_in, vector_len=4, data_width=16):
    """
    Functional golden model for activation_compressor (single-shot).

    Args:
        data_in: list of integers representing Q8.8 values (signed)
        vector_len: length of input vector
        data_width: width of input data (should be 16)

    Returns:
        tuple: (compressed_out, scale_out, total_compressions, total_bytes_saved)
    """
    model = ActivationCompressorGolden(vector_len, data_width)
    compressed_out, scale_out = model.compress(data_in)
    total_compressions, total_bytes_saved = model.get_counters()
    return compressed_out, scale_out, total_compressions, total_bytes_saved


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
    model = ActivationCompressorGolden(vector_len, data_width)
    decompressed_out = model.decompress(compressed_in, scale_in)
    return decompressed_out


if __name__ == "__main__":
    # Simple test
    print("Testing activation compressor golden model...")

    # Test 1: Small values
    data_in = [50, 30, 20, 10]
    compressed, scale, comp_count, bytes_saved = activation_compressor_golden(data_in)
    print(f"Input: {data_in}")
    print(f"Compressed: {compressed}, Scale: {scale}")
    print(f"Compressions: {comp_count}, Bytes saved: {bytes_saved}")

    # Test 2: Large values
    data_in = [1024, 512, 256, 128]
    compressed, scale, comp_count, bytes_saved = activation_compressor_golden(data_in)
    print(f"\nInput: {data_in}")
    print(f"Compressed: {compressed}, Scale: {scale}")
    print(f"Compressions: {comp_count}, Bytes saved: {bytes_saved}")

    # Test 3: Decompression
    decompressed = activation_decompressor_golden(compressed, scale)
    print(f"\nDecompressed: {decompressed}")
    print(f"Original: {data_in}")

    # Check accuracy
    error = [abs(orig - dec) for orig, dec in zip(data_in, decompressed)]
    print(f"Errors: {error}")
    print(f"Max error: {max(error)}")
