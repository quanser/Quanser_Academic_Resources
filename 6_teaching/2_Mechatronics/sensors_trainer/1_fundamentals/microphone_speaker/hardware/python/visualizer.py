# Visualizer for real-time audio waveform and FFT using PyQt6 and pyqtgraph
import numpy as np
import sounddevice as sd
from collections import deque
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from scipy.signal.windows import hann
from scipy.fft import rfft, rfftfreq

class AudioVisualizer(QtWidgets.QWidget):
    '''Real-time audio visualizer with waveform and FFT plots.
    attributes:
        - sample_rate: Audio sampling rate in Hz
        - block_size: Number of samples per audio block
        - max_time_blocks: Number of past blocks to show in waveform
        - waveform_yrange: Y-axis range for waveform plot
        - show_fft: Whether to show the FFT plot
        - fft_block_size: Number of samples for FFT computation
        - fft_xrange: X-axis range for FFT plot
        - fft_yrange: Y-axis range for FFT plot
        - user_audio_callback: Optional user-defined callback for audio blocks
        - user_fft_callback: Optional user-defined callback for FFT results
        - stream: sounddevice InputStream for audio capture
        - timer: QTimer for GUI updates    
    '''
    def __init__(self, sample_rate=44100, block_size=1024, input_device=None,
                 waveform_max_time_blocks=8,waveform_yrange=(-1,1),
                 show_fft=False,fft_block_size=1024,fft_xrange=(0,22050),fft_yrange=(0,10),
                 user_audio_callback=None,user_fft_callback=None):
        '''Initialize the AudioVisualizer.'''
        # Must construct a QApplication before a QWidget
        self.app=QtWidgets.QApplication([])
        super().__init__()

        self.sample_rate = sample_rate
        self.block_size = block_size
        # How many past blocks to show in the waveform history
        self.max_time_blocks = waveform_max_time_blocks
        self.waveform_yrange = waveform_yrange
        self.waveform_buffer = deque(maxlen=self.block_size * self.max_time_blocks)
        self.show_fft = show_fft

        if self.show_fft:    
            # check if fft block size is a multiple of audio block size
            self.fft_block_size = fft_block_size
            if self.fft_block_size % self.block_size != 0:
                raise ValueError("FFT block size must be a multiple of audio block size.")
            self.fft_buffer = deque(maxlen=self.fft_block_size)
            self.fft_xrange = fft_xrange
            self.fft_yrange = fft_yrange
            # FFT frequency axis [0, ... , sample_rate/2], length = block_size//2 +1
            self.freqs = rfftfreq(self.fft_block_size, d=1.0 / self.sample_rate)



        # Initialize the Visualizer UI
        self.init_ui()
        self.user_audio_callback = user_audio_callback
        self.user_fft_callback = user_fft_callback

        # Initialize sounddevice stream
        self.stream = sd.InputStream(
            device=input_device,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=1,
            callback=self.audio_callback,
        )

        # Timer for GUI updates
        self.timer = QtCore.QTimer()
        self.timer.setInterval(30)  # ms
        self.timer.timeout.connect(self.update_plots)

    def init_ui(self):
        '''Set up the UI layout and plots.'''

        layout = QtWidgets.QVBoxLayout(self)

        # Waveform plot
        self.plot_wave = pg.PlotWidget(title="Waveform (time domain)")
        self.curve_wave = self.plot_wave.plot(pen='c')
        self.plot_wave.setLabel('bottom', "Time", units='s')
        self.plot_wave.setLabel('left', "Amplitude")
        layout.addWidget(self.plot_wave)

        if self.show_fft:
            # FFT plot
            self.plot_fft = pg.PlotWidget(title="FFT (magnitude)")
            self.curve_fft = self.plot_fft.plot(pen='m')
            self.plot_fft.setLabel('bottom', "Frequency (Hz)")
            self.plot_fft.setLabel('left', "Magnitude")
            layout.addWidget(self.plot_fft)
        
        self.setWindowTitle("Audio Visualizer")
        self.resize(800, 600)

    def audio_callback(self, indata, frames, time, status):
        """Called in audio thread when each block arrives."""
        if status:
            print("Audio callback status:", status)
        # indata shape = (frames, channels)
        block = indata[:, 0].copy()
        # Append to waveform buffer
        self.waveform_buffer.extend(block)
        self.latest_block = block

        if hasattr(self, 'user_audio_callback') and callable(self.user_audio_callback):
            self.user_audio_callback(indata)

    def __enter__(self):
        """Start  the stream in the beginning of a "with" statement."""
        self.start()
        return self

    def __exit__(self, *args):
        """Stop and close the stream when exiting a "with" statement."""
        self.stop()

    def start(self):
        '''Start the audio stream and GUI.'''
        self.show()
        self.stream.start()
        self.timer.start()
        self.app.exec()

    def stop(self):
        '''Stop the audio stream and GUI.'''
        self.timer.stop()
        self.stream.stop()
        self.stream.close()

    def update_plots(self):
        '''Update the waveform and FFT plots.'''
        # --- Waveform update ---
        if len(self.waveform_buffer) > 0:
            buf = np.array(self.waveform_buffer)
            # Time axis: sample indices to seconds
            times= np.linspace(-len(buf) / self.sample_rate, 0, len(buf))

            self.curve_wave.setData(times, buf)
            # Limit waveform y-axis
            self.plot_wave.setYRange(self.waveform_yrange[0], self.waveform_yrange[1])

        # --- FFT update ---
        if hasattr(self, "latest_block") and self.show_fft:
            self.fft_buffer.extend(self.latest_block)
            # Once we have enough samples, compute FFT
            if len(self.fft_buffer) == self.fft_block_size:
                # Apply window to reduce spectral leakage
                window = hann(self.fft_block_size,sym=False)
                fft_block = np.array(self.fft_buffer)
                block_win = fft_block * window
                fft_vals = rfft(block_win)
                mag = np.abs(fft_vals)
                self.curve_fft.setData(self.freqs, mag)

                # Optionally adjust view / autoscaling
                # E.g. limit FFT x-axis
                self.plot_fft.setXRange(self.fft_xrange[0],self.fft_xrange[1])
                self.plot_fft.setYRange(self.fft_yrange[0],self.fft_yrange[1])

                if hasattr(self, 'user_fft_callback') and callable(self.user_fft_callback):
                    self.user_fft_callback(mag,self.freqs)

