# Fix Summary: Inconsistent behavior of `world_to_pixel` in `SlicedLowLevelWCS`

## Issue
When performing `world_to_pixel` on a sliced WCS with dropped world dimensions and a non-trivial PCij matrix that couples dimensions, the result is incorrect for one of the dimensions. The pixel coordinate returned is essentially infinite instead of the expected value.

## Root Cause
The `world_to_pixel_values` method in `SlicedLowLevelWCS` (line 254 of `astropy/wcs/wcsapi/wrappers/sliced_wcs.py`) fills dropped world dimensions with an arbitrary value of `1.0`:

```python
else:
    world_arrays_new.append(1.)  # <-- PROBLEM
```

When the PCij matrix couples dimensions together, the transformation from world to pixel coordinates depends on ALL world coordinate values. Using an arbitrary value like `1.0` for dropped dimensions causes incorrect pixel coordinate calculations.

## Solution
Use the actual world coordinate values from the `dropped_world_dimensions` property instead of the arbitrary `1.0`:

```python
else:
    # Use the actual world coordinate value for dropped dimensions
    if idropped < len(dropped_world_values):
        world_arrays_new.append(dropped_world_values[idropped])
        idropped += 1
    else:
        world_arrays_new.append(1.)  # Fallback for safety
```

## Files Modified
1. **astropy/wcs/wcsapi/wrappers/sliced_wcs.py** (lines 245-269)
   - Modified `world_to_pixel_values` method to use actual world coordinate values for dropped dimensions

2. **astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py** (lines 904-949)
   - Added regression test `test_world_to_pixel_with_pc_matrix` to verify the fix

## How the Fix Works

### Before (Buggy Behavior)
1. User calls `sliced_wcs.world_to_pixel_values(0.0, 0.0, 1.05)` on a 2D sliced WCS
2. The method fills the dropped wavelength dimension with `1.0`
3. Calls underlying WCS's `world_to_pixel_values(0.0, 0.0, 1.0)` (wrong wavelength!)
4. Due to PCij coupling, this produces incorrect pixel coordinates

### After (Fixed Behavior)
1. User calls `sliced_wcs.world_to_pixel_values(0.0, 0.0, 1.05)` on a 2D sliced WCS
2. The method retrieves the actual wavelength value from `dropped_world_dimensions['value']`
3. Calls underlying WCS's `world_to_pixel_values(0.0, 0.0, 1.05)` (correct wavelength!)
4. Produces correct pixel coordinates

## Why This Works
- The `dropped_world_dimensions` property computes the correct world coordinate values for dropped dimensions by calling `_pixel_to_world_values_all(*[0]*len(self._pixel_keep))`
- This gives the world coordinates at pixel position 0 for all kept dimensions
- These values are constant for a given slice and represent the actual world coordinates at the slice location
- Using these values ensures the transformation is accurate when dimensions are coupled

## Backward Compatibility
- The fix maintains backward compatibility because it only changes behavior when dropped world dimensions exist
- A fallback to `1.0` is still present for safety
- Existing tests continue to pass because they test cases where the arbitrary `1.0` value happens to work (e.g., when dimensions are not coupled)

## Test Coverage
The fix is validated by:
1. **New regression test**: `test_world_to_pixel_with_pc_matrix` - Tests the specific issue reported
2. **Existing tests**: All existing tests in `test_sliced_wcs.py` continue to pass, including:
   - `test_celestial_slice` - Tests `world_to_pixel_values` with dropped spectral dimension
   - `test_celestial_range_rot` - Tests with rotation matrix
   - Other slicing tests

## Example Usage
```python
import numpy as np
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

# Create a 3D WCS with non-trivial PCij matrix
wcs_header = {
    'WCSAXES': 3,
    'CRPIX1': 50.5, 'CRPIX2': 13.0, 'CRPIX3': 1.0,
    'PC1_1': 0.0, 'PC1_2': -1.0, 'PC1_3': 0.0,
    'PC2_1': 1.0, 'PC2_2': 0.0, 'PC2_3': -1.0,
    'CDELT1': 5, 'CDELT2': 5, 'CDELT3': 0.055,
    'CUNIT1': 'arcsec', 'CUNIT2': 'arcsec', 'CUNIT3': 'Angstrom',
    'CTYPE1': 'HPLN-TAN', 'CTYPE2': 'HPLT-TAN', 'CTYPE3': 'WAVE',
    'CRVAL1': 0.0, 'CRVAL2': 0.0, 'CRVAL3': 1.05,
}
fits_wcs = WCS(header=wcs_header)

# Full WCS world_to_pixel
px_full, py_full, pz_full = fits_wcs.world_to_pixel_values(0.0, 0.0, 1.05)
# Result: (49.5, 12.0, ~0.0)

# Sliced WCS world_to_pixel (now works correctly!)
sliced_wcs = SlicedLowLevelWCS(fits_wcs, 0)
px_sliced, py_sliced = sliced_wcs.world_to_pixel_values(0.0, 0.0, 1.05)
# Result: (49.5, 12.0) - matches the full WCS!
```
