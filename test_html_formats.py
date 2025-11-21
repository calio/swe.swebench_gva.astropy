#!/usr/bin/env python3
"""
Test script to verify HTML formats fix
"""
import sys
sys.path.insert(0, '/Users/calio/work/astropy__astropy-13453')

from astropy.table import Table
from io import StringIO

# Create a table with small float values
t = Table([(1.23875234858e-24, 3.2348748432e-15), (2, 4)], names=('a', 'b'))

# Write with format specification for column 'a'
buffer_output = StringIO()
t.write(buffer_output, format='html', formats={'a': lambda x: f'{x:.2e}'})
output = buffer_output.getvalue()

print("=== HTML Output with formats ===")
print(output)
print("\n=== Checking for formatted values ===")
print(f"'1.24e-24' in output: {'1.24e-24' in output}")
print(f"'3.23e-15' in output: {'3.23e-15' in output}")
print(f"'1.23875234858e-24' in output: {'1.23875234858e-24' in output}")
print(f"'3.2348748432e-15' in output: {'3.2348748432e-15' in output}")

# Test passes if formatted values are present and unformatted are not
if '1.24e-24' in output and '3.23e-15' in output and '1.23875234858e-24' not in output and '3.2348748432e-15' not in output:
    print("\n✓ TEST PASSED: Formats are correctly applied!")
    sys.exit(0)
else:
    print("\n✗ TEST FAILED: Formats are not applied correctly")
    sys.exit(1)
