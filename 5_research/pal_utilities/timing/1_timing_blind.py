#-----------------------------------------------------------------------------#
# Example 1: Characterize blind sleeps.
#-----------------------------------------------------------------------------#

# This method uses a blind and fixed sleep duration at each loop iteration.
# This does not track the time spent in computation, or the overhead and hence
# is expected to fall behind.

import time

# Computation task takes approximately 7 to 9 ms
def computation():
    num = 0
    for val in range(400000):
        num = num + val

total_time = 10     # 10  s simulation
sample_time = 0.01  # 10 ms sample time

startTime = time.time()

def elapsed_time():
    return time.time() - startTime
counter = 0

while elapsed_time() <= total_time:
    computation()

    # blind sleep duration
    time.sleep(sample_time)

    counter = counter + 1

print("Blind sleep")
print("Total Simulation Time:", total_time, "seconds.")
print("Frequency:", 1/sample_time, "Hz.")
print("Total samples expected:", int(total_time/sample_time))
print("Elapsed Time:", f"{elapsed_time():.3f}", "seconds.")
print("Samples achieved:", counter)
print("Net lag time:", f"{elapsed_time()-counter*sample_time:.3f}", 'seconds.')