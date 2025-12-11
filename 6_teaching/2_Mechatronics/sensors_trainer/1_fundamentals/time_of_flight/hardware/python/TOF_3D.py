# TOF_3D.py
# This script reads Time-of-Flight (TOF) sensor data from a Sensors Trainer
# and visualizes the 3D point cloud using Open3D.

# region: Python level imports
import numpy as np
import open3d as o3
import numpy as np
import matplotlib.pyplot as plt

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsDisplay

# endregion

# region: Helper Functions
def create_ground_grid_xy(rows=8, cols=8, spacing=0.02, z=0.001, color=[0.1, 0.1, 0.1]):
    points = []
    lines = []

    for i in range(rows + 1):
        y = i * spacing
        points.append([0, y, z])
        points.append([cols * spacing, y, z])
        lines.append([len(points) - 2, len(points) - 1])

    for j in range(cols + 1):
        x = j * spacing
        points.append([x, 0, z])
        points.append([x, rows * spacing, z])
        lines.append([len(points) - 2, len(points) - 1])

    grid = o3.geometry.LineSet()
    grid.points = o3.utility.Vector3dVector(points)
    grid.lines = o3.utility.Vector2iVector(lines)
    grid.colors = o3.utility.Vector3dVector([color] * len(lines))

    # Center the grid at origin
    grid.translate([-cols * spacing / 2, -rows * spacing / 2, 0])
    return grid

# endregion

# region: Experiment constants

simulationTime = 120 # will run for this amount of seconds
frequency =  300 #Hz

counter = 0 # counter to track scopes


FOV = 60
deltaAngle = np.linspace(-FOV/2,FOV/2,int(60/7))*np.pi/180
TOFDist = np.ones((8,8), dtype=np.float64)
TOFMeas3D = np.ones((8,8,3), dtype=np.float64)
distortion_map = np.zeros((8, 8))  # store Z error per pixel
calibration_points = None

vis = o3.visualization.Visualizer()
vis.create_window(window_name="ToF Live Update", width=800, height=600)

axis = o3.geometry.TriangleMesh.create_coordinate_frame(size=0.05)
vis.add_geometry(axis)  


# # Optional grid overlay
grid = create_ground_grid_xy(rows= 12, cols=12 )
vis.add_geometry(grid)


pcd = o3.geometry.PointCloud()
pcd.points = o3.utility.Vector3dVector(np.zeros((1,3)))  # placeholder
vis.add_geometry(pcd)

frame_counter =0

# Optional view setup
vis.poll_events()
vis.update_renderer()

# perform correction 
sample_flat_surface = np.zeros((8,8,3), dtype=np.float64)

# endregion

# region:  Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors, SensorsDisplay() as lcd:
    while timer.check():
        currentTime = timer.get_current_time()
        sensors.read_outputs()

        TOFSensor = sensors.TOFDistance
        NumberSquare = np.flip(sensors.TOFNumberOfTargets.reshape(8,8), axis=0)
        ToFMeasurements = np.flip((TOFSensor * sensors.TOFNumberOfTargets).reshape(8,8), axis=0)

        # Compute 3D coordinates

        for i in range(8):
            for j in range(8):

                # Value given is distance (X value) and we need to recover y and z elements
                X = ToFMeasurements[i][j]  # Assume this is the X component

                # Get direction vector from angles
                dir_x = np.cos(-deltaAngle[i]) * np.sin(np.pi/2 - deltaAngle[j])
                dir_y = np.cos(-deltaAngle[i]) * np.cos(np.pi/2 - deltaAngle[j])
                dir_z = np.sin(-deltaAngle[i])

                # Recover magnitude of the full 3D distance
                if abs(dir_x) > 1e-6:  # Prevent divide by zero
                    P = X / dir_x
                else:
                    P = 0.0  # Or skip this point

                # Compute full 3D vector
                TOFMeas3D[i][j][0] = X 
                TOFMeas3D[i][j][1] = P * dir_y 
                # Add offset from floor to vertical location of sensor 
                TOFMeas3D[i][j][2] = P * dir_z +0.045 

                # We assume you cannot see below the floor 
                if TOFMeas3D[i][j][2] < 0:
                    TOFMeas3D[i][j][2] = 0   


        
        # Flatten and validate
        points = TOFMeas3D.reshape(-1, 3)
        valid = np.isfinite(points).all(axis=1)
        points = points[valid]
        
        # Step 1: Compute Euclidean distance from origin (0, 0, 0)
        distances = points[:, 0] 

        # Step 2: Normalize distances to [0, 1]
        dist_min = 0.1
        dist_max = 0.3
        dist_norm = np.clip((distances - dist_min) / (dist_max - dist_min + 1e-8), 0.0, 1.0)
        colormap = plt.get_cmap("viridis")  # Can also try "plasma", "jet", etc.viridis
        colors = colormap(dist_norm)[:, :3]  # Ignore alpha channel

        # Update Open3D point cloud
        pcd.points = o3.utility.Vector3dVector(points*0.2)
        pcd.colors = o3.utility.Vector3dVector(colors)
        render_option = vis.get_render_option()
        render_option.point_size = 40.0  # Adjust the size as needed

        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()

        timer.sleep()

vis.destroy_window()
# endregion





