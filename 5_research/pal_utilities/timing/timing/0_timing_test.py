#-----------------------------------------------------------------------------#
# Example 0: Identify & characterize the "overhead" with simple sleep methods.
#-----------------------------------------------------------------------------#

import timeit
import time

sample_time = 0.01
num = 1000
cmd = 'time.sleep('+str(sample_time)+')'
achieved_sample_time = timeit.timeit(cmd, number=num)/num

print("Average time taken when sleeping for:", f"{sample_time:.3f}",
      "seconds is:", f"{achieved_sample_time:.3f}", "seconds.")

print("Average overhead:", f"{achieved_sample_time - sample_time:.3f}",
      "seconds. That is about:",
      f"{100*(achieved_sample_time - sample_time)/sample_time:.0f}",
      "% extra.")