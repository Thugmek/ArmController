from Kinematics import find_intersection
import numpy as np


for i in range(-20,20):
    for j in range(-20,20):
        for k in range(-20,20):
            v1 = (0,0,1)
            v2 = (i,j,k)
            intersection = find_intersection(v2,(0,1,1))

            base = (v1,v2,np.cross(v1,v2))

            res = np.linalg.solve(base, intersection[1])

            if res[2] != 0:
                print(f"v2: {v2}, intersection: {intersection[1]}, res: {res}")