"""nginx switcher"""
import subprocess
import os
import time

NGINX_PATH = os.path.expanduser("~/nginx.conf")

ENV_PORT = str(int(os.environ.get("PORT", 3030)))

PREV_CONFIG = (
    open("./nginx_prev.conf", "r", encoding="utf-8")
    .read()
    .replace("$ENV_PORT", ENV_PORT)
)
NEXT_CONFIG = (
    open("./nginx_next.conf", "r", encoding="utf-8")
    .read()
    .replace("$ENV_PORT", ENV_PORT)
)


def check_status():
    """check status"""
    return os.path.isfile("./tor_server/torrc.in")


def check_nginx_running():
    """check nginx running"""
    try:
        subprocess.run(["pgrep", "nginx"], check=True)
        is_running = True
    except subprocess.CalledProcessError:
        is_running = False
    return is_running


def boot_nginx(data):
    """boot nginx"""
    with open(NGINX_PATH, "w", encoding="utf-8") as conf:
        conf.write(data)
    if check_nginx_running():
        with subprocess.Popen(["nginx", "-s", "reload", "-c", NGINX_PATH]) as process:
            process.wait()
    else:
        with subprocess.Popen(["nginx", "-c", NGINX_PATH]) as process:
            process.wait()


boot_nginx(PREV_CONFIG)

while True:
    if check_status():
        boot_nginx(NEXT_CONFIG)
        print("booted nginx")
        break
    time.sleep(0.3)
