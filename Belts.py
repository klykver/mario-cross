class Belt:
    def __init__(self, x1, y1, x2, y2, direction=1):
        self.x1, self.y1 = x1, y1  # Start coords
        self.x2, self.y2 = x2, y2  # End coords
        self.direction = direction  # 1 right, -1 left