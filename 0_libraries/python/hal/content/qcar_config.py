
"""This is a modified version of qcar_config.py for interfacing virtual Qcar2 in a 
   remote machine. Currenly only used by the Lane Keeping lab.
"""
import numpy as np
from quanser.hardware import HIL, HILError
import json
from os.path import split,abspath,join,realpath,dirname
from os import getlogin
import platform

class QCar_check():
    def __init__(self,IS_PHYSICAL,remote_ip='172.16.4.61'):
        self.card = HIL()
        # initialize with QCar 1 parameters
        self.dict={'cartype':1,
                   'carname':'qcar',
                   'lidarurl':"serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'",
                   'WHEEL_RADIUS': 0.066/2,
                   'WHEEL_BASE':0.256,
                   "PIN_TO_SPUR_RATIO":(13.0*19.0) / (70.0*37.0), ### same for both
                   "WRITE_PWM_CHANNELS": [0], #np.array([0], dtype=np.int32),
                   'WRITE_OTHER_CHANNELS':[1000, 11008, 11009, 11010, 11011, 11000, 11001, 11002, 11003],
                                           #np.array([1000, 11008, 11009, 11010, 11011, 11000, 11001, 11002, 11003], dtype=np.int32),
                   'WRITE_DIGITAL_CHANNELS':[-1], # None
                   'writePWMBuffer': 1, #np.zeros(1, dtype=np.float64),
                   'writeDigitalBuffer': 1, # None
                   'writeOtherBuffer': 9, #np.zeros(9, dtype=np.float64),
                   'READ_ANALOG_CHANNELS':[5, 6], #np.array([5, 6], dtype=np.int32),
                   'READ_ENCODER_CHANNELS':[0], #np.array([0], dtype=np.uint32), ### same for both
                   'READ_OTHER_CHANNELS':[3000, 3001, 3002, 4000, 4001, 4002, 14000], 
                                        #np.array([3000, 3001, 3002, 4000, 4001, 4002, 14000],dtype=np.int32), ### same for both
                   'readAnalogBuffer': 2, #np.zeros(2, dtype=np.float64), ### same for both
                   'readEncoderBuffer': 1, #np.zeros(1, dtype=np.int32), ### same for both
                   'readOtherBuffer': 7, #np.zeros(7, dtype=np.float64), ### same for both
                   'csiRight': 0,
                   'csiBack':1,
                   'csiLeft':2,
                   'csiFront':3,
                   'lidarToGps':'qcarLidarToGPS.rt-linux_nvidia',
                   'captureScan':'qcarCaptureScan.rt-linux_nvidia',
                   'remote_ip':remote_ip
                   }
        if IS_PHYSICAL:
            self.check_car_type()
        else:
            # self.dict['cartype']=0
            # virtual_cartype = input('Would you like to use virtual QCar1 or QCar2? (enter 1 or 2)')
            virtual_cartype = '2'
            if virtual_cartype =='1':
                self.set_qcar1_params()
            elif virtual_cartype =='2':
                self.set_qcar2_params()
            else:
                print('Wrong car type:', virtual_cartype)
                exit()
        self.create_config()

    def check_car_type(self):
        try:
            self.card.open("qcar", "0")
            if self.card.is_valid():
                pass
        except HILError as e:            
            if str(e) == '-986':
                self.dict['cartype']=0
                pass
            else:
                print(e.get_error_message())

        if self.dict['cartype']==0:
            try:
                self.card.open("qcar2", "0")
                if self.card.is_valid():
                    self.set_qcar2_params()

            except HILError as e:            
                if str(e) == '-986':
                    self.dict['cartype']=0
                    pass
                else:
                    print(e.get_error_message())

    def create_config(self):
        name='qcar_config.json'
        qcar_env=dirname(realpath(__file__))
        save_path=join(qcar_env,name)
        with open(save_path,'w') as outfile:
            json.dump(self.dict,outfile)
        self.card.close()
    
    def set_qcar1_params(self):
        self.dict['cartype']=1
        self.dict['carname']='qcar'
        self.dict['lidarurl']="serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'"
        self.dict['WHEEL_RADIUS'] = 0.066/2
        self.dict['WHEEL_BASE'] = 0.256
        self.dict['PIN_TO_SPUR_RATIO'] = (13.0*19.0) / (70.0*37.0)  ### same for both
        self.dict['WRITE_PWM_CHANNELS'] = [0] # None
        self.dict['WRITE_OTHER_CHANNELS'] = [1000, 11008, 11009, 11010, 11011, 11000, 11001, 11002, 11003]
        self.dict['WRITE_DIGITAL_CHANNELS'] = [-1]
        self.dict['writePWMBuffer'] = 1
        self.dict['writeDigitalBuffer'] = 1 
        self.dict['writeOtherBuffer'] = 9 
        self.dict['READ_ANALOG_CHANNELS'] = [5, 6] #np.array([4, 2], dtype=np.int32)
        self.dict['READ_ENCODER_CHANNELS'] = [0] #np.array([0], dtype=np.uint32) ### same for both
        self.dict['READ_OTHER_CHANNELS'] = [3000, 3001, 3002, 4000, 4001, 4002, 14000] ### same for both
        self.dict['readAnalogBuffer'] = 2 #np.zeros(2, dtype=np.float64) ### same for both
        self.dict['readEncoderBuffer'] = 1 #np.zeros(1, dtype=np.int32) ### same for both
        self.dict['readOtherBuffer'] = 7 #np.zeros(7, dtype=np.float64) ### same for both
        self.dict['csiRight'] = 0
        self.dict['csiBack'] = 1
        self.dict['csiLeft'] = 2
        self.dict['csiFront'] = 3
        self.dict['lidarToGps']='qcarLidarToGPS.rt-linux_nvidia'
        self.dict['captureScan']='qcarCaptureScan.rt-linux_nvidia'

    def set_qcar2_params(self):
        self.dict['cartype']=2
        self.dict['carname']='qcar2'
        self.dict['lidarurl']="serial-cpu://172.16.4.61:1?baud='256000',word='8',parity='none',stop='1',flow='none',dsr='on'"
        self.dict['WHEEL_RADIUS'] = 0.066/2
        self.dict['WHEEL_BASE'] = 0.256
        self.dict['PIN_TO_SPUR_RATIO'] = (13.0*19.0) / (70.0*37.0)  ### same for both
        self.dict['WRITE_PWM_CHANNELS'] = [-1] # None
        self.dict['WRITE_OTHER_CHANNELS'] = [1000, 11000] #np.array([1000, 11000],dtype=np.int32)
        self.dict['WRITE_DIGITAL_CHANNELS'] = [17, 18, 25, 26, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24]
                                            #np.array([17, 18, 25, 26, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24],dtype=np.int32)
        self.dict['writePWMBuffer'] = 1 # None
        self.dict['writeDigitalBuffer'] = 16 #np.zeros(16, dtype=np.int8)
        self.dict['writeOtherBuffer'] = 2 #np.zeros(2, dtype=np.float64)
        self.dict['READ_ANALOG_CHANNELS'] = [4, 2] #np.array([4, 2], dtype=np.int32)
        self.dict['READ_ENCODER_CHANNELS'] = [0] #np.array([0], dtype=np.uint32) ### same for both
        self.dict['READ_OTHER_CHANNELS'] = [3000, 3001, 3002, 4000, 4001, 4002, 14000]
                                            #np.array([3000, 3001, 3002, 4000, 4001, 4002, 14000],dtype=np.int32) ### same for both
        self.dict['readAnalogBuffer'] = 2 #np.zeros(2, dtype=np.float64) ### same for both
        self.dict['readEncoderBuffer'] = 1 #np.zeros(1, dtype=np.int32) ### same for both
        self.dict['readOtherBuffer'] = 7 #np.zeros(7, dtype=np.float64) ### same for both
        self.dict['csiRight'] = 0
        self.dict['csiBack'] = 1
        self.dict['csiLeft'] = 3
        self.dict['csiFront'] = 2
        self.dict['lidarToGps']='qcar2LidarToGPS.rt-linux_qcar2'
        self.dict['captureScan']='qcar2CaptureScan.rt-linux_qcar2'

if __name__ == '__main__':
    IS_PHYSICAL_QCAR = ('nvidia' == getlogin()) \
    and ('aarch64' == platform.machine())
    test=QCar_check(IS_PHYSICAL_QCAR)
    qcar_env=dirname(realpath(__file__))
    read_path=join(qcar_env,'qcar_config.json')
    with open(read_path, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        for i in json_object:
            print (i,type(json_object[i]))
