from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(356, 316, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(300, 278, 3)

        def update():
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            self.mario.update()

        def draw():
            pyxel.cls(0)
            self.mario.draw()

        pyxel.run(update, draw)
