"""
Electro-Optical Detection Range Simulator
Interactive GUI for calculating maximum detection range of thermal imaging systems
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import physics
from constants import *


def main():
    st.set_page_config(
        page_title="EO Detection Range Simulator",
        page_icon="🔭",
        layout="wide"
    )

    st.title("🔭 Electro-Optical Detection Range Simulator")
    st.markdown("**Target: Small UAV (DJI-class) Detection**")
    st.markdown("---")

    # Create two columns for layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("⚙️ System Parameters")

        # Spectral Band Selection
        band_type = st.selectbox(
            "Spectral Band",
            options=['MWIR', 'LWIR'],
            help="MWIR: 3-5 μm (cooled detector), LWIR: 8-14 μm (uncooled detector)"
        )

        st.subheader("Sensor Configuration")

        # FOV
        fov_degrees = st.slider(
            "Field of View (degrees)",
            min_value=1.0,
            max_value=45.0,
            value=10.0,
            step=0.5,
            help="Horizontal/vertical field of view"
        )

        # Pixel array
        col_a, col_b = st.columns(2)
        with col_a:
            pixel_cols = st.number_input(
                "Columns (pixels)",
                min_value=64,
                max_value=1920,
                value=640,
                step=64
            )
        with col_b:
            pixel_rows = st.number_input(
                "Rows (pixels)",
                min_value=64,
                max_value=1080,
                value=480,
                step=64
            )

        # Pixel size
        pixel_size_um = st.slider(
            "Pixel Size (μm)",
            min_value=5.0,
            max_value=50.0,
            value=17.0,
            step=1.0,
            help="Detector pixel pitch"
        )

        st.subheader("Detector Performance")

        # NEDT
        default_nedt = TYPICAL_NEDT[band_type]
        nedt_mK = st.slider(
            "NEDT (mK)",
            min_value=5.0,
            max_value=200.0,
            value=float(default_nedt),
            step=5.0,
            help="Noise Equivalent Delta Temperature"
        )

        # Integration time
        default_int_time = TYPICAL_INTEGRATION_TIME[band_type]
        integration_time_ms = st.slider(
            "Integration Time (ms)",
            min_value=0.5,
            max_value=50.0,
            value=float(default_int_time),
            step=0.5,
            help="Detector integration/exposure time"
        )

        st.subheader("Environmental Conditions")

        # Time of day
        time_of_day = st.selectbox(
            "Time of Day",
            options=['day', 'night'],
            format_func=lambda x: x.capitalize()
        )

        # Background type
        background_type = st.selectbox(
            "Background Type",
            options=['ground', 'cloud', 'clear_sky'],
            format_func=lambda x: x.replace('_', ' ').title()
        )

        # Visibility
        visibility_preset = st.selectbox(
            "Visibility Conditions",
            options=list(VISIBILITY_PRESETS.keys()),
            index=1,  # Default to 'Good'
            format_func=lambda x: f"{x} ({VISIBILITY_PRESETS[x]['description']})"
        )

        st.subheader("Target Parameters")

        # Target emission
        target_intensity = st.slider(
            "Target Emission (W/sr)",
            min_value=0.01,
            max_value=10.0,
            value=0.5,
            step=0.05,
            help="Total radiant intensity of the target"
        )

        st.subheader("Detection Criteria")

        # SNR threshold
        snr_threshold = st.slider(
            "SNR Threshold",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
            help="Minimum Signal-to-Noise Ratio for detection"
        )

    with col2:
        st.header("📊 Results & Analysis")

        # Calculate system parameters
        sys_params = physics.calculate_system_parameters(
            fov_degrees, pixel_rows, pixel_cols, pixel_size_um
        )

        # Display calculated system parameters
        st.subheader("Calculated System Parameters")
        param_col1, param_col2, param_col3 = st.columns(3)

        with param_col1:
            st.metric("Focal Length", f"{sys_params['focal_length_mm']:.1f} mm")
            st.metric("IFOV", f"{sys_params['ifov_mrad']:.3f} mrad")

        with param_col2:
            st.metric("Aperture Diameter", f"{sys_params['aperture_diameter_mm']:.1f} mm")
            st.metric("IFOV", f"{sys_params['ifov_arcmin']:.2f} arcmin")

        with param_col3:
            st.metric("Aperture Area", f"{sys_params['aperture_area_cm2']:.2f} cm²")

        st.markdown("---")

        # Calculate detection range
        with st.spinner("Calculating detection range..."):
            max_range_km, range_array_km, snr_array = physics.calculate_detection_range(
                target_intensity=target_intensity,
                fov_degrees=fov_degrees,
                pixel_rows=pixel_rows,
                pixel_cols=pixel_cols,
                pixel_size_um=pixel_size_um,
                band_type=band_type,
                nedt_mK=nedt_mK,
                integration_time_ms=integration_time_ms,
                time_of_day=time_of_day,
                background_type=background_type,
                visibility_preset=visibility_preset,
                snr_threshold=snr_threshold
            )

        # Display main result
        st.subheader("🎯 Maximum Detection Range")
        if max_range_km > 0:
            st.success(f"## {max_range_km:.2f} km")
            st.info(f"Target detectable at ranges up to {max_range_km*1000:.0f} meters")
        else:
            st.error("Target not detectable under current conditions")

        st.markdown("---")

        # Plot SNR vs Range
        st.subheader("SNR vs Range Curve")

        fig_snr = go.Figure()

        fig_snr.add_trace(go.Scatter(
            x=range_array_km,
            y=snr_array,
            mode='lines',
            name='SNR',
            line=dict(color='blue', width=2)
        ))

        fig_snr.add_hline(
            y=snr_threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Detection Threshold (SNR={snr_threshold})",
            annotation_position="right"
        )

        if max_range_km > 0:
            fig_snr.add_vline(
                x=max_range_km,
                line_dash="dash",
                line_color="green",
                annotation_text=f"Max Range: {max_range_km:.2f} km",
                annotation_position="top"
            )

        fig_snr.update_layout(
            xaxis_title="Range (km)",
            yaxis_title="Signal-to-Noise Ratio",
            yaxis_type="log",
            hovermode='x unified',
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig_snr, use_container_width=True)

        # Sensitivity Analysis
        st.subheader("📈 Sensitivity Analysis")

        # Create tabs for different sensitivity analyses
        tab1, tab2, tab3 = st.tabs([
            "Target Emission",
            "Pixel Size",
            "NEDT"
        ])

        with tab1:
            # Sensitivity to target emission
            target_emissions = np.linspace(0.1, 5.0, 20)
            ranges_vs_emission = []

            for te in target_emissions:
                r, _, _ = physics.calculate_detection_range(
                    target_intensity=te,
                    fov_degrees=fov_degrees,
                    pixel_rows=pixel_rows,
                    pixel_cols=pixel_cols,
                    pixel_size_um=pixel_size_um,
                    band_type=band_type,
                    nedt_mK=nedt_mK,
                    integration_time_ms=integration_time_ms,
                    time_of_day=time_of_day,
                    background_type=background_type,
                    visibility_preset=visibility_preset,
                    snr_threshold=snr_threshold
                )
                ranges_vs_emission.append(r)

            fig_sens1 = go.Figure()
            fig_sens1.add_trace(go.Scatter(
                x=target_emissions,
                y=ranges_vs_emission,
                mode='lines+markers',
                name='Detection Range',
                line=dict(color='purple', width=2)
            ))

            # Mark current value
            fig_sens1.add_vline(
                x=target_intensity,
                line_dash="dash",
                line_color="red",
                annotation_text="Current",
                annotation_position="top"
            )

            fig_sens1.update_layout(
                xaxis_title="Target Emission (W/sr)",
                yaxis_title="Detection Range (km)",
                hovermode='x unified',
                height=350
            )

            st.plotly_chart(fig_sens1, use_container_width=True)

        with tab2:
            # Sensitivity to pixel size
            pixel_sizes = np.linspace(5, 50, 20)
            ranges_vs_pixel = []

            for ps in pixel_sizes:
                r, _, _ = physics.calculate_detection_range(
                    target_intensity=target_intensity,
                    fov_degrees=fov_degrees,
                    pixel_rows=pixel_rows,
                    pixel_cols=pixel_cols,
                    pixel_size_um=ps,
                    band_type=band_type,
                    nedt_mK=nedt_mK,
                    integration_time_ms=integration_time_ms,
                    time_of_day=time_of_day,
                    background_type=background_type,
                    visibility_preset=visibility_preset,
                    snr_threshold=snr_threshold
                )
                ranges_vs_pixel.append(r)

            fig_sens2 = go.Figure()
            fig_sens2.add_trace(go.Scatter(
                x=pixel_sizes,
                y=ranges_vs_pixel,
                mode='lines+markers',
                name='Detection Range',
                line=dict(color='orange', width=2)
            ))

            # Mark current value
            fig_sens2.add_vline(
                x=pixel_size_um,
                line_dash="dash",
                line_color="red",
                annotation_text="Current",
                annotation_position="top"
            )

            fig_sens2.update_layout(
                xaxis_title="Pixel Size (μm)",
                yaxis_title="Detection Range (km)",
                hovermode='x unified',
                height=350
            )

            st.plotly_chart(fig_sens2, use_container_width=True)

        with tab3:
            # Sensitivity to NEDT
            nedt_values = np.linspace(10, 150, 20)
            ranges_vs_nedt = []

            for nedt in nedt_values:
                r, _, _ = physics.calculate_detection_range(
                    target_intensity=target_intensity,
                    fov_degrees=fov_degrees,
                    pixel_rows=pixel_rows,
                    pixel_cols=pixel_cols,
                    pixel_size_um=pixel_size_um,
                    band_type=band_type,
                    nedt_mK=nedt,
                    integration_time_ms=integration_time_ms,
                    time_of_day=time_of_day,
                    background_type=background_type,
                    visibility_preset=visibility_preset,
                    snr_threshold=snr_threshold
                )
                ranges_vs_nedt.append(r)

            fig_sens3 = go.Figure()
            fig_sens3.add_trace(go.Scatter(
                x=nedt_values,
                y=ranges_vs_nedt,
                mode='lines+markers',
                name='Detection Range',
                line=dict(color='green', width=2)
            ))

            # Mark current value
            fig_sens3.add_vline(
                x=nedt_mK,
                line_dash="dash",
                line_color="red",
                annotation_text="Current",
                annotation_position="top"
            )

            fig_sens3.update_layout(
                xaxis_title="NEDT (mK)",
                yaxis_title="Detection Range (km)",
                hovermode='x unified',
                height=350
            )

            st.plotly_chart(fig_sens3, use_container_width=True)

    # Footer with information
    st.markdown("---")
    with st.expander("ℹ️ About this Simulator"):
        st.markdown("""
        ### Electro-Optical Detection Range Simulator

        This simulator calculates the maximum detection range of thermal imaging systems
        for small UAV targets (e.g., DJI consumer drones) based on:

        - **SNR-based detection**: Uses Signal-to-Noise Ratio as the detection criterion
        - **Atmospheric transmission**: Simplified Beer-Lambert law model for MWIR/LWIR
        - **Background radiance**: Standard values for different conditions
        - **Sensor physics**: Realistic detector and optical parameters

        #### Key Assumptions:
        - Target: Small quadcopter (~0.5m × 0.5m)
        - Optics: f/2.0, 70% transmission efficiency
        - Detection criterion: Configurable SNR threshold (default 5.0)

        #### Spectral Bands:
        - **MWIR**: 3-5 μm (typically cooled detectors, better sensitivity)
        - **LWIR**: 8-14 μm (typically uncooled, better atmospheric transmission)
        """)


if __name__ == "__main__":
    main()
