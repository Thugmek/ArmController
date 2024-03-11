import sys

from Kinematics import Kinematics
from Outputs import *

with open("move.g", "w") as f:
    f.write(f";precalculated movement file\n")

k = Kinematics(FileOutput("output.g"))

for i in range(0,60,5):
    k.set_position((300, 0, 300), np.radians(i), 0)
for i in range(60,-60,-5):
    k.set_position((300, 0, 300), np.radians(i), 0)
for i in range(-60, 0, 5):
    k.set_position((300, 0, 300), np.radians(i), 0)

# k.linear_move(0, 300, -100, 1)
# k.linear_move(0, 10, 500, 1)
# k.linear_move(300, 10, 500, 1)
# k.linear_move(300, 10, 500, 1)
# k.linear_move(0, 300, 300, 1)

#Duet.get_state()

