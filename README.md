# Electro-Optical Detection Range Simulator

A Python-based simulation tool for calculating the maximum detection range of electro-optical (thermal imaging) systems detecting small UAV targets.

## Overview

This simulator helps predict the detection performance of MWIR (Mid-Wave Infrared) and LWIR (Long-Wave Infrared) imaging systems for small unmanned aerial vehicles (UAVs) like DJI consumer drones. It uses physics-based models incorporating atmospheric transmission, detector noise characteristics, and environmental conditions.

## Features

- **Interactive GUI**: Web-based interface with sliders and dropdown menus
- **Real-time calculations**: Instant updates as parameters change
- **Multiple spectral bands**: MWIR (3-5 μm) and LWIR (8-14 μm)
- **Atmospheric modeling**: Simplified transmission model with visibility presets
- **Environmental conditions**: Day/night, ground/cloud/clear sky backgrounds
- **Sensitivity analysis**: Analyze impact of key parameters on detection range
- **SNR-based detection**: Configurable Signal-to-Noise Ratio threshold

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository:
```bash
cd Optical_Sens_Sim
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulator

Launch the application with:

```bash
streamlit run simulator_app.py
```

The simulator will open in your default web browser at `http://localhost:8501`

### Parameters

#### System Parameters

- **Spectral Band**: MWIR (3-5 μm) or LWIR (8-14 μm)
- **Field of View**: 1° to 45° (typical: 5-15°)
- **Pixel Array**: Rows and columns (e.g., 640×480)
- **Pixel Size**: 5-50 μm (typical: 15-25 μm)

#### Detector Performance

- **NEDT** (Noise Equivalent Delta Temperature): 5-200 mK
  - MWIR typical: 20 mK (cooled detectors)
  - LWIR typical: 50 mK (uncooled detectors)
- **Integration Time**: 0.5-50 ms

#### Environmental Conditions

- **Time of Day**: Day or Night
- **Background**: Ground, Cloud, or Clear Sky
- **Visibility**: Excellent (40 km), Good (20 km), Moderate (10 km), Poor (5 km)

#### Target Parameters

- **Target Emission**: 0.01-10 W/sr (radiant intensity)
- **Target Type**: Small UAV (approximately 0.5m × 0.5m)

#### Detection Criteria

- **SNR Threshold**: 1-20 (typical: 5)

## Understanding the Results

### Main Output

The simulator displays:
- **Maximum Detection Range**: Distance at which SNR equals the threshold
- **Calculated System Parameters**: Focal length, aperture size, IFOV

### Plots

1. **SNR vs Range Curve**: Shows how signal quality degrades with distance
2. **Sensitivity Analysis**:
   - Target emission impact
   - Pixel size impact
   - NEDT impact

## Physics Background

### Detection Model

The simulator uses the following physical principles:

1. **Signal Calculation**:
   - Target radiant intensity (W/sr)
   - Inverse square law
   - Atmospheric transmission (Beer-Lambert)
   - Optical system collection efficiency

2. **Noise Model**:
   - Background radiance from scene
   - Detector NEDT
   - Thermal noise characteristics

3. **SNR Calculation**:
   ```
   SNR = Signal_Power / Noise_Power
   Detection occurs when SNR ≥ Threshold
   ```

### Atmospheric Transmission

Simplified Beer-Lambert law:
```
τ = exp(-β × Range)
```
where β (extinction coefficient) depends on visibility and wavelength.

### Key Assumptions

- Target: Small quadcopter (~0.5m × 0.5m cross-section)
- Optical system: f/2.0, 70% transmission efficiency
- Lambertian target emission model
- Simplified atmospheric model (no turbulence effects)

## File Structure

```
Optical_Sens_Sim/
├── simulator_app.py      # Main Streamlit GUI application
├── physics.py            # Physics calculations and models
├── constants.py          # Physical constants and typical values
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Example Use Cases

1. **System Design**: Compare MWIR vs LWIR for specific operational requirements
2. **Performance Prediction**: Estimate detection range for given sensor specifications
3. **Requirement Analysis**: Determine necessary NEDT or aperture size for target range
4. **Trade Studies**: Analyze pixel count vs pixel size trade-offs

## Limitations

- Simplified atmospheric model (no molecular absorption bands)
- No turbulence or scintillation effects
- Assumes point source target (valid for small, distant objects)
- No clutter or false alarm modeling
- Simplified noise model

## Technical Notes

### Spectral Bands

- **MWIR (3-5 μm)**:
  - Better detector sensitivity (cooled)
  - More affected by atmospheric extinction
  - Good for hot targets

- **LWIR (8-14 μm)**:
  - Better atmospheric transmission
  - Uncooled detectors available
  - Better for cooler targets and longer ranges

### Typical Sensor Values

| Parameter | MWIR | LWIR |
|-----------|------|------|
| NEDT | 20 mK | 50 mK |
| Pixel size | 15-25 μm | 17-25 μm |
| Integration time | 5 ms | 10 ms |
| Detector type | Cooled (InSb, HgCdTe) | Uncooled (microbolometer) |

## Troubleshooting

**Issue**: Range shows as 0 km
- Increase target emission
- Improve detector sensitivity (lower NEDT)
- Increase aperture size (decrease FOV or increase pixel count)
- Check visibility conditions

**Issue**: Unrealistic ranges
- Verify target emission is reasonable (0.1-2 W/sr typical for small UAV)
- Check that visibility preset matches conditions
- Ensure NEDT values are appropriate for detector type

## Future Enhancements

Potential improvements for future versions:
- Johnson Criteria detection model
- Multiple target types
- Advanced atmospheric models (MODTRAN integration)
- Temporal noise modeling
- False alarm rate calculations
- Export results to CSV/PDF

## License

This software is provided for educational and research purposes.

## Contact

For questions or suggestions, please create an issue in the repository.
