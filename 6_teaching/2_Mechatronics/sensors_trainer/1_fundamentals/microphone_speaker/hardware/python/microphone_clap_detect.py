# Clap detection using microphone data
# In this section of the experience, we will implement a simple clap detection 
# algorithm using microphone data.

# region: Python level imports
from visualizer import AudioVisualizer
from pal.products.sensors import  find_audio_in
# endregion

# region: define Clap Detection Callback Class
class clap_detection:
    def __init__(self):

        pass

    def __call__(self, indata):
        """
        callback function for audio blocks
        indata: input audio block,
                numpy array of shape (block_size, num_channels)
        """
        # --- complete function here ---
        
        # -----------------------------
        clapped = False
        if clapped:
            print("Clap detected!")
# endregion            

# region: start main program
input_device = find_audio_in("Quanser")
audio_callback = clap_detection()
vis = AudioVisualizer(input_device=input_device,
                        sample_rate=44100, 
                        block_size=1024, 
                        waveform_max_time_blocks=15,
                        waveform_yrange = (-1, 1),
                        user_audio_callback=audio_callback,
                        )
vis.start()
# endregion