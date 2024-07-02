import numpy as np
from pyhackrf2 import HackRF
from gcpds.filters import frequency as flt
import logging

########################################################################
class scanning:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, bandwidth=20e6, samples_limit=5e5, vga_gain=16, lna_gain=0, amp_status=False):
        """Constructor"""
        self.hackrf = HackRF()
        self.hackrf.filter_bandwidth = bandwidth
        self.hackrf.sample_count_limit = samples_limit
        self.hackrf.vga_gain = vga_gain     # Baseband gain
        self.hackrf.lna_gain = lna_gain     # IF gain
        self.hackrf.amplifier_on = amp_status

    # ----------------------------------------------------------------------
    def scan(self, start=88e6, stop=108e6, sample_rate=20e6, duration=0.1):
        """"""
        self.start = start
        self.stop = stop
        self.sample_rate = sample_rate
        self.duration = duration

        if (stop - start) > sample_rate:
            raise ValueError("El rango de frecuencias no se puede manejar Sen un solo ensamblaje con la tasa de muestreo proporcionada.")

        self.hackrf.sample_rate = self.sample_rate
        self.hackrf.center_freq = (self.start + self.stop) / 2

        num_samples = int(self.sample_rate * self.duration)

        iq_samples = self.hackrf.read_samples(num_samples) #Aquí se genera el error

        high100 = flt.GenericButterHighPass(f0=0.01, N=1)
        iq_samples = high100(iq_samples, fs=250)

        i, q = np.real(iq_samples), np.imag(iq_samples)

        return i, q

    # ----------------------------------------------------------------------
    def wide_scan(self, start=88e6, stops=108e6, sample_rate=20e6, duration=0.1):
        """"""
        self.start = start
        self.stops = stops
        self.sample_rate = sample_rate
        self.duration = duration
        self.freq = start


        while self.freq < self.stops:
            logging.debug(f"Scanning frequency: {(self.freq + self.sample_rate/2) / 1e6} MHz con un sample rate de: {self.sample_rate/1e6}M")
            i, q = self.scan(self.freq, self.freq+self.sample_rate, self.sample_rate, self.duration)

            self.freq += self.sample_rate

        return i, q


    # ----------------------------------------------------------------------
    def read(self, '.h5'):
        """"""


    # ----------------------------------------------------------------------
    def write(self):
        """"""
