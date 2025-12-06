import pyxel


class Boss:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.side = "left"  # "left" = Mario, "right" = Luigi

        # координати дверей (з твого рисунку)
        self.left_x = 486
        self.left_y = 145

        self.right_x = 7
        self.right_y = 233

    def appear(self, side: str):
        self.active = True
        self.side = side
        self.timer = 60  # 2 seconds at 30 FPS

    def update(self):
        if not self.active:
            return
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self):
        if not self.active:
            return
        # draw boss sprite (use appropriate sprite coords from your sheet)
        if self.side == "right":
            pyxel.blt(self.left_x, self.left_y, 2, 80, 168, 23, 33, 0)
        if self.side == "left":
            pyxel.blt(self.right_x, self.right_y, 2, 81, 128, 20, 33, 0)
