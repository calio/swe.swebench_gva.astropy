#!/usr/bin/env python3
"""Direct test of float16 dtype preservation logic."""

import numpy as np

print("Testing float16 dtype preservation logic...")
print("=" * 60)

# Simulate the fixed unit_scale_converter logic
def unit_scale_converter_fixed(val):
    """Fixed version that preserves dtype."""
    if hasattr(val, 'dtype') and val.dtype.kind == 'f':
        # For floating point types, cast 1. to the same dtype
        return val.dtype.type(1.) * val
    else:
        return 1. * val

# Simulate the old broken version
def unit_scale_converter_broken(val):
    """Old broken version."""
    return 1. * val

# Test 1: float16 scalar
print("\nTest 1: float16 scalar")
f16_scalar = np.float16(1)
result_broken = unit_scale_converter_broken(f16_scalar)
result_fixed = unit_scale_converter_fixed(f16_scalar)
print(f"Input: {f16_scalar}, dtype: {f16_scalar.dtype}")
print(f"Broken version: dtype={result_broken.dtype}")
print(f"Fixed version: dtype={result_fixed.dtype}")
assert result_fixed.dtype == np.float16, f"Expected float16, got {result_fixed.dtype}"
print("✓ PASSED")

# Test 2: float16 array
print("\nTest 2: float16 array")
f16_array = np.array([1., 2.], dtype=np.float16)
result_broken = unit_scale_converter_broken(f16_array)
result_fixed = unit_scale_converter_fixed(f16_array)
print(f"Input: {f16_array}, dtype: {f16_array.dtype}")
print(f"Broken version: dtype={result_broken.dtype}")
print(f"Fixed version: dtype={result_fixed.dtype}")
assert result_fixed.dtype == np.float16, f"Expected float16, got {result_fixed.dtype}"
print("✓ PASSED")

# Test 3: float32 scalar
print("\nTest 3: float32 scalar")
f32_scalar = np.float32(1)
result_fixed = unit_scale_converter_fixed(f32_scalar)
print(f"Input: {f32_scalar}, dtype: {f32_scalar.dtype}")
print(f"Fixed version: dtype={result_fixed.dtype}")
assert result_fixed.dtype == np.float32, f"Expected float32, got {result_fixed.dtype}"
print("✓ PASSED")

# Test 4: float64 scalar
print("\nTest 4: float64 scalar")
f64_scalar = np.float64(1)
result_fixed = unit_scale_converter_fixed(f64_scalar)
print(f"Input: {f64_scalar}, dtype: {f64_scalar.dtype}")
print(f"Fixed version: dtype={result_fixed.dtype}")
assert result_fixed.dtype == np.float64, f"Expected float64, got {result_fixed.dtype}"
print("✓ PASSED")

# Test 5: integer scalar (should still work)
print("\nTest 5: integer scalar")
int_scalar = 1
result_fixed = unit_scale_converter_fixed(int_scalar)
print(f"Input: {int_scalar}, type: {type(int_scalar)}")
print(f"Fixed version: {result_fixed}")
print("✓ PASSED")

# Test 6: scale_converter with non-unity scale
print("\nTest 6: scale_converter with non-unity scale")
def scale_converter_fixed(val, scale):
    """Fixed version that preserves dtype."""
    if hasattr(val, 'dtype') and val.dtype.kind == 'f':
        # For floating point types, cast scale to the same dtype
        return val.dtype.type(scale) * val
    else:
        return scale * val

f16_scalar = np.float16(1)
result = scale_converter_fixed(f16_scalar, 2.0)
print(f"Input: {f16_scalar}, dtype: {f16_scalar.dtype}, scale: 2.0")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
assert result == 2.0, f"Expected 2.0, got {result}"
print("✓ PASSED")

print("\n" + "=" * 60)
print("All tests passed! ✓")
