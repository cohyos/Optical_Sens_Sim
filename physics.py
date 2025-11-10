"""
Physics calculations for electro-optical detection simulation
"""

import numpy as np
from constants import *


def calculate_focal_length(fov_degrees, pixel_array_width, pixel_size_um):
    """
    Calculate focal length from FOV and detector parameters

    Args:
        fov_degrees: Field of view in degrees
        pixel_array_width: Number of pixels across the FOV dimension
        pixel_size_um: Pixel pitch in micrometers

    Returns:
        focal_length: Focal length in meters
    """
    fov_rad = np.deg2rad(fov_degrees)
    detector_width_m = pixel_array_width * pixel_size_um * 1e-6
    focal_length = detector_width_m / (2 * np.tan(fov_rad / 2))
    return focal_length


def calculate_ifov(pixel_size_um, focal_length_m):
    """
    Calculate instantaneous field of view (IFOV) per pixel

    Args:
        pixel_size_um: Pixel pitch in micrometers
        focal_length_m: Focal length in meters

    Returns:
        ifov_rad: IFOV in radians
    """
    pixel_size_m = pixel_size_um * 1e-6
    ifov_rad = pixel_size_m / focal_length_m
    return ifov_rad


def atmospheric_transmission(range_km, visibility_km, band_type):
    """
    Calculate atmospheric transmission using simplified Beer-Lambert law

    Args:
        range_km: Range to target in kilometers
        visibility_km: Meteorological visibility in kilometers
        band_type: 'MWIR' or 'LWIR'

    Returns:
        transmission: Atmospheric transmission coefficient (0-1)
    """
    # Calculate extinction coefficient from visibility
    # Using approximation: beta = 3.912 / visibility (km^-1)
    beta_base = 3.912 / visibility_km

    # Apply spectral correction factor
    beta = beta_base * ATMOSPHERIC_EXTINCTION[band_type]

    # Beer-Lambert law
    transmission = np.exp(-beta * range_km)

    return transmission


def calculate_pixel_solid_angle(ifov_rad):
    """
    Calculate solid angle subtended by a single pixel

    Args:
        ifov_rad: Instantaneous field of view in radians

    Returns:
        omega: Solid angle in steradians
    """
    # For small angles: omega ≈ IFOV²
    omega = ifov_rad ** 2
    return omega


def calculate_signal_power(target_intensity_W_per_sr, range_m, aperture_area_m2,
                          atm_transmission, optics_transmission):
    """
    Calculate signal power at the detector from target

    Args:
        target_intensity_W_per_sr: Target radiant intensity in W/sr
        range_m: Range to target in meters
        aperture_area_m2: Collecting aperture area in m²
        atm_transmission: Atmospheric transmission (0-1)
        optics_transmission: Optical system transmission (0-1)

    Returns:
        signal_power_W: Signal power at detector in Watts
    """
    # Solid angle subtended by aperture at range R
    solid_angle_aperture = aperture_area_m2 / (range_m ** 2)

    # Power received (inverse square law + atmospheric loss)
    signal_power = (target_intensity_W_per_sr * solid_angle_aperture *
                   atm_transmission * optics_transmission)

    return signal_power


def calculate_background_power(background_radiance, pixel_solid_angle,
                               aperture_area_m2, optics_transmission):
    """
    Calculate background power at a single pixel

    Args:
        background_radiance: Background radiance in W/m²/sr
        pixel_solid_angle: Solid angle of a pixel in steradians
        aperture_area_m2: Collecting aperture area in m²
        optics_transmission: Optical system transmission (0-1)

    Returns:
        background_power_W: Background power per pixel in Watts
    """
    background_power = (background_radiance * pixel_solid_angle *
                       aperture_area_m2 * optics_transmission)

    return background_power


def calculate_noise_power(nedt_mK, background_power_W, temperature_ref_K=300):
    """
    Calculate noise power from NEDT

    Args:
        nedt_mK: Noise Equivalent Delta Temperature in milliKelvin
        background_power_W: Background power in Watts
        temperature_ref_K: Reference temperature in Kelvin

    Returns:
        noise_power_W: Noise power in Watts
    """
    # NEDT relates to the noise through the derivative of radiance with temperature
    # Simplified approach: noise_power ≈ (dP/dT) * NEDT
    # For this simulation, we use a simplified model:
    nedt_K = nedt_mK * 1e-3

    # Approximate relationship between power and temperature change
    # dP/dT ≈ 4 * P / T (from Stefan-Boltzmann for small changes)
    dP_dT = 4 * background_power_W / temperature_ref_K

    noise_power = dP_dT * nedt_K

    return noise_power


