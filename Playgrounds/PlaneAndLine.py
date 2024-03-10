import math
import numpy as np
from ursina import *
from ursina.shaders import *


def find_intersection(A, v1):
    B = np.array([0, 0, 0])
    v0 = np.array([0, 1, 0])
    AB = A - B
    normal_p0 = np.cross(AB, v0)
    normal_p1 = v1
    direction = np.cross(normal_p0, normal_p1)
    direction = direction / np.linalg.norm(direction)
    point_on_line = A
    return point_on_line, direction


def angle_between_vectors(v1, v2):
    # Calculate the dot product of v1 and v2
    dot_product = np.dot(v1, v2)

    # Calculate the magnitudes of v1 and v2
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    # Calculate the cosine of the angle between v1 and v2
    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

    # Calculate the angle in radians
    angle_radians = np.arccos(cos_theta)

    # Convert the angle to degrees
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees

LENGTH = 0.3
LENGTH2 = 0.3
azimuth = math.pi * 0.25
zenith = math.pi * -0.25

pointA = (1, 2, 0)

y = LENGTH * math.sin(zenith)
xz = LENGTH * math.cos(zenith)
x = xz * math.sin(azimuth)
z = xz * math.cos(azimuth)
vecAB = (x, y, z)
pointB = np.subtract(pointA, vecAB)

print(f"PointB: {pointB}, vecAB: {vecAB}")
intersection = find_intersection(pointB, vecAB)
print(intersection)

normal_vector = np.cross(intersection[1], (0, 1, 0))
vecBC = np.cross(normal_vector, intersection[1])
vecBC = vecBC / np.linalg.norm(vecBC) * LENGTH2
pointC1 = np.add(pointB, vecBC)
pointC2 = np.subtract(pointB, vecBC)

ursina_app = Ursina(borderless=False, title="Plane and Line")
EditorCamera(rotation=(30, -120, 0))
Entity(model='plane', scale=10, color=color.gray, shader=basic_lighting_shader)

Entity(model=Mesh(vertices=[(0, 0, 0), (1, 0, 0)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.red)
Entity(model=Mesh(vertices=[(0, 0, 0), (0, 1, 0)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.green)
Entity(model=Mesh(vertices=[(0, 0, 0), (0, 0, 1)], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.blue)

Entity(model=Mesh(vertices=[pointA], mode='point', static=False, render_points_in_3d=False, thickness=10),
       color=color.red)
Entity(model=Mesh(vertices=[pointB], mode='point', static=False, render_points_in_3d=False, thickness=10),
       color=color.green)
Entity(model=Mesh(vertices=[pointC1], mode='point', static=False, render_points_in_3d=False, thickness=10),
       color=color.blue)
Entity(model=Mesh(vertices=[pointC2], mode='point', static=False, render_points_in_3d=False, thickness=10),
       color=color.pink)

Entity(model=Mesh(vertices=[pointA, pointB], mode='line', static=False, render_points_in_3d=True, thickness=5),
       color=color.red)
Entity(model=Mesh(vertices=[intersection[0], np.add(intersection[0], intersection[1])], mode='line', static=False,
                  render_points_in_3d=True, thickness=5),
       color=color.blue)

ursina_app.run()
