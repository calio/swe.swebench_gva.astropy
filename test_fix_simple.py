#!/usr/bin/env python3
"""Simple test script to validate the fix for SlicedLowLevelWCS world_to_pixel issue."""

import sys
import os

# Add the repo to the path
sys.path.insert(0, '/Users/calio/work/astropy__astropy-13579')

import numpy as np
from numpy.testing import assert_allclose

# Import WCS components
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

def test_world_to_pixel_with_pc_matrix():
    """
    Test world_to_pixel with a non-trivial PCij matrix that couples dimensions.
    
    This is a regression test for https://github.com/astropy/astropy/issues/13579
    where world_to_pixel on a sliced WCS with coupled dimensions returned incorrect results.
    """
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
    fits_wcs = WCS(header=wcs_header)
    
    # Test full WCS world_to_pixel
    px_full, py_full, pz_full = fits_wcs.world_to_pixel_values(0.0, 0.0, 1.05)
    print(f"Full WCS world_to_pixel: ({px_full}, {py_full}, {pz_full})")
    
    # Test sliced WCS world_to_pixel (slice at first wavelength)
    sliced_wcs = SlicedLowLevelWCS(fits_wcs, 0)
    px_sliced, py_sliced = sliced_wcs.world_to_pixel_values(0.0, 0.0, 1.05)
    print(f"Sliced WCS world_to_pixel: ({px_sliced}, {py_sliced})")
    
    # The first two pixel coordinates should match
    print(f"\nValidation:")
    print(f"  X pixel match: {np.isclose(px_full, px_sliced, rtol=1e-5)} (full={px_full}, sliced={px_sliced})")
    print(f"  Y pixel match: {np.isclose(py_full, py_sliced, rtol=1e-5)} (full={py_full}, sliced={py_sliced})")
    
    try:
        assert_allclose(px_full, px_sliced, rtol=1e-5)
        assert_allclose(py_full, py_sliced, rtol=1e-5)
        print("\n✓ TEST PASSED: Sliced WCS world_to_pixel now returns correct results!")
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False

def test_celestial_slice():
    """Test from the existing test suite to ensure no regression."""
    from astropy.io.fits import Header
    import warnings
    from astropy.io.fits.verify import VerifyWarning
    
    HEADER_SPECTRAL_CUBE = """
NAXIS   = 3
NAXIS1  = 10
NAXIS2  = 20
NAXIS3  = 30
CTYPE1  = GLAT-CAR
CTYPE2  = FREQ
CTYPE3  = GLON-CAR
CNAME1  = Latitude
CNAME2  = Frequency
CNAME3  = Longitude
CRVAL1  = 10
CRVAL2  = 20
CRVAL3  = 25
CRPIX1  = 30
CRPIX2  = 40
CRPIX3  = 45
CDELT1  = -0.1
CDELT2  =  0.5
CDELT3  =  0.1
CUNIT1  = deg
CUNIT2  = Hz
CUNIT3  = deg
"""
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', VerifyWarning)
        WCS_SPECTRAL_CUBE = WCS(Header.fromstring(HEADER_SPECTRAL_CUBE, sep='\n'))
    WCS_SPECTRAL_CUBE.pixel_bounds = [(-1, 11), (-2, 18), (5, 15)]
    
    wcs = SlicedLowLevelWCS(WCS_SPECTRAL_CUBE, [Ellipsis, 5])
    
    # Test world_to_pixel_values with dropped spectral dimension
    result = wcs.world_to_pixel_values(12.4, 20, 25)
    expected = (39., 44.)
    
    print(f"\nCelestial slice test:")
    print(f"  Result: {result}")
    print(f"  Expected: {expected}")
    
    try:
        assert_allclose(result, expected)
        print("✓ TEST PASSED: Celestial slice world_to_pixel works correctly!")
        return True
    except AssertionError as e:
        print(f"✗ TEST FAILED: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing SlicedLowLevelWCS world_to_pixel fix")
    print("=" * 60)
    
    test1_passed = test_world_to_pixel_with_pc_matrix()
    test2_passed = test_celestial_slice()
    
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("All tests PASSED!")
        sys.exit(0)
    else:
        print("Some tests FAILED!")
        sys.exit(1)
