from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(386, 356, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(283, 311, 3)
        pyxel.run(self.update, self.draw)  #must be last line in init

    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(283, 283, 0, 0, 72, 49, 29)
        pyxel.blt(280, 340, 0, 58, 71, 37, 29)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
