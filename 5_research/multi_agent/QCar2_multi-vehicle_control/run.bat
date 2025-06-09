::   For this to run, open first Quanser Interactive labs, self driving car studio/CityScape or CityScape Lite. 
:: It will spawn two QCar 2s. It will also have two windows for vehicle control asking which QCar is going to be used (QCar1 or QCar 2). Type 2 on both windows and click enter. The cars should start driving. 
:: If you are running it again and it has issues, exit the environment and go into it again (menu and then again to CityScape or CityScape Lite)

start cmd /k start "" python initCars.py

TIMEOUT /T 5
start "" python vehicle_control.py
TIMEOUT /T 1
start "" python vehicle_control2.py

cmd /k