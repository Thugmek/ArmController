from ursina import *
from ursina.shaders import *
import math
from flask import Flask, request, make_response
from threading import Thread
import os
import numpy as np
from Robot import *

SCALE=0.005

ARM1LENGTH = 450
ARM2LENGTH = 400

ursina_app = Ursina(borderless=False, title="Arm Simulator")
flask_app = Flask(__name__)
EditorCamera(rotation=(30,-120,0))
Entity(model='plane', scale=10, color=color.gray, shader=basic_lighting_shader)

cursor = Entity(x=1,rotation=(0,0,0))
Entity(model=Mesh(vertices=[(0,0,0),(1,0,0)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.red, parent=cursor)
Entity(model=Mesh(vertices=[(0,0,0),(0,1,0)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.blue, parent=cursor)
Entity(model=Mesh(vertices=[(0,0,0),(0,0,1)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.green, parent=cursor)

robot = Robot()

@flask_app.route("/cursor", methods=["POST"])
def set_cursor():
    try:
        data = request.json
    except Exception:
        return make_response("Malformed JSON body", 400)

    if "x" in data:
        x = data["x"]
    else:
        return make_response("Field 'x' is missing", 400)
    if "y" in data:
        y = data["y"]
    else:
        return make_response("Field 'y' is missing", 400)
    if "z" in data:
        z = data["z"]
    else:
        return make_response("Field 'z' is missing", 400)
    if "azimuth" in data:
        azimuth = data["azimuth"]
    else:
        return make_response("Field 'azimuth' is missing", 400)
    if "zenith" in data:
        zenith = data["zenith"]
    else:
        return make_response("Field 'zenith' is missing", 400)

    cursor.position = (x,z,y)
    cursor.rotation = (zenith,azimuth,0)

    return make_response({
        "x": x,
        "y": y,
        "z": z,
        "azimuth": azimuth,
        "zenith": zenith
    }, 200)

@flask_app.route("/", methods=["POST"])
def move():
    try:
        data = request.json
    except Exception:
        return make_response("Malformed JSON body", 400)

    robot.queue.append(data)

    return make_response("", 200)

@flask_app.route("/gcode", methods=["POST"])
def gcode():
    data = request.data.decode().split('\n')
    for row in data:
        parts = row.split(' ')
        command = parts[0].strip()
        args = parts[1:]
        if command == "CLEAR":
            robot.clear_trajectory()
        elif command == "G0" or command == "G1":
            move = {}
            for arg in args:
                arg = arg.strip()
                type = arg[0]
                value = arg[1:]
                if type == "X":
                    move["angle0"] = float(value)
                if type == "Y":
                    move["angle1"] = float(value)
                if type == "Z":
                    move["angle2"] = float(value)
                if type == "A":
                    move["angle3"] = float(value)
                if type == "B":
                    move["angle4"] = float(value)
                if type == "C":
                    move["angle5"] = float(value)
                if type == "F":
                    move["speed"] = float(value)
            robot.queue.append(move)

    return make_response("", 200)

flask_thread = Thread(target=flask_app.run)
flask_thread.start()

ursina_app.run()
