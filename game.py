from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(200, 213, 3)
        pyxel.run(self.update, self.draw)  #must be last line in init

    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(200, 178, 0, 0, 72, 41, 29)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
