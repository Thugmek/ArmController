from ursina import *
from ursina.shaders import *
import math
from flask import Flask, request, make_response
from threading import Thread
import os
import numpy as np


class Joint(Entity):
    def __init__(self, length, axis_dir, axis_rot, prev_joint=None, **kwargs):
        super().__init__(**kwargs)
        self.length = length
        self.axis_dir = [0, 0, 0]
        self.axis_dir[axis_dir] = 1
        self.axis_rot = axis_rot
        self.prev_joint = prev_joint
        self.angle_offset = 0
        self.reversed = True
        self.current_angle = 0
        self.target = 0
        self.speed = 0
        self.busy = False

        if self.prev_joint:
            self.parent = self.prev_joint.end

        joint_rot = (0, 0, 90)
        joint_scale = (0.3, 0.5, 0.3)
        if self.axis_rot == 1:
            joint_rot = (0, 0, 0)
            joint_scale = (0.6, 0.1, 0.6)
        if self.axis_rot == 2:
            joint_rot = (90, 0, 0)
        self.joint0 = Entity(model=Cylinder(16, start=-0.5), scale=joint_scale, rotation=joint_rot,
                             parent=self, color=color.orange)

        beam_scale = np.maximum((0.3, 0.3, 0.3), np.multiply(self.axis_dir, length))
        self.beam0 = Entity(model='cube', parent=self, position=np.multiply(self.axis_dir, length / 2),
                            scale=beam_scale, shader=basic_lighting_shader, color=color.gray)

        self.end = Entity(position=np.multiply(self.axis_dir, length),
                          parent=self)


    def set_angle(self, angle, set_target=True):
        self.current_angle = angle
        if set_target:
            self.target = angle
        rot = [0, 0, 0]
        rot[self.axis_rot] = self.angle_offset + angle * (-1 if self.reversed else 1)
        self.rotation = rot

    def move_to(self, angle, speed):
        self.target = angle
        self.speed = speed

    def update(self):
        if self.current_angle != self.target:
            self.busy = True
            err = self.target - self.current_angle
            self.set_angle(self.current_angle + (min(err, self.speed * time.dt) if err > 0 else max(err, -self.speed * time.dt)),False)
        else:
            self.busy = False

class Robot(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.queue = []
        self.busy = False
        self.trajectory = []
        self.trajectory_entity = Entity(color=color.blue)
        self.last_speed = 90

        self.scale = 0.008

        self.l0 = 100
        self.l1 = 386
        self.l2 = 376.3
        self.l3 = 68
        self.l4 = 30
        self.l5 = 8

        self.joints:[Joint] = []
        j0 = Joint(self.l0*self.scale, 1, 1)
        self.joints.append(j0)

        j1 = Joint(self.l1*self.scale, 1, 0, j0)
        j1.angle_offset = 90
        j1.set_angle(90)
        self.joints.append(j1)

        j2 = Joint(self.l2*self.scale, 1, 0, j1)
        j2.angle_offset = 180
        j2.set_angle(90)
        self.joints.append(j2)

        j3 = Joint(self.l3*self.scale, 1, 0, j2)
        self.joints.append(j3)

        j4 = Joint(self.l4*self.scale, 1, 2, j3)
        self.joints.append(j4)

        j5 = Joint(self.l5*self.scale, 1, 1, j4)
        self.joints.append(j5)

    def clear_trajectory(self):
        self.trajectory = []
        self.trajectory_entity.model = None

    def update(self):
        busy = False
        for j in self.joints:
            if j.busy:
                busy = True
                break
        self.busy = busy

        if busy:
            effector_end = self.joints[-1].end.world_position
            if len(self.trajectory) == 0 or np.linalg.norm(np.subtract(effector_end,self.trajectory[-1])) > 0.1:
                self.trajectory.append(effector_end)
                if len(self.trajectory) > 1:
                    self.trajectory_entity.model=Mesh(vertices=self.trajectory, mode='line', static=False, render_points_in_3d=True, thickness=5)

        if not busy and len(self.queue) > 0:
            data = self.queue[0]
            self.queue = self.queue[1:]

            num_joints = len(self.joints)

            d = [0] * num_joints
            targets = [0] * num_joints

            for t in range(num_joints):
                if f"angle{t}" in data:
                    targets[t] = data[f"angle{t}"]
                else:
                    targets[t] = self.joints[t].current_angle
                d[t] = np.abs(targets[t] - self.joints[t].current_angle)

            dmax = max(d)

            if "speed" in data:
                top_speed = data["speed"]
                self.last_speed = top_speed
            else:
                top_speed = self.last_speed

            for t in range(num_joints):
                speed = d[t] / dmax * top_speed
                self.joints[t].move_to(targets[t], speed)





