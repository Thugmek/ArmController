from Kinematics import Kinematics
import Duet

with open("move.g", "w") as f:
    f.write(f";precalculated movement file\n")

k = Kinematics()

k.set_position(0,300,300)
k.linear_move(0, 300, -100, 1)
k.linear_move(0, 10, 500, 1)
k.linear_move(300, 10, 500, 1)
k.linear_move(300, 10, 500, 1)
k.linear_move(0, 300, 300, 1)


#Duet.get_state()

