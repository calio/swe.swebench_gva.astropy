"""Test to reproduce the issue with Quantity.__array_ufunc__()"""
import dataclasses
import numpy as np
import astropy.units as u


@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    """A duck type of astropy.units.Quantity for testing."""
    ndarray: u.Quantity

    @property
    def unit(self) -> u.UnitBase:
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):
        inputs = [inp.ndarray if isinstance(inp, DuckArray) else inp for inp in inputs]

        for inp in inputs:
            if isinstance(inp, np.ndarray):
                result = inp.__array_ufunc__(function, method, *inputs, **kwargs)
                if result is not NotImplemented:
                    return DuckArray(result)

        return NotImplemented


def test_duck_array_with_quantity_same_units():
    """Test DuckArray + Quantity with same units."""
    print("Test 1: DuckArray(1 mm) + Quantity(1 mm)")
    result = DuckArray(1 * u.mm) + (1 * u.mm)
    print(f"  Result: {result}")
    assert isinstance(result, DuckArray)
    print("  PASSED\n")


def test_quantity_with_duck_array_same_units():
    """Test Quantity + DuckArray with same units."""
    print("Test 2: Quantity(1 mm) + DuckArray(1 mm)")
    result = (1 * u.mm) + DuckArray(1 * u.mm)
    print(f"  Result: {result}")
    assert isinstance(result, DuckArray)
    print("  PASSED\n")


def test_quantity_with_duck_array_different_units():
    """Test Quantity + DuckArray with different but compatible units.
    
    This should work by calling DuckArray.__radd__ after Quantity.__array_ufunc__
    returns NotImplemented.
    """
    print("Test 3: Quantity(1 m) + DuckArray(1 mm) - SHOULD WORK")
    try:
        result = (1 * u.m) + DuckArray(1 * u.mm)
        print(f"  Result: {result}")
        assert isinstance(result, DuckArray)
        print("  PASSED\n")
    except ValueError as e:
        print(f"  FAILED with ValueError: {e}\n")
        raise


if __name__ == "__main__":
    test_duck_array_with_quantity_same_units()
    test_quantity_with_duck_array_same_units()
    test_quantity_with_duck_array_different_units()
    print("All tests passed!")
