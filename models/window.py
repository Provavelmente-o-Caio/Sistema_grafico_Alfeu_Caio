import math


class Window:
    def __init__(self, xmin=-1, ymin=-1, xmax=1, ymax=1, rotation_angle=0):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.rotation_angle = rotation_angle

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    def center(self):
        return (self.xmax + self.xmin) / 2, (self.ymax + self.ymin) / 2

    # Pan the window
    def pan(self, dx, dy):
        # dx e dy estão no espaço da window, ou seja, em coordenadas normalizadas.
        rad = math.radians(self.rotation_angle)
        dx_rot = dx * math.cos(rad) + dy * math.sin(rad)
        dy_rot = -dx * math.sin(rad) + dy * math.cos(rad)

        self.xmin += dx_rot
        self.xmax += dx_rot
        self.ymin += dy_rot
        self.ymax += dy_rot

    # Zoom the window (centered zoom)
    def zoom(self, factor):
        # Calculate center point
        xcenter, ycenter = self.center()

        # Calculate new width and height
        new_width = self.width() * factor
        new_height = self.height() * factor

        # Set new boundaries
        self.xmin = xcenter - new_width / 2
        self.xmax = xcenter + new_width / 2
        self.ymin = ycenter - new_height / 2
        self.ymax = ycenter + new_height / 2

    def rotate(self, angle: float):
        self.rotation_angle += angle

    def move_to_center(self):
        cx, cy = self.center()
        self.pan(-cx, -cy)

    def normalize_to_scn(self, x, y):
        nx = 2 * (x - self.xmin) / self.width() - 1
        ny = 2 * (y - self.ymin) / self.height() - 1
        return nx, ny

    def denormalize_from_scn(self, nx, ny):
        x = (nx + 1) * self.width() / 2 + self.xmin
        y = (ny + 1) * self.height() / 2 + self.ymin
        return x, y
