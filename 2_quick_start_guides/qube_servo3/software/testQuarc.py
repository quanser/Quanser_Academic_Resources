from quanser.hardware import HIL
import numpy as np

myDev = HIL()
myDev.open('null_device', '0')

input_channels = np.array([0], dtype=np.uint32)
output_channels = np.array([0], dtype=np.uint32)
num_input_channels = len(input_channels)
num_output_channels = len(output_channels)
input_buffer = np.zeros(num_input_channels, dtype=np.float64)
output_buffer = np.array([0.5], dtype=np.float64)

ret = myDev.read_analog_write_analog(input_channels, num_input_channels,
                            output_channels, num_output_channels,
                            input_buffer,
                            output_buffer)
if ret is None:
    print('Pass')
else:
    print('Fail')

myDev.close()