import numpy as np


def rotation_angle_with_direction(v1, v2, v3):
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
        angle_degrees = -np.degrees(angle_radians)
    else:
        angle_degrees = np.degrees(angle_radians)

    return angle_degrees


# Example vectors
v1 = np.array([1, 0, 0])
v2 = np.array([0, 0, 1])  # Rotation axis, perpendicular to v1
v3 = np.array([1, 0, 0.1])  # Result of rotating v1 around v2

# Calculate the rotation angle with direction
angle = rotation_angle_with_direction(v1, v2, v3)
print(f"Rotation angle: {angle} degrees")
