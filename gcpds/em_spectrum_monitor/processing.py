import numpy as np
from scipy.signal import welch, windows
from scipy.fftpack import fft
from scipy.signal import spectrogram

class Processing:
    """
    This class provides various methods for processing signals,
    including Fourier Transform, spectral estimation using Welch's method,
    Multi-taper method, and Wavelet transform.
    """

    # ----------------------------------------------------------------------
    def fft(self, signal: np.ndarray) -> np.ndarray:
        """
        Compute the Fast Fourier Transform of the given signal.

        Parameters
        ----------
        signal : np.ndarray
            An array representing the signal to be transformed where
            the real part is the in-phase component (I) and the imaginary part
            is the quadrature component (Q).

        Returns
        -------
        numpy.ndarray
            The transformed signal in the frequency domain.

        Raises
        ------
        ValueError
            If the input signal is not a numpy array.

        Notes
        -----
        This method utilizes NumPy's FFT function to transform the signal from
        the time domain to the frequency domain.
        """
        if not isinstance(signal, np.ndarray):
            raise ValueError("Input signal must be a numpy array")

        return np.fft.fft(signal)

    # ----------------------------------------------------------------------
    def welch(self, signal: np.ndarray, fs: float = 1.0) -> np.ndarray:
        """
        Estimate the power spectral density of the given signal using Welch's method.

        Parameters
        ----------
        signal : np.ndarray
            An array representing the signal to be analyzed where
            the real part is the in-phase component (I) and the imaginary part
            is the quadrature component (Q).
        fs : float, optional
            The sampling frequency of the signal. Default is 1.0.

        Returns
        -------
        numpy.ndarray
            The estimated power spectral density of the signal.

        Raises
        ------
        ValueError
            If the input signal is not a numpy array.

        Notes
        -----
        This method utilizes Welch's algorithm, implemented in NumPy, to estimate
        the power spectral density of the signal. The signal is divided into
        overlapping segments, windowed, and then averaged to reduce variance.
        """
        if not isinstance(signal, np.ndarray):
            raise ValueError("Input signal must be a numpy array")

        f, Pxx = welch(signal, fs=fs)
        return f, Pxx

    # ----------------------------------------------------------------------
    def multi_taper(self, signal: np.ndarray, fs: float = 1.0) -> np.ndarray:
        """
        Estimate the power spectral density of the given signal using the Multi-taper method.

        Parameters
        ----------
        signal : np.ndarray
            An array representing the signal to be analyzed where
            the real part is the in-phase component (I) and the imaginary part
            is the quadrature component (Q).
        fs : float, optional
            The sampling frequency of the signal. Default is 1.0.

        Returns
        -------
        numpy.ndarray
            The estimated power spectral density of the signal.

        Raises
        ------
        ValueError
            If the input signal is not a numpy array.

        Notes
        -----
        This method utilizes the Multi-taper method to estimate the power spectral
        density of the signal. The method is often favored for its ability to
        reduce spectral leakage and provide better frequency resolution. Multiple
        orthogonal windowing functions (tapers) are used to obtain independent
        estimates of the power spectrum, which are then averaged.
        """
        if not isinstance(signal, np.ndarray):
            raise ValueError("Input signal must be a numpy array")

        from mne.time_frequency import psd_array_multitaper

        psd, freqs = psd_array_multitaper(signal, sfreq=fs, adaptive=True, normalization='full', verbose=0)
        return freqs, psd

    # ----------------------------------------------------------------------
    def wavelet(self, signal: np.ndarray, scales: np.ndarray) -> np.ndarray:
        """
        Perform wavelet transform on the given signal.

        Parameters
        ----------
        signal : np.ndarray
            An array representing the signal to be transformed where
            the real part is the in-phase component (I) and the imaginary part
            is the quadrature component (Q).
        scales : np.ndarray
            An array of scales to use in the wavelet transform.

        Returns
        -------
        numpy.ndarray
            The wavelet-transformed signal in the time-frequency domain.

        Raises
        ------
        ValueError
            If the input signal is not a numpy array.

        Notes
        -----
        This method utilizes wavelet transform techniques to analyze the signal
        in both time and frequency domains. Wavelet transforms are highly effective
        for analyzing non-stationary signals.
        """
        if not isinstance(signal, np.ndarray):
            raise ValueError("Input signal must be a numpy array")

        import pywt

        coeffs, _ = pywt.cwt(signal, scales, 'cmor')
        return coeffs
