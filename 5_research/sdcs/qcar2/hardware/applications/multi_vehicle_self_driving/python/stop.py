import paramiko
import argparse


# Configuration
parser = argparse.ArgumentParser(description="Stop all applications on QCars.")
parser.add_argument('-ip', '--qcar_ips', type=str, required=True, help="IP addresses of QCars")
args = parser.parse_args()
QCAR_IPS = args.qcar_ips.split(",")  # Comma-separated list of IPs
USERNAME = "nvidia"
PASSWORD = "nvidia"

def create_ssh(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=USERNAME, password=PASSWORD)
    return ssh

for ip in QCAR_IPS:
    ssh = create_ssh(ip)
    ssh.exec_command("pkill -2 python ; pkill -15 python")
    ssh.close()