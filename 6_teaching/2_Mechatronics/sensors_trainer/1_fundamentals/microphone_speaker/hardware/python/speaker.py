# Generate and play audio signals through the Speaker output of the Sensors Trainer
# In this section of the experiment, you will generate sine wave audio signals 
# of user-defined frequencies, and play them through the Speaker output of the
# Sensors Trainer using the sounddevice library.

# region: Python level imports
import numpy as np
import sounddevice as sd
import time
from pal.products.sensors import  find_audio_out
# endregion 

# region: set up audio output parameters
output_device = find_audio_out("Quanser")
sampleRate = 44100        # sample rate
wave_duration = 5.0   # seconds per note
# endregion

# region: function to generate waveform
def generate_waveform(desiredFreq, sampleRate, duration):
    '''
    Generate a sine wave of desired frequency.
    args:
        desiredFreq: desired frequency in Hz (float)
        sampleRate: sample rate in Hz (int)
        duration: duration in seconds (float)
    
    return: numpy array of shape (sampleRate * duration, 1)
    '''
    # --- complete function hre ---
    wave = np.zeros((sampleRate, 1), dtype=np.float32)
    # -----------------------------
    return wave
# endregion

# region: main speaker loop
with sd.OutputStream(device= output_device, channels=1, samplerate=sampleRate) as stream:
    try:
        while True:
            ans = input("Enter desired frequency:")
            try:
                freq = float(ans)
                print(f"Playing {freq:.2f} Hz...")
                wave = generate_waveform(freq, sampleRate, wave_duration)
                stream.write(wave)

                time.sleep(1)
            except ValueError:
                print("Invalid input, need to be a number.")
    except KeyboardInterrupt:
        pass
# endregion
input ("Press Enter to exit...")


