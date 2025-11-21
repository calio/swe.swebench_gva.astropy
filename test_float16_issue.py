#!/usr/bin/env python3
"""Test script to reproduce the float16 dtype issue."""

import numpy as np
import sys
sys.path.insert(0, '.')

# Test the issue
print("Testing float16 dtype preservation in Quantity...")

# Test 1: Direct creation with float16 array
print("\nTest 1: Direct creation with float16 array")
a16 = np.array([1., 2.], dtype=np.float16)
print(f"Input array dtype: {a16.dtype}")

# We can't import astropy directly due to build issues, so let's test the core logic
# Test what happens with _condition_arg and multiplication

# Simulate what happens in Unit._get_converter
scale = 1.0
f16_scalar = np.float16(1)
print(f"\nTest 2: Multiplication with scale")
print(f"scale type: {type(scale)}, value: {scale}")
print(f"f16_scalar type: {type(f16_scalar)}, dtype: {f16_scalar.dtype}")

result = scale * f16_scalar
print(f"scale * f16_scalar: {result}, dtype: {result.dtype}")

# Test what _condition_arg does
print(f"\nTest 3: _condition_arg behavior")
print(f"isinstance(f16_scalar, (np.ndarray, float, int, complex, np.void)): {isinstance(f16_scalar, (np.ndarray, float, int, complex, np.void))}")

# If not in the list, it gets converted to array
avalue = np.array(f16_scalar)
print(f"np.array(f16_scalar): dtype={avalue.dtype}")

# Then multiplied by scale
result2 = scale * avalue
print(f"scale * np.array(f16_scalar): dtype={result2.dtype}")

print("\n" + "="*60)
print("ISSUE IDENTIFIED:")
print("When scale (float64) is multiplied by f16_scalar (float16),")
print("numpy promotes the result to float64!")
print("="*60)
