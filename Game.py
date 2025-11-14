from Mario import Mario
import pyxel

pyxel.init(356, 356, title="Mario Bros Factory")
pyxel.load("assets/sprites.pyxres")
mario = Mario(210, 222, 3)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    mario.update()

def draw():
    pyxel.cls(0)
    mario.draw()

pyxel.run(update, draw)