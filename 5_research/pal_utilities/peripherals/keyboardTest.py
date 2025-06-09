import time

from pal.utilities.keyboard import KeyBoardDriver

keyboard = KeyBoardDriver(rate=10)

startTime = time.time()
then = startTime
def elapsed_time():
    return time.time() - startTime

try:
    while True:
        if not keyboard.connected:
            keyboard.checkConnection()
            startTime = time.time()
            then = startTime
        else:
            new = keyboard.update()
            if new:
                now = elapsed_time()
                print('Timing frequency:', 1/(now - then))

                # Note that printing will affect performance. Comment out the
                # print line below if selecting a 100 Hz or 500 Hz rate.
                keyboard.print()
                then = now

except KeyboardInterrupt as ke:
    print('Terminated.')
finally:
    keyboard.terminate()
