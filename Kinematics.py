import math
import os

import Duet
import sys
import numpy as np

import serial

# ser = serial.Serial("/dev/ttyACM0", 115200)


def rad_to_deg(rad):
    return (rad / math.pi) * 180


def deg_to_rad(deg):
    return (deg / 180) * math.pi


def find_intersection(A, v1):
    B = np.array([0, 0, 0])
    v0 = np.array([0, 0, 1])
    AB = A - B
    normal_p0 = np.cross(AB, v0)
    normal_p1 = v1
    direction = np.cross(normal_p0, normal_p1)
    direction = direction / np.linalg.norm(direction)
    point_on_line = A
    return point_on_line, direction

def rotation_angle( v1, v2, v3):
    # Normalize v1 and v3
    v1_normalized = v1 / np.linalg.norm(v1)
    v3_normalized = v3 / np.linalg.norm(v3)

    # Calculate the cosine of the angle between v1 and v3 using the dot product
    cos_theta = np.dot(v1_normalized, v3_normalized)

    # Calculate the angle in radians
    angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Clip for numerical stability

    # Determine the rotation direction
    cross_product = np.cross(v1_normalized, v3_normalized)
    direction = np.dot(cross_product, v2)

    # Adjust the angle based on the direction
    if direction < 0:
        return -angle_radians
    else:
        return angle_radians


class Kinematics():
    def __init__(self):
        self.l0 = 213
        self.l1 = 386
        self.l2 = 376.3
        self.l3 = 68
        self.l4 = 38
        self.joint2_limits = (deg_to_rad(0), deg_to_rad(150), 800)
        self.joint1_limits = (deg_to_rad(5), deg_to_rad(180), 800)
        self.azimuth_limits = (deg_to_rad(-90), deg_to_rad(90), 3000)

        self.position = [0, 300, 300]
        self.angles = [0, 90, 90]

    def solve(self, pointE, azimuth, zenith):
        z = self.l4 * math.sin(zenith)
        xy = self.l4 * math.cos(zenith)
        x = xy * math.cos(azimuth)
        y = xy * math.sin(azimuth)
        vecDE = (x, y, z)
        pointD = np.subtract(pointE, vecDE)

        #print(f"pointE: {pointE}, pointD: {pointD}")

        normal_p0 = np.cross(pointD, [0, 0, 1])
        rot4vec = np.cross(normal_p0, vecDE)
        rot4vec = rot4vec / np.linalg.norm(rot4vec)

        #print(f"normal_p0: {normal_p0}, rot4vec: {rot4vec}")

        #rot4vec angle to [0,0,1]
        angle3a = np.arccos(np.dot(rot4vec, [0,0,1]))
        #print(f"angle3a: {angle3a}")

        vecDC = np.cross(normal_p0, rot4vec)
        vecDC = vecDC / np.linalg.norm(vecDC) * self.l3
        pointC1 = np.add(pointD, vecDC)
        pointC2 = np.subtract(pointD, vecDC)

        # TODO - some distinction needed
        if(True):
            pointC = pointC1
        else:
            pointC = pointC2

        lAC = np.linalg.norm(pointC)

        angle1a = np.arcsin(pointC[2]/lAC)
        x = pointC[0] if pointC[0] != 0 else sys.float_info.epsilon
        angle0 = np.arctan(pointC[1]/x)

        a = self.l2
        b = lAC
        c = self.l1
        alpha = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        beta = np.arccos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
        gamma = np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

        angle2 = beta
        angle1 = alpha+angle1a
        angle3 = gamma-angle1a+zenith
        #print(f"Point C: {pointC}")
        return angle0, angle1, angle2, angle3, azimuth

    # def prismasolve(self, x, y, z):
    #     if y == 0:
    #         y = sys.float_info.epsilon
    #     azimuth = math.atan(x / y)
    #     radius = math.sqrt(x * x + y * y)
    #     if radius == 0:
    #         radius = sys.float_info.epsilon
    #     length = math.sqrt(x * x + y * y + z * z)
    #     if length > 2 * self.arm_length:
    #         raise Exception(f"Point is too far - {length:.2f} mm. Max distance: {2 * self.arm_length % .2} mm")
    #     zenith = math.atan(z / radius)
    #
    #     joint1 = 2 * math.asin((length / 2) / self.arm_length)
    #     joint2 = math.acos((length / 2) / self.arm_length) + zenith
    #
    #     if joint1 < self.joint1_limits[0] or joint1 > self.joint1_limits[1]:
    #         raise Exception(
    #             f"Joint1 ({rad_to_deg(joint1):.2f}) outside limit ({rad_to_deg(self.joint1_limits[0])},{rad_to_deg(self.joint1_limits[1])})")
    #     if joint2 < self.joint2_limits[0] or joint2 > self.joint2_limits[1]:
    #         raise Exception(
    #             f"Joint2 ({rad_to_deg(joint2):.2f}) outside limit ({rad_to_deg(self.joint2_limits[0])},{rad_to_deg(self.joint2_limits[1])})")
    #     if azimuth < self.azimuth_limits[0] or azimuth > self.azimuth_limits[1]:
    #         raise Exception(
    #             f"Azimuth ({rad_to_deg(azimuth):.2f}) outside limit ({rad_to_deg(self.azimuth_limits[0])},{rad_to_deg(self.azimuth_limits[1])})")
    #
    #     return rad_to_deg(azimuth), rad_to_deg(joint1), rad_to_deg(joint2)

    def set_position(self, x, y, z, calculate_fr=False):
        angles = self.prismasolve(x, y, z)

        if calculate_fr:
            d1 = abs(angles[0] - self.angles[0])
            d2 = abs(angles[1] - self.angles[1])
            d3 = abs(angles[2] - self.angles[2])

            d = math.sqrt(d1 * d1 + d2 * d2 + d3 * d3)

            fr1 = self.azimuth_limits[2] * d / (d1 if d1 != 0 else sys.float_info.epsilon)
            fr2 = self.joint1_limits[2] * d / (d2 if d2 != 0 else sys.float_info.epsilon)
            fr3 = self.joint2_limits[2] * d / (d3 if d2 != 0 else sys.float_info.epsilon)

            fr = min(fr1, fr2, fr3)
        else:
            fr = 500

        # Duet.set_angles(angles[0],angles[1],angles[2])
        # with open("move.g","a") as f:
        #    f.write(f"G0 X{angles[1]} Y{angles[2]} Z{angles[0]} F{fr}\n")
        ser.write(f'G0 X{angles[1]} Y{angles[2]} Z{angles[0]} F{fr}\n'.encode())
        self.position = (x, y, z)
        self.angles = angles

    def linear_move(self, x, y, z, segment=5):
        # origin of move
        ox = self.position[0]
        oy = self.position[1]
        oz = self.position[2]
        # delta vector
        dx = x - ox
        dy = y - oy
        dz = z - oz
        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        segments = math.ceil(length / segment)
        for i in range(segments):
            a = (i + 1) / segments

            # end of current step
            cx = ox + dx * a
            cy = oy + dy * a
            cz = oz + dz * a

            self.set_position(cx, cy, cz, True)
