"""main"""
from typing import List
import subprocess
import time
import os

PREV_CONFIG = open("./nginx_prev.conf", "r", encoding="utf-8").read()
NEXT_CONFIG = open("./nginx_next.conf", "r", encoding="utf-8").read()

NGINX_PATH = os.path.expanduser("~/nginx.conf")

CMDS = [
    ["python3", "summon_sub.py", "--port", "3031"],
    ["python3", "summon_sub.py", "--port", "3032"],
    ["python3", "nginx_switcher.py"],
]

PROGS = []


def check_status():
    """check status"""
    return os.path.isfile("./tor_server/torrc.in")


def boot_nginx(data):
    """boot nginx"""
    with subprocess.Popen(["nginx", "-s", "reload", "-c", NGINX_PATH]) as prog:
        prog.wait()
    with open(NGINX_PATH, "w", encoding="utf-8") as conf:
        conf.write(data)


def boot_processes(commands):
    """boot process"""
    processes = []
    for command in commands:
        processes.append(subprocess.Popen(command))
    return processes


def kill_processes(processes: List[subprocess.Popen]):
    """kill processes"""
    for prog in processes:
        try:
            prog.kill()
        except Exception as error:  # pylint: disable=broad-exception-caught
            print(error)


def check_process_running(process_name):
    """check if process is running"""
    try:
        command = f"ps aux | grep '{process_name}' | grep -v grep"
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        output = result.stdout.lower()
        if process_name.lower() in output:
            return True
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {str(error)}")
    return False


while True:
    try:
        if not check_process_running("et_client_app.py"):
            if check_status():
                os.remove("./tor_server/torrc.in")
            kill_processes(PROGS)
            PROGS = boot_processes(CMDS)
            with subprocess.Popen(["python3", "et_client_app.py"]) as process:
                process.wait()

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {str(e)}")
    time.sleep(0.3)
