"""
Resonance Modes Probing
=======================

PROBING QUESTION: What are the natural oscillation frequencies of the Merkaba?

This probe performs spectral analysis to identify resonance modes.
Like a drum or wine glass, the structure should have characteristic frequencies.

MATHEMATICAL FOUNDATION:
- Power spectrum: S(f) = |FFT(x(t))|^2
- Peaks indicate resonance frequencies
- Spectral exponent reveals noise type (white, 1/f, etc.)

NULL HYPOTHESIS: White noise (flat spectrum, no preferred frequencies)
DISCOVERY: Peaks would indicate natural oscillation modes

Reference: Fourier analysis, spectral theory
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter

from gravity_field_model.framework import *
from gravity_field_model.common import traverse_pi_base8, TET_A, TET_B


def get_vertex_history(n_steps: int) -> List[int]:
    """Extract vertex sequence from traversal."""
    traversal = traverse_pi_base8(n_steps, include_integer=True)
    return [step['vertex'] for step in traversal]


def compute_power_spectrum(signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute power spectral density using FFT.
    
    Returns: (frequencies, power)
    """
    n = len(signal)
    
    # Apply Hanning window to reduce spectral leakage
    window = np.hanning(n)
    windowed = (signal - np.mean(signal)) * window
    
    # FFT
    fft_result = np.fft.rfft(windowed)
    power = np.abs(fft_result) ** 2
    
    # Frequencies (normalized to cycles per step)
    freqs = np.fft.rfftfreq(n)
    
    return freqs, power


def find_spectral_peaks(freqs: np.ndarray, power: np.ndarray, 
                       threshold_ratio: float = 5.0) -> List[Dict]:
    """
    Find peaks in power spectrum that exceed the mean by threshold_ratio.
    """
    mean_power = np.mean(power[1:])  # Exclude DC
    std_power = np.std(power[1:])
    
    peaks = []
    for i in range(1, len(power) - 1):
        if power[i] > power[i-1] and power[i] > power[i+1]:
            if power[i] > mean_power + threshold_ratio * std_power:
                peaks.append({
                    'frequency': freqs[i],
                    'period': 1 / freqs[i] if freqs[i] > 0 else float('inf'),
                    'power': power[i],
                    'snr': power[i] / mean_power,
                })
    
    # Sort by power
    peaks.sort(key=lambda x: x['power'], reverse=True)
    return peaks


def compute_spectral_exponent(freqs: np.ndarray, power: np.ndarray) -> float:
    """
    Fit power law S(f) ~ f^(-beta) to determine noise type.
    
    beta = 0: white noise
    beta = 1: pink noise (1/f)
    beta = 2: Brownian noise (1/f^2)
    """
    # Use log-log fit, excluding DC and very high frequencies
    valid = (freqs > 0.01) & (freqs < 0.4) & (power > 0)
    
    if np.sum(valid) < 5:
        return 0.0
    
    log_f = np.log10(freqs[valid])
    log_p = np.log10(power[valid])
    
    # Linear fit
    slope, intercept = np.polyfit(log_f, log_p, 1)
    
    return -slope  # beta is negative of slope


def compute_chamber_oscillation(history: List[int]) -> np.ndarray:
    """
    Convert vertex sequence to TetA/TetB oscillation signal.
    
    +1 for TetA, -1 for TetB
    """
    return np.array([1 if v in TET_A else -1 for v in history], dtype=float)


# =============================================================================
# TEST CLASSES
# =============================================================================

class SpectralAnalysisProbe(Test):
    """
    PROBING: Identify resonance frequencies from power spectrum.
    """
    name = "Resonance Mode Spectral Analysis"
    question = (
        "Does the Merkaba have preferred oscillation frequencies, like a drum "
        "or bell? We analyze the power spectrum of the TetA/TetB oscillation "
        "to find resonance peaks."
    )
    reference = "Fourier analysis, spectral theory, resonance"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We compute the power spectrum of the chamber oscillation. "
        "Peaks above the noise floor indicate natural frequencies. White noise "
        "would have a flat spectrum. 1/f noise indicates scale-free dynamics. "
        "Sharp peaks would suggest quantized modes."
    )

    def derivation(self):
        return (
            Derivation()
            .step("POWER SPECTRUM:")
            .equation("S(f) = |FFT(x(t))|^2")
            .step("Interpretation:")
            .step("  Peaks: natural frequencies (resonances)")
            .step("  Flat: white noise (no preferred frequency)")
            .step("  1/f: scale-free dynamics")
            .step("RESONANCE CONDITION:")
            .step("Peaks occur where the structure naturally oscillates.")
            .step("Period T = 1/f gives characteristic timescale.")
            .conclude("Power spectrum reveals resonance structure.")
        )

    def model(self):
        n_steps = 8192  # Power of 2 for efficient FFT
        history = get_vertex_history(n_steps)
        
        # Convert to chamber oscillation signal
        signal = compute_chamber_oscillation(history)
        
        # Compute power spectrum
        freqs, power = compute_power_spectrum(signal)
        
        # Find peaks
        peaks = find_spectral_peaks(freqs, power, threshold_ratio=3.0)
        
        # Dominant frequency
        dominant_freq = peaks[0]['frequency'] if peaks else 0.0
        dominant_period = peaks[0]['period'] if peaks else float('inf')
        
        # Spectral exponent
        beta = compute_spectral_exponent(freqs, power)
        
        # Characterize spectrum type
        if beta < 0.3:
            spectrum_type = "white"
        elif beta < 0.7:
            spectrum_type = "pink-ish"
        elif beta < 1.3:
            spectrum_type = "pink (1/f)"
        else:
            spectrum_type = "brown (1/f^2)"
        
        return (
            Model()
            .add("Number of peaks", len(peaks))
            .add("Dominant frequency (cycles/step)", dominant_freq)
            .add("Dominant period (steps)", dominant_period)
            .add("Spectral exponent beta", beta)
            .add("Peak SNR", peaks[0]['snr'] if peaks else 1.0)
        )

    def observations(self):
        # NULL: White noise (flat spectrum, no peaks)
        return (
            Observed()
            .add("Number of peaks", 0)
            .add("Dominant frequency (cycles/step)", 0.0)
            .add("Dominant period (steps)", 0.0)
            .add("Spectral exponent beta", 0.0)  # White noise
            .add("Peak SNR", 1.0)
        )


