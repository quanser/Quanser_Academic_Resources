# region: system imports
import numpy as np
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.keyboard import QKeyboard
from matplotlib import pyplot as plt
# endregion 

# region: observer definition 
# <NO SCOPE DEFINED>
# endregion

# region: experiment constants
simulationTime = 120 # will run for this amount of seconds
frequency = 200 # Hz
counter = 0
samples = 0
data = []
minMeasurementValue = 0.1
stepBetweenMeasurements = 0.05
maximumMeasurementValue = 0.8

numSamples = int((maximumMeasurementValue - minMeasurementValue)/stepBetweenMeasurements)
# endregion 


# region: experiment
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
keyboardInput = QKeyboard()
print("Press SPACE to record a measurement, a total of ", numSamples+1, "will be recorded.")
with SensorsTrainer() as sensors:

    while timer.check():
        sensors.read_outputs()
        infrared = sensors.IRDistance
        if counter%30 == 0:
            keyboardInput.update()
            if bool(keyboardInput.states[keyboardInput.K_SPACE]):
                # append data [voltage, distance]
                distance = minMeasurementValue
                data.append([infrared,distance + stepBetweenMeasurements *(samples)])
                print(f"Recorded Voltage: {infrared:.3f}     Distance (m): {distance + 0.05 * (samples):.3f} samples: {samples+1}   (space pressed)")

                samples += 1

                print("value appended")
        counter += 1
        if samples > numSamples:
            break
        timer.sleep()

# endregion

# region: perform linear regression to fit data

# convert to numpy array and take log 
npData = np.log(np.array(data) + 1e-9)  # avoid log(0)

sizeData = np.size(npData, axis=0)


# mean of voltage and distance
m_voltage = np.mean(npData[:,0])
m_distance = np.mean(npData[:,1])

# cross deviation and variance
SS_xy = np.sum(npData[:,0]*npData[:,1]) - sizeData*m_voltage*m_distance
SS_xx = np.sum(npData[:,0]*npData[:,0]) - sizeData*m_voltage*m_voltage      

# regression coefficients
b1 = SS_xy / SS_xx
b0 = m_distance - b1*m_voltage 

# return to original scale
b0 = np.exp(b0)
b1 = b1

print(f"Fitted curve: Distance = {b0:.3f} * Voltage^({b1:.3f})")
# endregion

#region: plot recorded data and fitted curve
voltages = np.linspace(0.4,2.5,100)
distances = b0 * voltages**b1
plt.scatter(np.exp(npData[:,1]), np.exp(npData[:,0]), label="Recorded Data")
plt.plot(distances,voltages, color='red', label="Fitted Curve")
plt.xlabel("Distance (m)")
plt.ylabel("Voltage (V)")             
plt.legend()
plt.show()

#endregion