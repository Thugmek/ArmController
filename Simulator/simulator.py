from ursina import *
from ursina.shaders import *
import math
from flask import Flask, request, make_response
from threading import Thread
import os
import numpy as np

ursina_app = Ursina()
flask_app = Flask(__name__)
EditorCamera(rotation=(30,-120,0))
Entity(model='plane', scale=10, color=color.gray,
shader=basic_lighting_shader)

pivot1 = Entity(y=0.3)
joint1 = Entity(model=Cylinder(16, start=-0.5), scale=(0.3,0.5,0.3),rotation=(0,0,90),parent=pivot1,color=color.orange)
beam1 = Entity(model='cube', parent=pivot1 ,y=1, scale=(0.3,2,0.3), shader=basic_lighting_shader, color=color.gray)

pivot2 = Entity(y=2, parent=pivot1,rotation=(90,0,0))
joint2 = Entity(model=Cylinder(16, start=-0.5), scale=(0.3,0.5,0.3),rotation=(0,0,90),parent=pivot2,color=color.orange)
beam2 = Entity(model='cube', parent=pivot2 ,y=1, scale=(0.3,2,0.3), shader=basic_lighting_shader, color=color.gray)

pivot3 = Entity(y=2, parent=pivot2)
joint3 = Entity(model=Cylinder(16, start=-0.5), scale=(0.3,0.5,0.3),rotation=(0,0,90),parent=pivot3,color=color.orange)
beam3 = Entity(model='cube', parent=pivot3 ,y=0.25, scale=(0.3,0.5,0.3), shader=basic_lighting_shader, color=color.gray)

pivot4 = Entity(y=0.5, parent=pivot3)
joint4 = Entity(model=Cylinder(16, start=-0.5), scale=(0.3,0.5,0.3),rotation=(90,0,0),parent=pivot4,color=color.orange)
beam4 = Entity(model='cube', parent=pivot4 ,y=0.25, scale=(0.3,0.5,0.3), shader=basic_lighting_shader, color=color.gray)

target1 = 0
speed1 = 360
target2 = 90
speed2 = 360
target3 = 0
speed3 = 360
target4 = 0
speed4 = 360

def update():
    if pivot1.rotation_x != target1:
        err = target1-pivot1.rotation_x
        pivot1.rotation_x += min(err, speed1*time.dt) if err > 0 else max(err, -speed1*time.dt)

    if pivot2.rotation_x != target2:
        err = target2-pivot2.rotation_x
        pivot2.rotation_x += min(err, speed2*time.dt) if err > 0 else max(err, -speed2*time.dt)

    if pivot3.rotation_x != target3:
        err = target3-pivot3.rotation_x
        pivot3.rotation_x += min(err, speed3*time.dt) if err > 0 else max(err, -speed3*time.dt)

    if pivot4.rotation_z != target4:
        err = target4-pivot4.rotation_z
        pivot4.rotation_z += min(err, speed4*time.dt) if err > 0 else max(err, -speed4*time.dt)

@flask_app.route("/", methods=["POST"])
def move():
    try:
        data = request.json
    except Exception:
        return make_response("Malformed JSON body", 400)

    global target1, target2, target3, target4, speed1, speed2, speed3, speed4

    if "speed" not in data:
        return make_response("Speed field Required", 400)

    if "angle1" in data:
        target1 = data["angle1"]
    if "angle2" in data:
        target2 = data["angle2"]
    if "angle3" in data:
        target3 = data["angle3"]
    if "angle4" in data:
        target4 = data["angle4"]

    d1 = np.abs(target1 - pivot1.rotation_x)
    d2 = np.abs(target2 - pivot2.rotation_x)
    d3 = np.abs(target3 - pivot3.rotation_x)
    d4 = np.abs(target4 - pivot4.rotation_z)

    dmax = max(d1,d2,d3,d4)

    print(f"d1: {d1}, d2: {d2}, d3: {d3}, d4: {d4}, max: {dmax}")

    speed = data["speed"]
    speed1 = d1 / dmax * speed
    speed2 = d2 / dmax * speed
    speed3 = d3 / dmax * speed
    speed4 = d4 / dmax * speed

    return make_response("", 200)

flask_thread = Thread(target=flask_app.run)
flask_thread.start()

ursina_app.run()
