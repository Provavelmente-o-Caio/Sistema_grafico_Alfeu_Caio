class Window:
    def __init__(self, xmin=-10, ymin=-10, xmax=10, ymax=10):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    # Pan the window
    def pan(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy

    # Zoom the window (centered zoom)
    def zoom(self, factor):
        # Calculate center point
        xcenter = (self.xmin + self.xmax) / 2
        ycenter = (self.ymin + self.ymax) / 2

        # Calculate new width and height
        new_width = self.width() * factor
        new_height = self.height() * factor

        # Set new boundaries
        self.xmin = xcenter - new_width / 2
        self.xmax = xcenter + new_width / 2
        self.ymin = ycenter - new_height / 2
        self.ymax = ycenter + new_height / 2