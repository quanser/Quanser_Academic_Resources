import paramiko
import argparse
from scp import SCPClient
import subprocess
import os
import glob
import time

parser = argparse.ArgumentParser(description="Run a demo script on a remote server.")
parser.add_argument('-ip', '--qcar_ips', type=str, required=True, help="IP addresses of QCars")
parser.add_argument('-rp','--remote_path',type=str,required=True, help="Remote path on QCar")
parser.add_argument('-ipp','--probing_ip', type=str, required=True, help="IP addresses of QCar to probe")
parser.add_argument('-ipl','--local_ip', type=str, required=True,help="IP addresses of local machine")
parser.add_argument('-w','--width', default=320, help="width of to image to be displayed in the observer")
parser.add_argument('-ht','--height', default=200, help="height of to image to be displayed in the observer")
args = parser.parse_args()

QCAR_IPS = args.qcar_ips.split(",")  # Comma-separated list of IPs
LOCAL_IP = args.local_ip
PROBING_IP = args.probing_ip
WIDTH = args.width
HEIGHT = args.height
REMOTE_PATH = args.remote_path
USERNAME = "nvidia"
PASSWORD = "nvidia"
LOCAL_SCRIPTS_PATH = "../qcar"
LOCAL_OBSERVER_PATH = "python/observer.py"
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPTS_PATH = os.path.normpath(os.path.join(CURRENT_DIR,LOCAL_SCRIPTS_PATH))

# --- Helper to create SSH + SCP connections ---
def create_ssh_and_scp(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=USERNAME, password=PASSWORD)
    scp = SCPClient(ssh.get_transport())
    return ssh, scp

for ip in QCAR_IPS:
    print(f"\n Starting QCar: {ip}")

    # Upload Python scripts
    ssh, scp = create_ssh_and_scp(ip)

    py_files = glob.glob(os.path.normpath(os.path.join(SCRIPTS_PATH, "*.py")))
    for file in py_files:
        scp.put(file, REMOTE_PATH)
    print(f"[{ip}] Uploaded QCar scripts.")

    # Set PROBING flag
    is_probing = (ip == PROBING_IP)
    probing_flag = "True" if is_probing else "False"

    # Start observer.py locally if this is the probing QCar
    if is_probing:
        print(f"[{ip}] Starting observer.py locally (probing mode).")
        subprocess.Popen(["python", LOCAL_OBSERVER_PATH])

    # Start vehicle_control.py remotely
    cmd_vehicle = f"cd {REMOTE_PATH} && python vehicle_control.py &"
    ssh.exec_command(cmd_vehicle)
    print(f"[{ip}] Started vehicle_control.py.")

    time.sleep(1) 

    # Start yolo_server.py remotely with probing and other args
    cmd_yolo = (
        f"cd {REMOTE_PATH} && "
        f"python yolo_server.py -p {probing_flag} -i {LOCAL_IP} -w {WIDTH} -ht {HEIGHT} &"
    )
    ssh.exec_command(cmd_yolo)
    print(f"[{ip}] Started yolo_server.py.")

    ssh.close()
    scp.close()

    time.sleep(3) 

input("\n All QCars started, press Enter to exit...")  # Wait for user input before exiting
