import pyxel

pyxel.init(256, 256)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)

pyxel.run(update, draw)