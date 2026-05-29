#import sys
#sys.path.append('../libraries/')
import numpy as np

from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.qcar import QLabsQCar
from qvl.basic_shape import QLabsBasicShape
from qvl.environment_outdoors import QLabsEnvironmentOutdoors
from qvl.traffic_light import QLabsTrafficLight
from qvl.stop_sign import QLabsStopSign
from qvl.spline_line import QLabsSplineLine
from qvl.qcar2 import QLabsQCar2

qlabs = QuanserInteractiveLabs()

print("Connecting to QLabs...")
qlabs.open("localhost")

# destroy all spawned actors to reset the scene
print("Deleting current spawned actors...")
qlabs.destroy_all_spawned_actors()


print("Spawning new actors...")

hEnvironmentOutdoors = QLabsEnvironmentOutdoors(qlabs)
#hEnvironmentOutdoors.set_time_of_day(24) #1:00pm
hEnvironmentOutdoors.set_time_of_day(13) #1:00pm
hEnvironmentOutdoors.set_weather_preset(hEnvironmentOutdoors.CLEAR_SKIES)

#offset = np.array([5.86, -2.587, 0])

# First QCar 1 spawned in
car1 = QLabsQCar(qlabs)
car1.spawn_id_degrees(actorNumber=1, 
                      location=[11.5, -8.2, 0.005], 
                      rotation=[0, 0, 180], 
                      scale=[1, 1, 1], 
                      configuration=0, 
                      waitForConfirmation=True)

basicshape1 = QLabsBasicShape(qlabs)
basicshape1.spawn_id_and_parent_with_relative_transform(actorNumber=101, 
                                                        location=[1.15, 0, 1.8], 
                                                        rotation=[0, 0, 0], 
                                                        scale=[.65, .65, .1], 
                                                        configuration=basicshape1.SHAPE_SPHERE, 
                                                        parentClassID=car1.ID_QCAR, 
                                                        parentActorNumber=1, 
                                                        parentComponent=1,  
                                                        waitForConfirmation=True)
basicshape1.set_material_properties(color=[0,0.4,0], roughness=0.4, metallic=True, waitForConfirmation=True)

# Second QCar 1 spawned in
car2 = QLabsQCar(qlabs)
car2.spawn_id_degrees(actorNumber=2, 
                      location=[0, 20, 0.005], 
                      rotation=[0, 0, -90], 
                      scale=[1, 1, 1], 
                      configuration=0, 
                      waitForConfirmation=True)

basicshape2 = QLabsBasicShape(qlabs)
basicshape2.spawn_id_and_parent_with_relative_transform(actorNumber=102, 
                                                        location=[1.15, 0, 1.8], 
                                                        rotation=[0, 0, 0], 
                                                        scale=[.65, .65, .1], 
                                                        configuration=basicshape2.SHAPE_SPHERE, 
                                                        parentClassID=car2.ID_QCAR, 
                                                        parentActorNumber=2, 
                                                        parentComponent=1,  
                                                        waitForConfirmation=True)
basicshape2.set_material_properties(color=[0.8,0.8,0], roughness=0.4, metallic=True, waitForConfirmation=True)

# Third QCar 1 spawned in
car3 = QLabsQCar(qlabs)
car3.spawn_id_degrees(actorNumber=3, 
                      location=[-18, -2.5, 0.005], 
                      rotation=[0, 0, -45], 
                      scale=[1, 1, 1], 
                      configuration=0, 
                      waitForConfirmation=True)

basicshape3 = QLabsBasicShape(qlabs)
basicshape3.spawn_id_and_parent_with_relative_transform(actorNumber=103, 
                                                        location=[1.15, 0, 1.8],
                                                         rotation=[0, 0, 0], 
                                                         scale=[.65, .65, .1], 
                                                         configuration=basicshape3.SHAPE_SPHERE, 
                                                         parentClassID=car3.ID_QCAR, 
                                                         parentActorNumber=3, 
                                                         parentComponent=1,  
                                                         waitForConfirmation=True)
basicshape3.set_material_properties(color=[0.4,0,0], roughness=0.4, metallic=True, waitForConfirmation=True)

# VIRTUAL QCar 2 (Fourth QCar)
car4 = QLabsQCar2(qlabs)
car4.spawn_id_degrees(actorNumber=4, 
                      location=[23.361, 47.763, 0.2], 
                      rotation=[0, 0, 210], 
                      scale=[1, 1, 1], 
                      configuration=0, 
                      waitForConfirmation=True)

car4.set_led_strip_uniform(color=[0.8, 0, 0.8])

# VIRTUAL QCar 2 (Fifth QCar)
car5 = QLabsQCar2(qlabs)
car5.spawn_id_degrees(actorNumber=5, 
                      location=[-23.0, 43.228, 0.2], 
                      rotation=[0, 0, -30], 
                      scale=[1, 1, 1], 
                      configuration=0, 
                      waitForConfirmation=True)

car5.set_led_strip_uniform(color=[0.05, 0.05, 1])

# Spawn Cameras
myCamera0 = QLabsFreeCamera (qlabs)
myCamera0.spawn(location=[24.142, -17.5, 14.233], rotation=[0, 0.576, 2.336])
myCamera1 = QLabsFreeCamera (qlabs)
myCamera1.spawn_degrees(location=[2.859, -23.782, 30.361], rotation=[0, 43, 90])
myCamera1.possess()

# stop signs
myStopSign = QLabsStopSign(qlabs)
myStopSign.spawn_degrees ([24.5, 4.5, 0.2], [0, 0, -90], [1.0, 1.0, 1.0], False)
myStopSign.spawn_degrees ([8, 13.5, 0.2], [0, 0, 0], [1.0, 1.0, 1.0], False)

#spawnSplineLineTwoPoint(qlabs, deviceNumber=20, p1=[2, -4.1, 0.05], p2=[2, -6.9, 0.05], lineWidth=10, color=[1, 1, 1])
mySpline = QLabsSplineLine(qlabs)
mySpline.spawn_degrees(location=[2, -4.1, 0.05], rotation=[0, 0, 0], scale=[1, 1, 1], configuration=0, waitForConfirmation=True)
qlabs.close()
print("Done!")  
