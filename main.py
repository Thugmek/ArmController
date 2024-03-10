import sys

from Kinematics import Kinematics
import numpy as np

with open("move.g", "w") as f:
    f.write(f";precalculated movement file\n")

k = Kinematics()

# k.set_position(0,300,300)
# k.linear_move(0, 300, -100, 1)
# k.linear_move(0, 10, 500, 1)
# k.linear_move(300, 10, 500, 1)
# k.linear_move(300, 10, 500, 1)
# k.linear_move(0, 300, 300, 1)

res = np.degrees(k.solve((100,0,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((100,0,400),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((400,0,400),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((400,0,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((100,0,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

#---------------------------------

res = np.degrees(k.solve((100,300,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((100,300,400),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((400,300,400),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((400,300,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

res = np.degrees(k.solve((100,300,100),np.radians(0),np.radians(-0)))
print(f"G0 X{res[0]:.2f} Y{res[1]:.2f} Z{res[2]:.2f} A{res[3]:.2f} B{res[4]:.2f}")

#Duet.get_state()

