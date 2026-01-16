# Frequency Detection using Microphone Input
# In this sectin of the experiment, we will detect the dominant frequencies
# from the microphone input using FFT and peak detection.

# region: Python level imports
from visualizer import AudioVisualizer
from pal.products.sensors import  find_audio_in
# endregion

# region: define Frequency Detection Callback Class
class frequency_detection:
    def __init__(self):
        self.previous_peaks = []
        pass

    def __call__(self, mag, freqs):
        """
        callback function for FFT magnitude and frequency axis
        mag: magnitude of each frequency bin,
             numpy array of shape (fft_block_size//2 + 1,)
        freqs: frequency axis,
               numpy array of shape (fft_block_size//2 + 1,)
        """
        # --- complete you function here ---

        # -----------------------------
        
        pass
# endregion

# region: define and start main loop
input_device = find_audio_in("Quanser")
fft_callback = frequency_detection()
vis = AudioVisualizer(input_device=input_device,
                        sample_rate=44100, 
                        block_size=1024, 
                        waveform_max_time_blocks=1,
                        waveform_yrange = (-0.1, 0.1),
                        show_fft=True,
                        fft_block_size=1024,
                        fft_xrange=(5,20000),
                        fft_yrange=(0,5),
                        user_fft_callback=fft_callback
                        )
vis.start()
# endregion
