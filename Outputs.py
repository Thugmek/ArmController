import numpy as np


class DummyOutput():
    def moveTo(self, angles, feed_rate=None):
        pass


class FileOutput(DummyOutput):
    def __init__(self, path):
        self.path = path
        with open(self.path, "w") as f:
            f.write("")
            f.close()

    def moveTo(self, angles, feed_rate=None):
        angles = np.degrees(angles)
        fr = f" F{feed_rate}" if feed_rate else ""
        gcode = f"G0 X{angles[0]:.2f} Y{angles[1]:.2f} Z{angles[2]:.2f} A{angles[3]:.2f} B{angles[4]:.2f}{fr}\n"
        with open(self.path, "a") as f:
            f.write(gcode)
            f.close()