# Visualizing Microphone data from Sensors Trainer
# In this section of the experiment, we will visualize real-time audio data
# captured from the microphone on the Sensors Trainer using the AudioVisualizer class.

# region: Python level imports
from visualizer import AudioVisualizer
from pal.products.sensors import  find_audio_in
# endregion

# region: Create and start the audio visualizer
input_device = find_audio_in("Sensors Trainer")
vis = AudioVisualizer(input_device=input_device,
                        sample_rate=44100, 
                        block_size=1024, 
                        waveform_max_time_blocks=1,
                        waveform_yrange = (-0.1, 0.1),
                        # show_fft=True,
                        # fft_block_size= 1024,
                        # fft_xrange=(0,20000),
                        # fft_yrange=(0,5)
                        )
vis.start()
# endregion
input("Press Enter to exit...")
