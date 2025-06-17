from pal.products.qdrone2 import QDrone2StreamStack
from q_setup import IPs
import time

# ipServer = 'localhost'
ipServer = IPs["GroundPC"]

qd2DataClient = QDrone2StreamStack(ip=ipServer)

startTime = time.time()
def elapsed_time():
    return time.time() - startTime

try:
    while True:
        new = qd2DataClient.read(timestamp= time.time() - startTime)

        if new:
            print('IMU_0 Accelerometer & Gyroscope: ', qd2DataClient.imu_0_raw)
            # print('IMU_1 Accelerometer & Gyroscope: ', qd2DataClient.imu_1_raw)
            # print('IMU_0 derived state vec (rad, rad/s, rad/s/s)', qd2DataClient.state_vec_0)
            # print('IMU_1 derived state vec (rad, rad/s, rad/s/s)', qd2DataClient.state_vec_1)
            # print('Net derived state vec (rad, rad/s, rad/s/s)', qd2DataClient.state_vec)
            # print('Motor Current', qd2DataClient.motorCurrent)
            # print('Motor Commands', qd2DataClient.motorCmd)
            # print('Battery Voltage', qd2DataClient.battVoltage)
            # print('Low Batter', qd2DataClient.lowBattery)

except KeyboardInterrupt:
    pass

finally:
    qd2DataClient.terminate()
