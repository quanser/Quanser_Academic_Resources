Run the 5 timing tests on your PC from the terminal opened in this directory.
>> python 0_timing_test.py
>> python 1_timing_blind.py
>> python 2_timing_relative.py
>> python 3_timing_absolute.py
>> python 4_quanser_timing.py

The very first example characterizes the overhead to sleeping.

The blind approach is not recommended at all, and pays no attention to any
time lost during computations or any time lost to the overhead of sleep.
The relative approach accounts for computation time per sample. The absolute
approach tallies against a global clock to maintain time, and hence accounts
for losses in computation and sleep overheard.

The final example expands on two timing modules available to you within
pal.utilities.timing.