def calculate_snr(signal_power_W, noise_power_W):
    """
    Calculate Signal-to-Noise Ratio

    Args:
        signal_power_W: Signal power in Watts
        noise_power_W: Noise power in Watts

    Returns:
        snr: Signal-to-Noise Ratio
    """
    if noise_power_W <= 0:
        return 0

    snr = signal_power_W / noise_power_W
    return snr


def calculate_aperture_diameter(focal_length_m, f_number):
    """
    Calculate aperture diameter from focal length and f-number

    Args:
        focal_length_m: Focal length in meters
        f_number: F-number of the optical system

    Returns:
        diameter_m: Aperture diameter in meters
    """
    diameter_m = focal_length_m / f_number
    return diameter_m


def calculate_aperture_area(diameter_m):
    """
    Calculate aperture area from diameter

    Args:
        diameter_m: Aperture diameter in meters

    Returns:
        area_m2: Aperture area in m²
    """
    area_m2 = np.pi * (diameter_m / 2) ** 2
    return area_m2


def calculate_detection_range(target_intensity, fov_degrees, pixel_rows, pixel_cols,
                              pixel_size_um, band_type, nedt_mK, integration_time_ms,
                              time_of_day, background_type, visibility_preset,
                              snr_threshold, f_number=DEFAULT_F_NUMBER,
                              optics_transmission=DEFAULT_OPTICS_TRANSMISSION):
    """
    Calculate maximum detection range for given parameters

    Returns:
        max_range_km: Maximum detection range in kilometers
        range_array_km: Array of ranges for plotting
        snr_array: Corresponding SNR values
    """
    # Get visibility
    visibility_km = VISIBILITY_PRESETS[visibility_preset]['visibility_km']

    # Get background radiance
    background_radiance = BACKGROUND_RADIANCE[band_type][time_of_day][background_type]

    # Calculate optical parameters
    pixel_array_width = max(pixel_cols, pixel_rows)
    focal_length_m = calculate_focal_length(fov_degrees, pixel_array_width, pixel_size_um)
    aperture_diameter_m = calculate_aperture_diameter(focal_length_m, f_number)
    aperture_area_m2 = calculate_aperture_area(aperture_diameter_m)

    # Calculate IFOV and pixel solid angle
    ifov_rad = calculate_ifov(pixel_size_um, focal_length_m)
    pixel_solid_angle = calculate_pixel_solid_angle(ifov_rad)

    # Calculate background and noise power
    background_power_W = calculate_background_power(background_radiance, pixel_solid_angle,
                                                    aperture_area_m2, optics_transmission)
    noise_power_W = calculate_noise_power(nedt_mK, background_power_W)

    # Search for maximum range by testing different ranges
    range_array_km = np.linspace(0.1, 50, 500)  # Test from 100m to 50km
    snr_array = np.zeros_like(range_array_km)

    for i, range_km in enumerate(range_array_km):
        range_m = range_km * 1000

        # Calculate atmospheric transmission
        atm_trans = atmospheric_transmission(range_km, visibility_km, band_type)

        # Calculate signal power
        signal_power_W = calculate_signal_power(target_intensity, range_m,
                                               aperture_area_m2, atm_trans,
                                               optics_transmission)

        # Calculate SNR
        snr = calculate_snr(signal_power_W, noise_power_W)
        snr_array[i] = snr

    # Find maximum detection range where SNR >= threshold
    detection_indices = np.where(snr_array >= snr_threshold)[0]

    if len(detection_indices) > 0:
        max_range_km = range_array_km[detection_indices[-1]]
    else:
        max_range_km = 0

    return max_range_km, range_array_km, snr_array


def calculate_system_parameters(fov_degrees, pixel_rows, pixel_cols, pixel_size_um,
                                f_number=DEFAULT_F_NUMBER):
    """
    Calculate derived system parameters for display

    Returns:
        dict with calculated parameters
    """
    pixel_array_width = max(pixel_cols, pixel_rows)
    focal_length_m = calculate_focal_length(fov_degrees, pixel_array_width, pixel_size_um)
    aperture_diameter_m = calculate_aperture_diameter(focal_length_m, f_number)
    aperture_area_m2 = calculate_aperture_area(aperture_diameter_m)
    ifov_rad = calculate_ifov(pixel_size_um, focal_length_m)
    ifov_mrad = ifov_rad * 1000

    return {
        'focal_length_mm': focal_length_m * 1000,
        'aperture_diameter_mm': aperture_diameter_m * 1000,
        'aperture_area_cm2': aperture_area_m2 * 10000,
        'ifov_mrad': ifov_mrad,
        'ifov_arcmin': np.rad2deg(ifov_rad) * 60
    }
