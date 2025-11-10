"""
Test script for the EO detection simulator
"""

import numpy as np
from physics import calculate_detection_range, calculate_system_parameters
from constants import TYPICAL_NEDT, TYPICAL_INTEGRATION_TIME

def test_basic_calculation():
    """Test basic detection range calculation"""
    print("=" * 60)
    print("ELECTRO-OPTICAL DETECTION SIMULATOR - TEST")
    print("=" * 60)

    # Test Case 1: MWIR system, daytime, ground background
    print("\nTest Case 1: MWIR System")
    print("-" * 60)

    params = {
        'target_intensity': 0.5,        # W/sr
        'fov_degrees': 10.0,            # degrees
        'pixel_rows': 480,
        'pixel_cols': 640,
        'pixel_size_um': 17.0,          # μm
        'band_type': 'MWIR',
        'nedt_mK': TYPICAL_NEDT['MWIR'],
        'integration_time_ms': TYPICAL_INTEGRATION_TIME['MWIR'],
        'time_of_day': 'day',
        'background_type': 'ground',
        'visibility_preset': 'Good',
        'snr_threshold': 5.0
    }

    # Calculate system parameters
    sys_params = calculate_system_parameters(
        params['fov_degrees'],
        params['pixel_rows'],
        params['pixel_cols'],
        params['pixel_size_um']
    )

    print(f"FOV: {params['fov_degrees']}°")
    print(f"Pixel Array: {params['pixel_rows']} × {params['pixel_cols']}")
    print(f"Pixel Size: {params['pixel_size_um']} μm")
    print(f"\nCalculated System Parameters:")
    print(f"  Focal Length: {sys_params['focal_length_mm']:.1f} mm")
    print(f"  Aperture Diameter: {sys_params['aperture_diameter_mm']:.1f} mm")
    print(f"  Aperture Area: {sys_params['aperture_area_cm2']:.2f} cm²")
    print(f"  IFOV: {sys_params['ifov_mrad']:.3f} mrad")

    # Calculate detection range
    max_range, _, _ = calculate_detection_range(**params)

    print(f"\nDetection Performance:")
    print(f"  Band: {params['band_type']}")
    print(f"  NEDT: {params['nedt_mK']} mK")
    print(f"  Target Emission: {params['target_intensity']} W/sr")
    print(f"  Conditions: {params['time_of_day'].capitalize()}, {params['background_type'].replace('_', ' ').title()}")
    print(f"  Visibility: {params['visibility_preset']}")
    print(f"  SNR Threshold: {params['snr_threshold']}")
    print(f"\n  ✓ MAXIMUM DETECTION RANGE: {max_range:.2f} km ({max_range*1000:.0f} m)")

    # Test Case 2: LWIR system, night, clear sky
    print("\n" + "=" * 60)
    print("Test Case 2: LWIR System")
    print("-" * 60)

    params['band_type'] = 'LWIR'
    params['nedt_mK'] = TYPICAL_NEDT['LWIR']
    params['time_of_day'] = 'night'
    params['background_type'] = 'clear_sky'

    max_range, _, _ = calculate_detection_range(**params)

    print(f"  Band: {params['band_type']}")
    print(f"  NEDT: {params['nedt_mK']} mK")
    print(f"  Conditions: {params['time_of_day'].capitalize()}, {params['background_type'].replace('_', ' ').title()}")
    print(f"\n  ✓ MAXIMUM DETECTION RANGE: {max_range:.2f} km ({max_range*1000:.0f} m)")

    # Test Case 3: Sensitivity to target emission
    print("\n" + "=" * 60)
    print("Test Case 3: Sensitivity Analysis - Target Emission")
    print("-" * 60)

    params['band_type'] = 'MWIR'
    params['nedt_mK'] = TYPICAL_NEDT['MWIR']
    params['time_of_day'] = 'day'
    params['background_type'] = 'ground'

    target_emissions = [0.1, 0.5, 1.0, 2.0, 5.0]

    print(f"{'Target Emission (W/sr)':<25} {'Detection Range (km)':<25}")
    print("-" * 50)

    for te in target_emissions:
        params['target_intensity'] = te
        max_range, _, _ = calculate_detection_range(**params)
        print(f"{te:<25.1f} {max_range:<25.2f}")

    print("\n" + "=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)
    print("\nTo run the interactive GUI, execute:")
    print("    streamlit run simulator_app.py")
    print("=" * 60)

if __name__ == "__main__":
    test_basic_calculation()
