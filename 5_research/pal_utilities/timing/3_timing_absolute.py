#-----------------------------------------------------------------------------#
# Example 3: Characterize absolute sleeps that track computations & overhead.
#-----------------------------------------------------------------------------#

# This method uses a absolute timer to compare current loop progress
# against a global OS based clock. As such, this will track the time
# spent in computation as well as any overhead in going to sleep or
# waking up.

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

    # sleep duration reduced based on computation & overhead
    delta = min(elapsed_time() - counter*sample_time, sample_time)
    time.sleep(sample_time - delta)
    counter = counter + 1

print("Absolute Correction")
print("Total Simulation Time:", total_time, "seconds.")
print("Frequency:", 1/sample_time, "Hz.")
print("Total samples expected:", int(total_time/sample_time))
print("Elapsed Time:", f"{elapsed_time():.3f}", "seconds.")
print("Samples achieved:", counter)
print("Net lag time:", f"{elapsed_time()-counter*sample_time:.3f}", 'seconds.')