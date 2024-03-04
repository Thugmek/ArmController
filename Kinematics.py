import math
import Duet
import sys
import numpy as np

import serial
ser = serial.Serial("/dev/ttyACM0",115200)

def rad_to_deg(rad):
    return (rad/math.pi)*180

def deg_to_rad(deg):
    return (deg/180)*math.pi


def find_intersection(A, v1):
    # Constants
    B = np.array([0, 0, 0])
    v0 = np.array([0, 0, 1])

    # Calculate normal to p0 (use cross product of AB and v0)
    AB = A - B
    normal_p0 = np.cross(AB, v0)

    # Normal to p1 is v1 itself
    normal_p1 = v1

    # Direction vector of the intersection line is the cross product of the normals to p0 and p1
    direction = np.cross(normal_p0, normal_p1)

    # Normalize direction vector
    direction = direction / np.linalg.norm(direction)

    # Since the line must pass through A, we use A as the point on the line
    point_on_line = A

    return point_on_line, direction

class Kinematics():
    def __init__(self):
        self.arm_length = 300
        self.joint2_limits = (deg_to_rad(0),deg_to_rad(150), 800)
        self.joint1_limits = (deg_to_rad(5), deg_to_rad(180), 800)
        self.azimuth_limits = (deg_to_rad(-90), deg_to_rad(90), 3000)

        self.position = [0,300,300]
        self.angles = [0,90,90]

    def prismasolve(self, x, y, z):
        if y == 0:
            y = sys.float_info.epsilon
        azimuth = math.atan(x/y)
        radius = math.sqrt(x*x + y*y)
        if radius == 0:
            radius = sys.float_info.epsilon
        length = math.sqrt(x*x + y*y + z*z)
        if length > 2*self.arm_length:
            raise Exception(f"Point is too far - {length:.2f} mm. Max distance: {2*self.arm_length%.2} mm")
        zenith = math.atan(z/radius)

        joint1 = 2*math.asin((length/2)/self.arm_length)
        joint2 = math.acos((length/2)/self.arm_length) + zenith

        # print(f"azimuth: {rad_to_deg(azimuth)}\n"
        #       f"radius: {radius}\n"
        #       f"length: {length}\n"
        #       f"zenith: {rad_to_deg(zenith)}\n"
        #       f"joint1: {rad_to_deg(joint1)}\n"
        #       f"joint2: {rad_to_deg(joint2)}\n")

        if joint1 < self.joint1_limits[0] or joint1 > self.joint1_limits[1]:
            raise Exception(f"Joint1 ({rad_to_deg(joint1):.2f}) outside limit ({rad_to_deg(self.joint1_limits[0])},{rad_to_deg(self.joint1_limits[1])})")
        if joint2 < self.joint2_limits[0] or joint2 > self.joint2_limits[1]:
            raise Exception(f"Joint2 ({rad_to_deg(joint2):.2f}) outside limit ({rad_to_deg(self.joint2_limits[0])},{rad_to_deg(self.joint2_limits[1])})")
        if azimuth < self.azimuth_limits[0] or azimuth > self.azimuth_limits[1]:
            raise Exception(f"Azimuth ({rad_to_deg(azimuth):.2f}) outside limit ({rad_to_deg(self.azimuth_limits[0])},{rad_to_deg(self.azimuth_limits[1])})")

        return rad_to_deg(azimuth), rad_to_deg(joint1), rad_to_deg(joint2)

    def set_position(self,x,y,z,calculate_fr=False):
        angles = self.prismasolve(x,y,z)

        if calculate_fr:
            d1 = abs(angles[0] - self.angles[0])
            d2 = abs(angles[1] - self.angles[1])
            d3 = abs(angles[2] - self.angles[2])

            d = math.sqrt(d1*d1 + d2*d2 + d3*d3)

            fr1 = self.azimuth_limits[2] * d / (d1 if d1 != 0 else sys.float_info.epsilon)
            fr2 = self.joint1_limits[2] * d / (d2 if d2 != 0 else sys.float_info.epsilon)
            fr3 = self.joint2_limits[2] * d / (d3 if d2 != 0 else sys.float_info.epsilon)

            fr = min(fr1, fr2, fr3)
        else:
            fr = 500


        # Duet.set_angles(angles[0],angles[1],angles[2])
        #with open("move.g","a") as f:
        #    f.write(f"G0 X{angles[1]} Y{angles[2]} Z{angles[0]} F{fr}\n")
        ser.write(f'G0 X{angles[1]} Y{angles[2]} Z{angles[0]} F{fr}\n'.encode())
        self.position = (x,y,z)
        self.angles = angles

    def linear_move(self, x, y, z, segment=5):
        #origin of move
        ox = self.position[0]
        oy = self.position[1]
        oz = self.position[2]
        #delta vector
        dx = x - ox
        dy = y - oy
        dz = z - oz
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        segments = math.ceil(length/segment)
        for i in range(segments):
            a = (i+1)/segments

            #end of current step
            cx = ox + dx * a
            cy = oy + dy * a
            cz = oz + dz * a

            self.set_position(cx, cy, cz, True)
