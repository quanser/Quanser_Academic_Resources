import os

__rtModelDirPath = os.environ['RTMODELS_DIR']

# QCar1 RT Models
QCAR = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QCar/QCar_Workspace'))

QCAR_STUDIO = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QCar/QCar_Workspace_studio'))

# QCar2 RT Models
QCAR2 = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QCar2/QCar2_Workspace'))

QCAR2_STUDIO = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QCar2/QCar2_Workspace_studio'))

# QBotPlatform RT Models
QBOT_PLATFORM = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QBotPlatform/QBotPlatform_Workspace'))

QBOT_PLATFORM_DRIVER = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QBotPlatform/qbot_platform_driver_virtual'))

# QDrone 2 RT Models
QDRONE2 = os.path.normpath(
    os.path.join(__rtModelDirPath, 'QDrone2/QDrone2_Workspace'))
