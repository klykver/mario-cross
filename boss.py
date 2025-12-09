import pyxel


class Boss:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.side = "left"  # "left" = Mario, "right" = Luigi

        # match the position of the boss's door
        self.left_x = 486
        self.left_y = 145

        self.right_x = 7
        self.right_y = 233

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        if value not in ("left", "right"):
            raise ValueError("Side must be 'left' or 'right'")
        self.__side = value

    # the boss after a failure
    def appear(self, side: str):
        self.active = True
        self.side = side
        self.timer = 60  # 2 seconds at 30 FPS

    # is a timer that counts down to 0. Time the boss is visible on screen
    def update(self):
        if not self.active:
            return
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self):
        if not self.active:
            return
        # draw boss sprites
        if self.side == "right":
            pyxel.blt(self.left_x, self.left_y, 2, 80, 168, 23, 33, 0)
        if self.side == "left":
            pyxel.blt(self.right_x, self.right_y, 2, 81, 128, 20, 33, 0)