class OscillationModeProbe(Test):
    """
    PROBING: Characterize the dominant oscillation mode.
    """
    name = "Dominant Oscillation Mode"
    question = (
        "If there is a dominant oscillation, what is its character? "
        "Is it a simple period-2 (TetA-TetB-TetA-TetB) or more complex? "
        "What fraction of the variance does it explain?"
    )
    reference = "Mode analysis, principal oscillation patterns"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: We isolate the dominant oscillation mode and measure its "
        "properties. Period-2 would mean simple alternation. Longer periods "
        "suggest more complex dynamics. Mode strength indicates how much "
        "of the dynamics is explained by this single frequency."
    )

    def derivation(self):
        return (
            Derivation()
            .step("OSCILLATION MODES:")
            .step("Decompose signal into Fourier modes:")
            .equation("x(t) = sum_k A_k * cos(2*pi*f_k*t + phi_k)")
            .step("Dominant mode: largest A_k")
            .step("MODE STRENGTH:")
            .equation("Strength = |A_dominant|^2 / sum_k |A_k|^2")
            .step("Measures fraction of variance in this mode.")
            .step("PERIOD-2 TEST:")
            .step("If f = 0.5, we have period-2 oscillation.")
            .step("This is the fastest possible oscillation (TetA-TetB-...).")
            .conclude("Mode analysis reveals oscillation character.")
        )

    def model(self):
        n_steps = 8192
        history = get_vertex_history(n_steps)
        signal = compute_chamber_oscillation(history)
        
        # FFT
        fft_result = np.fft.rfft(signal - np.mean(signal))
        power = np.abs(fft_result) ** 2
        freqs = np.fft.rfftfreq(n_steps)
        
        # Total power (excluding DC)
        total_power = np.sum(power[1:])
        
        # Find dominant mode
        dominant_idx = np.argmax(power[1:]) + 1
        dominant_freq = freqs[dominant_idx]
        dominant_power = power[dominant_idx]
        
        # Mode strength
        mode_strength = dominant_power / total_power if total_power > 0 else 0
        
        # Is it period-2?
        is_period_2 = abs(dominant_freq - 0.5) < 0.05
        
        # Check for harmonics
        harmonic_freqs = [dominant_freq * k for k in [2, 3, 4]]
        harmonic_power = 0
        for hf in harmonic_freqs:
            idx = np.argmin(np.abs(freqs - hf))
            if idx < len(power):
                harmonic_power += power[idx]
        
        return (
            Model()
            .add("Dominant frequency", dominant_freq)
            .add("Dominant period", 1/dominant_freq if dominant_freq > 0 else 0)
            .add("Mode strength (fraction)", mode_strength)
            .add("Is period-2", 1.0 if is_period_2 else 0.0)
            .add("Harmonic content", harmonic_power / total_power if total_power > 0 else 0)
        )

    def observations(self):
        # NULL: No dominant mode (uniform spectrum)
        return (
            Observed()
            .add("Dominant frequency", 0.0)
            .add("Dominant period", 0.0)
            .add("Mode strength (fraction)", 0.0)
            .add("Is period-2", 0.0)
            .add("Harmonic content", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    SpectralAnalysisProbe,
    OscillationModeProbe,
]


def run_all():
    """Run all resonance modes probing tests."""
    summary = (
        "RESONANCE MODES PROBING\n\n"
        "These probes identify natural oscillation frequencies.\n"
        "Power spectrum: S(f) = |FFT(x)|^2\n"
        "Peaks indicate resonances\n\n"
        "We are DISCOVERING the field's natural frequencies."
    )
    return run_tests("Resonance Modes Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
