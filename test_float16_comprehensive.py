#!/usr/bin/env python3
"""Comprehensive test for float16 dtype preservation in unit conversions."""

import numpy as np
import sys
sys.path.insert(0, '.')

# Test the core functions directly
from astropy.units.core import unit_scale_converter, _condition_arg

print("Testing float16 dtype preservation in unit conversions...")
print("=" * 60)

# Test 1: unit_scale_converter with float16 scalar
print("\nTest 1: unit_scale_converter with float16 scalar")
f16_scalar = np.float16(1)
result = unit_scale_converter(f16_scalar)
print(f"Input: {f16_scalar}, dtype: {f16_scalar.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

# Test 2: unit_scale_converter with float16 array
print("\nTest 2: unit_scale_converter with float16 array")
f16_array = np.array([1., 2.], dtype=np.float16)
result = unit_scale_converter(f16_array)
print(f"Input: {f16_array}, dtype: {f16_array.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float16, f"Expected float16, got {result.dtype}"
print("✓ PASSED")

# Test 3: unit_scale_converter with float32 (should still work)
print("\nTest 3: unit_scale_converter with float32")
f32_scalar = np.float32(1)
result = unit_scale_converter(f32_scalar)
print(f"Input: {f32_scalar}, dtype: {f32_scalar.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float32, f"Expected float32, got {result.dtype}"
print("✓ PASSED")

# Test 4: unit_scale_converter with float64 (should still work)
print("\nTest 4: unit_scale_converter with float64")
f64_scalar = np.float64(1)
result = unit_scale_converter(f64_scalar)
print(f"Input: {f64_scalar}, dtype: {f64_scalar.dtype}")
print(f"Result: {result}, dtype: {result.dtype}")
assert result.dtype == np.float64, f"Expected float64, got {result.dtype}"
print("✓ PASSED")

# Test 5: unit_scale_converter with integer (should still work)
print("\nTest 5: unit_scale_converter with integer")
int_scalar = 1
result = unit_scale_converter(int_scalar)
print(f"Input: {int_scalar}, type: {type(int_scalar)}")
print(f"Result: {result}, dtype: {result.dtype if hasattr(result, 'dtype') else type(result)}")
print("✓ PASSED")

print("\n" + "=" * 60)
print("All tests passed! ✓")
