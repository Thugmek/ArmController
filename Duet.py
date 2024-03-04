import time

import requests

SERVER = "http://192.168.20.30"
GCODE_ENDPOINT = f"{SERVER}/rr_gcode?gcode="
STATE_ENDPOINT = f"{SERVER}/rr_model?flags=d99fno"

def set_angles(azimuth, joint1, joint2):
    #print(f"{GCODE_ENDPOINT}G0 X{joint1} Y{joint2} Z{azimuth} F500")
    requests.get(f"{GCODE_ENDPOINT}G0 X{joint1} Y{joint2} Z{azimuth} F500")
    time.sleep(0.05)

def get_state():
    res = requests.get(STATE_ENDPOINT)
    state = res.json()["result"]
    print(res.json()["result"])
