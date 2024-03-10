import numpy as np
import sys

l1 = 300
l2 = 300

pointC = (0,300,300)

lAC = np.linalg.norm(pointC)

angle1a = np.arcsin(pointC[2]/lAC)
x = pointC[0] if pointC[0] != 0 else sys.float_info.epsilon
angle0 = np.arctan(pointC[1]/x)

a = l2
b = lAC
c = l1
alpha = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
beta = np.arccos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
gamma = np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

print(f"alpha: {alpha}, angle1a: {angle1a}")
print(f"")

angle2 = beta
angle1 = alpha+angle1a

print(np.degrees((angle0,angle1,angle2)))