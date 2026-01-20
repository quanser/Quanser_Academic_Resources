# TOF_3D.py
# Live visualization of TOF 3D point cloud using VisPy
# Mimics the behavior of your Open3D code, but compatible with Python 3.11-3.14

import numpy as np
import matplotlib.pyplot as plt

from vispy import scene, app
from vispy.color import Colormap

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer

# -----------------------------
# Experiment constants
# -----------------------------
simulationTime = 120   # seconds
frequency = 300        # Hz

FOV = 60               # Field of view in degrees
deltaAngle = np.linspace(-FOV / 2, FOV / 2, int(60 / 7)) * np.pi / 180

SCALE = 0.2  # Visualization scaling factor
TOFMeas3D = np.zeros((8, 8, 3), dtype=np.float64)

# Distance coloring
colormap = plt.get_cmap("viridis")  # Can also try "plasma", "jet", etc.viridis
vispy_cmap = Colormap(colormap(np.linspace(0, 1, 256))[:, :3])

# -----------------------------
# VisPy scene setup
# -----------------------------
canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True, bgcolor='white')
view = canvas.central_widget.add_view()

# Add XYZ axes
axes = scene.visuals.XYZAxis(parent=view.scene)

# Add a simple ground grid (wireframe)
grid_size = 0.24
grid_res = 12
x = np.linspace(-grid_size/2, grid_size/2, grid_res)
y = np.linspace(-grid_size/2, grid_size/2, grid_res)
for xi in x:
    line = scene.visuals.Line(pos=np.column_stack([np.full_like(y, xi), y, np.zeros_like(y)]),
                              color=(0.5, 0.5, 0.5, 0.8), parent=view.scene)
for yi in y:
    line = scene.visuals.Line(pos=np.column_stack([x, np.full_like(x, yi), np.zeros_like(x)]),
                              color=(0.5, 0.5, 0.5, 0.8), parent=view.scene)

# Preallocate 64-point cloud (8x8)
points_init = np.zeros((64, 3))
colors_init = np.zeros((64, 3))

# Create a VisPy Markers visual for point cloud
pcd = scene.visuals.Markers(parent=view.scene)
pcd.set_data(points_init, face_color=colors_init, size=10)

# Set camera 
view.camera = scene.TurntableCamera(fov=0, azimuth=-29, elevation=32, distance=0.018, center=[0,0,0])

# -----------------------------
# Timer for updates
# -----------------------------
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

# -----------------------------
# Main loop
# -----------------------------
with SensorsTrainer() as sensors:

    while timer.check():
        sensors.read_outputs()

        # Read TOF sensor values (8x8)
        TOFSensor = sensors.TOFDistance
        ToFMeasurements = np.flip((TOFSensor * sensors.TOFNumberOfTargets).reshape(8, 8), axis=0)

        # Compute 3D coordinates
        for i in range(8):
            for j in range(8):
                X = ToFMeasurements[i, j]

                dir_x = np.cos(-deltaAngle[i]) * np.sin(np.pi / 2 - deltaAngle[j])
                dir_y = np.cos(-deltaAngle[i]) * np.cos(np.pi / 2 - deltaAngle[j])
                dir_z = np.sin(-deltaAngle[i])

                if abs(dir_x) > 1e-6:
                    P = X / dir_x
                else:
                    P = 0.0

                TOFMeas3D[i, j, 0] = X
                TOFMeas3D[i, j, 1] = P * dir_y
                TOFMeas3D[i, j, 2] = max(P * dir_z + 0.045, 0.0)  # Sensor height offset, clamp floor

        # Flatten to 64x3 points
        points = TOFMeas3D.reshape(-1, 3) * SCALE

        # Distance-based coloring
        # Step 1. Compute Euclidean distance from origin (0, 0, 0) 
        distances = points[:, 0]

        # Step 2: Normalize distances to [0, 1]
        dist_min = 0.1
        dist_max = 0.3
        dist_norm = np.clip((distances - dist_min) / (dist_max - dist_min + 1e-8), 0.0, 1.0)
        colors = vispy_cmap.map(dist_norm)

        # Update the point cloud (in-place)
        pcd.set_data(points, face_color=colors, size=10)

        # Process VisPy GUI events (needed to actually display)
        app.process_events()

        timer.sleep()

# Close VisPy app (optional)
canvas.close()
