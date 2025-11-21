"""Simple test to verify the fix works"""
import sys
import os

# Add the repo to the path
sys.path.insert(0, '/Users/calio/work/astropy__astropy-13977')

# Now test the fix
import dataclasses
import numpy as np

# Import units directly
from astropy.units import Quantity, m, mm

@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    """A duck type of astropy.units.Quantity for testing."""
    ndarray: Quantity

    @property
    def unit(self):
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):
        inputs = [inp.ndarray if isinstance(inp, DuckArray) else inp for inp in inputs]

        for inp in inputs:
            if isinstance(inp, np.ndarray):
                result = inp.__array_ufunc__(function, method, *inputs, **kwargs)
                if result is not NotImplemented:
                    return DuckArray(result)

        return NotImplemented


def test_duck_array_with_quantity_different_units():
    """Test Quantity + DuckArray with different but compatible units.
    
    This should work by calling DuckArray.__radd__ after Quantity.__array_ufunc__
    returns NotImplemented.
    """
    print("Test: Quantity(1 m) + DuckArray(1 mm) - SHOULD WORK")
    try:
        result = (1 * m) + DuckArray(1 * mm)
        print(f"  Result: {result}")
        print(f"  Result type: {type(result)}")
        assert isinstance(result, DuckArray), f"Expected DuckArray, got {type(result)}"
        print("  PASSED\n")
        return True
    except Exception as e:
        print(f"  FAILED with {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_duck_array_with_quantity_different_units()
    sys.exit(0 if success else 1)
