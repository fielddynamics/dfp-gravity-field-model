"""
Mode Coupling Probing
=====================

PROBING QUESTION: Do different oscillation modes interact (nonlinear coupling)?

This probe tests for mode coupling using bispectral analysis:
correlations between three frequencies indicate nonlinear interactions.

MATHEMATICAL FOUNDATION:
- Bispectrum: B(f1, f2) = <X(f1) * X(f2) * X*(f1+f2)>
- Non-zero bispectrum indicates phase coupling between modes
- Linear systems have zero bispectrum

NULL HYPOTHESIS: Linear (independent modes, zero bispectrum)
DISCOVERY: Mode coupling would indicate nonlinear dynamics

Reference: Bispectral analysis, nonlinear dynamics
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


def compute_bispectrum(signal: np.ndarray, max_freq_idx: int = 30) -> np.ndarray:
    """
    Compute bispectrum: B(f1, f2) = <X(f1) * X(f2) * X*(f1+f2)>
    
    Non-zero bispectrum indicates nonlinear phase coupling.
    """
    n = len(signal)
    
    # FFT
    x_mean = signal - np.mean(signal)
    X = np.fft.rfft(x_mean)
    
    # Compute bispectrum for frequency pairs
    bispec = np.zeros((max_freq_idx, max_freq_idx), dtype=complex)
    
    for i in range(max_freq_idx):
        for j in range(max_freq_idx):
            k = i + j
            if k < len(X):
                bispec[i, j] = X[i] * X[j] * np.conj(X[k])
    
    return bispec


def compute_bicoherence(signal: np.ndarray, max_freq_idx: int = 30) -> np.ndarray:
    """
    Compute bicoherence: normalized bispectrum.
    
    b^2(f1, f2) = |B(f1, f2)|^2 / (<|X(f1)*X(f2)|^2> * <|X(f1+f2)|^2>)
    
    Range [0, 1]: 1 = perfect phase coupling, 0 = no coupling
    """
    n = len(signal)
    x_mean = signal - np.mean(signal)
    X = np.fft.rfft(x_mean)
    
    bispec = np.zeros((max_freq_idx, max_freq_idx), dtype=complex)
    norm = np.zeros((max_freq_idx, max_freq_idx))
    
    for i in range(max_freq_idx):
        for j in range(max_freq_idx):
            k = i + j
            if k < len(X):
                bispec[i, j] = X[i] * X[j] * np.conj(X[k])
                norm[i, j] = np.abs(X[i] * X[j]) ** 2 * np.abs(X[k]) ** 2
    
    # Avoid division by zero
    norm[norm == 0] = 1
    
    bicoherence = np.abs(bispec) ** 2 / norm
    
    return bicoherence


def find_significant_couplings(bicoherence: np.ndarray, 
                               threshold: float = 0.3) -> List[Dict]:
    """
    Find frequency pairs with significant bicoherence.
    """
    couplings = []
    max_i, max_j = bicoherence.shape
    
    for i in range(1, max_i):  # Skip DC
        for j in range(i, max_j):  # Avoid double counting
            if bicoherence[i, j] > threshold:
                couplings.append({
                    'f1_idx': i,
                    'f2_idx': j,
                    'f_sum_idx': i + j,
                    'bicoherence': bicoherence[i, j],
                })
    
    # Sort by bicoherence
    couplings.sort(key=lambda x: x['bicoherence'], reverse=True)
    return couplings


def compute_phase_synchronization(signal: np.ndarray, f1_idx: int, f2_idx: int) -> float:
    """
    Compute phase synchronization between two frequency components.
    
    Using phase difference: phi_1 + phi_2 - phi_{1+2}
    Narrow distribution indicates coupling.
    """
    n = len(signal)
    x_mean = signal - np.mean(signal)
    
    # Analytic signal via Hilbert transform (approximated with FFT)
    X = np.fft.fft(x_mean)
    
    # Extract phases
    freqs = np.fft.fftfreq(n)
    
    # Band-pass at each frequency
    def extract_phase_at_freq(X, f_idx, bandwidth=2):
        X_filtered = np.zeros_like(X)
        for i in range(max(0, f_idx - bandwidth), min(len(X), f_idx + bandwidth + 1)):
            X_filtered[i] = X[i]
        x_filtered = np.fft.ifft(X_filtered)
        return np.angle(x_filtered)
    
    phi1 = extract_phase_at_freq(X, f1_idx)
    phi2 = extract_phase_at_freq(X, f2_idx)
    phi_sum = extract_phase_at_freq(X, f1_idx + f2_idx)
    
    # Phase coupling: phi_1 + phi_2 - phi_{1+2}
    phase_diff = phi1 + phi2 - phi_sum
    
    # Synchronization index: mean resultant length
    sync_index = np.abs(np.mean(np.exp(1j * phase_diff)))
    
    return sync_index


# =============================================================================
# TEST CLASSES
# =============================================================================

class BispectrumProbe(Test):
    """
    PROBING: Detect nonlinear mode coupling via bispectrum.
    """
    name = "Bispectral Mode Coupling Analysis"
    question = (
        "Do different oscillation frequencies interact nonlinearly? The bispectrum "
        "measures three-frequency correlations. Non-zero values indicate that "
        "energy transfers between modes (nonlinear dynamics)."
    )
    reference = "Bispectral analysis, nonlinear signal processing"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: Linear systems have independent modes (zero bispectrum). "
        "Nonlinear systems show mode coupling: energy can transfer from one "
        "frequency to another. This probes whether the field dynamics is "
        "fundamentally linear or nonlinear."
    )

    def derivation(self):
        return (
            Derivation()
            .step("BISPECTRUM:")
            .equation("B(f1, f2) = <X(f1) * X(f2) * X*(f1+f2)>")
            .step("Three-frequency correlation")
            .step("BICOHERENCE (normalized):")
            .equation("b^2 = |B|^2 / (|X(f1)X(f2)|^2 * |X(f1+f2)|^2)")
            .step("Range [0, 1]: 0 = no coupling, 1 = perfect coupling")
            .step("LINEAR SYSTEMS: b^2 = 0 (phases are random)")
            .step("NONLINEAR: b^2 > 0 (phases are locked)")
            .conclude("Bicoherence reveals nonlinear mode interactions.")
        )

    def model(self):
        n_steps = 4096
        history = get_vertex_history(n_steps)
        
        # Convert to signal
        signal = np.array([1 if v in TET_A else -1 for v in history], dtype=float)
        
        # Compute bicoherence
        bicoh = compute_bicoherence(signal, max_freq_idx=30)
        
        # Find significant couplings
        couplings = find_significant_couplings(bicoh, threshold=0.2)
        
        # Summary statistics
        max_bicoh = np.max(bicoh[1:, 1:])  # Exclude DC
        mean_bicoh = np.mean(bicoh[1:, 1:])
        
        # Number of significant couplings
        n_couplings = len(couplings)
        
        return (
            Model()
            .add("Max bicoherence", max_bicoh)
            .add("Mean bicoherence", mean_bicoh)
            .add("Number of significant couplings", n_couplings)
            .add("Is nonlinear", 1.0 if max_bicoh > 0.3 else 0.0)
        )

    def observations(self):
        # NULL: Linear (zero bicoherence)
        return (
            Observed()
            .add("Max bicoherence", 0.0)
            .add("Mean bicoherence", 0.0)
            .add("Number of significant couplings", 0)
            .add("Is nonlinear", 0.0)
        )


class PhaseSynchronizationProbe(Test):
    """
    PROBING: Test for phase synchronization between modes.
    """
    name = "Phase Synchronization Analysis"
    question = (
        "Are the phases of different frequency components locked together? "
        "Phase synchronization is another signature of nonlinear coupling "
        "and appears in many complex systems."
    )
    reference = "Phase synchronization, Arnold tongues"
    level = Exploratory
    tolerance = 0.3

    commentary = (
        "PROBING: In synchronized systems, the phase relationship between "
        "modes is stable over time. We measure the phase synchronization "
        "index between the dominant mode and its harmonics."
    )

    def derivation(self):
        return (
            Derivation()
            .step("PHASE SYNCHRONIZATION:")
            .step("For two signals at frequencies f1 and f2:")
            .equation("phi_rel = n*phi_1 - m*phi_2")
            .step("If phases are locked, phi_rel is roughly constant.")
            .step("SYNCHRONIZATION INDEX:")
            .equation("R = |<exp(i * phi_rel)>|")
            .step("R = 0: no sync (random phases)")
            .step("R = 1: perfect sync (locked phases)")
            .conclude("Phase synchronization indicates coupled dynamics.")
        )

    def model(self):
        n_steps = 4096
        history = get_vertex_history(n_steps)
        signal = np.array([1 if v in TET_A else -1 for v in history], dtype=float)
        
        # Find dominant frequency
        power = np.abs(np.fft.rfft(signal - np.mean(signal))) ** 2
        dominant_idx = np.argmax(power[1:30]) + 1
        
        # Compute synchronization with harmonics
        sync_2nd = compute_phase_synchronization(signal, dominant_idx, dominant_idx)
        sync_3rd = compute_phase_synchronization(signal, dominant_idx, 2 * dominant_idx)
        
        # Overall synchronization
        mean_sync = (sync_2nd + sync_3rd) / 2
        
        return (
            Model()
            .add("Dominant frequency index", dominant_idx)
            .add("Sync with 2nd harmonic", sync_2nd)
            .add("Sync with 3rd harmonic", sync_3rd)
            .add("Mean synchronization", mean_sync)
            .add("Is synchronized", 1.0 if mean_sync > 0.3 else 0.0)
        )

    def observations(self):
        # NULL: No synchronization
        return (
            Observed()
            .add("Dominant frequency index", 1)
            .add("Sync with 2nd harmonic", 0.0)
            .add("Sync with 3rd harmonic", 0.0)
            .add("Mean synchronization", 0.0)
            .add("Is synchronized", 0.0)
        )


# =============================================================================
# TEST RUNNER
# =============================================================================

ALL_TESTS = [
    BispectrumProbe,
    PhaseSynchronizationProbe,
]


def run_all():
    """Run all mode coupling probing tests."""
    summary = (
        "MODE COUPLING PROBING\n\n"
        "These probes test for nonlinear interactions between modes.\n"
        "Bispectrum: three-frequency correlations\n"
        "Phase synchronization: locked phase relationships\n\n"
        "We are DISCOVERING if the dynamics is linear or nonlinear."
    )
    return run_tests("Mode Coupling Probing", summary, ALL_TESTS)


if __name__ == "__main__":
    import sys
    success = run_all()
    sys.exit(0 if success else 1)
