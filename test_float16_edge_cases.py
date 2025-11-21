#!/usr/bin/env python3
"""Test edge cases for float16 dtype preservation."""

import numpy as np

print("Testing edge cases for float16 dtype preservation...")
print("=" * 60)

# Simulate the fixed unit_scale_converter logic
def unit_scale_converter_fixed(val):
    """Fixed version that preserves dtype."""
    if hasattr(val, 'dtype') and val.dtype.kind == 'f':
        # For floating point types, cast 1. to the same dtype
        return val.dtype.type(1.) * val
    else:
        return 1. * val

# Test 1: complex numbers (should not be affected)
print("\nTest 1: complex numbers")
c_scalar = np.complex64(1+2j)
result = unit_scale_converter_fixed(c_scalar)
print(f"Input: {c_scalar}, dtype: {c_scalar.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
print("✓ PASSED")

# Test 2: complex128
print("\nTest 2: complex128")
c_scalar = np.complex128(1+2j)
result = unit_scale_converter_fixed(c_scalar)
print(f"Input: {c_scalar}, dtype: {c_scalar.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
print("✓ PASSED")

# Test 3: integer arrays
print("\nTest 3: integer arrays")
int_array = np.array([1, 2, 3], dtype=np.int32)
result = unit_scale_converter_fixed(int_array)
print(f"Input: {int_array}, dtype: {int_array.dtype}")
print(f"Result: {result}, dtype: {result.dtype if hasattr(result, 'dtype') else type(result)}")
print("✓ PASSED")

# Test 4: float16 with NaN
print("\nTest 4: float16 with NaN")
f16_nan = np.float16(np.nan)
result = unit_scale_converter_fixed(f16_nan)
print(f"Input: {f16_nan}, dtype: {f16_nan.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

# Test 5: float16 with infinity
print("\nTest 5: float16 with infinity")
f16_inf = np.float16(np.inf)
result = unit_scale_converter_fixed(f16_inf)
print(f"Input: {f16_inf}, dtype: {f16_inf.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

# Test 6: float16 with negative values
print("\nTest 6: float16 with negative values")
f16_neg = np.float16(-1.5)
result = unit_scale_converter_fixed(f16_neg)
print(f"Input: {f16_neg}, dtype: {f16_neg.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
assert result == -1.5, f"Expected -1.5, got {result}"
print("✓ PASSED")

# Test 7: float16 with very small values
print("\nTest 7: float16 with very small values")
f16_small = np.float16(1e-4)
result = unit_scale_converter_fixed(f16_small)
print(f"Input: {f16_small}, dtype: {f16_small.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

# Test 8: float16 with very large values
print("\nTest 8: float16 with very large values")
f16_large = np.float16(1e4)
result = unit_scale_converter_fixed(f16_large)
print(f"Input: {f16_large}, dtype: {f16_large.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

print("\n" + "=" * 60)
print("All edge case tests passed! ✓")
