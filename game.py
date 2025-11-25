
from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(446, 326, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(313, 268, 3)
        pyxel.run(self.update, self.draw)  #must be last line in init


    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(23, 171, 2, 0, 0, 255, 119)  # left side esta elevado a 13 cm del suelo
        pyxel.blt(268, 194, 2, 0, 118, 255, 119)#right side
        pyxel.blt(313, 257, 0, 0, 72, 49, 29)
        pyxel.blt(310, 306, 0, 58, 71, 37, 29)
        pyxel.blt(0, 0, 1, 0, 88, 223, 13) # marc
        pyxel.blt(223, 0, 1, 0, 88, 223, 13)
        pyxel.blt(0, 313, 1, 0, 88, 223, 13)
        pyxel.blt(223, 313, 1, 0, 88, 223, 13)






    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
