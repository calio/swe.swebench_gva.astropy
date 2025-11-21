#!/usr/bin/env python3
"""Test script to validate the fix for SlicedLowLevelWCS world_to_pixel issue."""

import sys
import numpy as np

# Test the fix
try:
    import astropy.wcs
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    nx = 100
    ny = 25
    nz = 2
    wcs_header = {
        'WCSAXES': 3,
        'CRPIX1': (nx + 1)/2,
        'CRPIX2': (ny + 1)/2,
        'CRPIX3': 1.0,
        'PC1_1': 0.0,
        'PC1_2': -1.0,
        'PC1_3': 0.0,
        'PC2_1': 1.0,
        'PC2_2': 0.0,
        'PC2_3': -1.0,
        'CDELT1': 5,
        'CDELT2': 5,
        'CDELT3': 0.055,
        'CUNIT1': 'arcsec',
        'CUNIT2': 'arcsec',
        'CUNIT3': 'Angstrom',
        'CTYPE1': 'HPLN-TAN',
        'CTYPE2': 'HPLT-TAN',
        'CTYPE3': 'WAVE',
        'CRVAL1': 0.0,
        'CRVAL2': 0.0,
        'CRVAL3': 1.05,
    }
    fits_wcs = astropy.wcs.WCS(header=wcs_header)

    # Test 1: Full WCS world_to_pixel
    pt = SkyCoord(Tx=0*u.arcsec, Ty=0*u.arcsec, frame=astropy.wcs.utils.wcs_to_celestial_frame(fits_wcs))
    result_full = fits_wcs.world_to_pixel(pt, 1.05*u.angstrom)
    print("Test 1: Full WCS world_to_pixel")
    print(f"  Result: {result_full}")
    print(f"  Expected: (49.5, 12.0, ~0.0)")
    
    # Test 2: Sliced WCS world_to_pixel
    ll_sliced_wcs = astropy.wcs.wcsapi.SlicedLowLevelWCS(fits_wcs, 0)
    hl_sliced_wcs = astropy.wcs.wcsapi.HighLevelWCSWrapper(ll_sliced_wcs)
    result_sliced = hl_sliced_wcs.world_to_pixel(pt)
    print("\nTest 2: Sliced WCS world_to_pixel")
    print(f"  Result: {result_sliced}")
    print(f"  Expected: (49.5, 12.0)")
    
    # Check if the fix works
    px_full, py_full, pz_full = result_full
    px_sliced, py_sliced = result_sliced
    
    # The first two components should match
    px_match = np.isclose(px_full, px_sliced, rtol=1e-5)
    py_match = np.isclose(py_full, py_sliced, rtol=1e-5)
    
    print("\nValidation:")
    print(f"  X pixel match: {px_match} (full={px_full}, sliced={px_sliced})")
    print(f"  Y pixel match: {py_match} (full={py_full}, sliced={py_sliced})")
    
    if px_match and py_match:
        print("\n✓ FIX SUCCESSFUL: Sliced WCS world_to_pixel now returns correct results!")
        sys.exit(0)
    else:
        print("\n✗ FIX FAILED: Sliced WCS world_to_pixel still returns incorrect results!")
        sys.exit(1)

except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
