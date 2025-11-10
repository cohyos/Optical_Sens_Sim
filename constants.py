"""
Physical constants and typical values for electro-optical detection simulation
"""

import numpy as np

# Physical Constants
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
SPEED_OF_LIGHT = 2.99792458e8     # m/s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
STEFAN_BOLTZMANN = 5.670374419e-8  # W⋅m⁻²⋅K⁻⁴

# Spectral Bands (wavelengths in meters)
MWIR_BAND = {'name': 'MWIR', 'lambda_min': 3e-6, 'lambda_max': 5e-6, 'lambda_center': 4e-6}
LWIR_BAND = {'name': 'LWIR', 'lambda_min': 8e-6, 'lambda_max': 14e-6, 'lambda_center': 10e-6}

# Typical Sensor Parameters
TYPICAL_NEDT = {
    'MWIR': 20,  # mK - typical for cooled MWIR detector
    'LWIR': 50   # mK - typical for uncooled LWIR detector
}

TYPICAL_INTEGRATION_TIME = {
    'MWIR': 5,   # ms
    'LWIR': 10   # ms
}

# Atmospheric Transmission Coefficients (simplified model)
# These are approximate values for different visibility conditions
VISIBILITY_PRESETS = {
    'Excellent': {'visibility_km': 40, 'description': 'Very clear day'},
    'Good': {'visibility_km': 20, 'description': 'Clear conditions'},
    'Moderate': {'visibility_km': 10, 'description': 'Light haze'},
    'Poor': {'visibility_km': 5, 'description': 'Fog or heavy haze'}
}

# Atmospheric transmission parameters (Beer-Lambert law approximation)
# tau = exp(-beta * range) where beta depends on visibility and wavelength
ATMOSPHERIC_EXTINCTION = {
    'MWIR': 0.5,  # Relative extinction coefficient
    'LWIR': 0.3   # LWIR typically has better transmission through atmosphere
}

# Background Radiance (W/m²/sr) - approximate values
# These are integrated spectral radiance over the respective bands
BACKGROUND_RADIANCE = {
    'MWIR': {
        'day': {
            'ground': 150,      # Warm ground in daytime
            'cloud': 80,        # Clouds
            'clear_sky': 50     # Clear sky (cold)
        },
        'night': {
            'ground': 100,      # Cooler ground at night
            'cloud': 90,        # Clouds at night (warmer than clear sky)
            'clear_sky': 30     # Clear sky at night (very cold)
        }
    },
    'LWIR': {
        'day': {
            'ground': 400,      # Warm ground in daytime
            'cloud': 250,       # Clouds
            'clear_sky': 150    # Clear sky
        },
        'night': {
            'ground': 300,      # Cooler ground at night
            'cloud': 280,       # Clouds at night
            'clear_sky': 100    # Clear sky at night
        }
    }
}

# Target Parameters (small UAV like DJI)
TARGET_SIZE = {
    'length': 0.5,   # meters (approximate for small quadcopter)
    'width': 0.5,    # meters
    'height': 0.2,   # meters
    'area': 0.25     # m² (effective cross-sectional area)
}

# Default SNR threshold for detection
DEFAULT_SNR_THRESHOLD = 5.0

# Optics assumptions
DEFAULT_OPTICS_TRANSMISSION = 0.7  # Typical optical transmission efficiency
DEFAULT_F_NUMBER = 2.0  # Typical f-number for thermal imaging systems
