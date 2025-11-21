from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(446, 326, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(313, 281, 3)
        pyxel.run(self.update, self.draw)  #must be last line in init

    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(313, 253, 0, 0, 72, 49, 29)
        pyxel.blt(310, 310, 0, 58, 71, 37, 29)
        pyxel.blt(180,282,1,0,16,95,26)
        pyxel.blt(180, 258, 1, 0, 16, 95, 26)
        pyxel.blt(180, 234, 1, 0, 16, 95, 26)
        pyxel.blt(180, 210, 1, 0, 16, 95, 26)
        pyxel.blt(180, 186, 1, 0, 16, 95, 26)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
