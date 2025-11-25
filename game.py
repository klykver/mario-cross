
from mario import Mario
from luigi import Luigi
import pyxel


class Game:
    def __init__(self):
        pyxel.init(400, 240, title="Mario Bros Factory") # antes 446x326 aumento de 86
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(313, 182, 3)
        pyxel.run(self.update, self.draw)  #must be last line in init


    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(200, 30, 2, 0,0,3,4)#midel point
        pyxel.blt(211,118,2,189,9,22,109)#division between
        pyxel.blt(199,109,2,176,0,48,9)# TOP
        pyxel.blt(233,133,2,211,20,36,10) #conveyor 1 right
        pyxel.blt(233, 152, 2, 211, 40, 39, 10)  # conveyor 2 right
        pyxel.blt(233, 171, 2, 211, 60, 36, 10)  # conveyor 3 right
        pyxel.blt(233, 190, 2, 211, 80, 39, 10)  # conveyor 4 right
        pyxel.blt(233, 209, 2, 211, 100, 36, 10)  # conveyor 5 right
        #left
        pyxel.blt(171, 133, 2, 149, 20, 40, 10)  # conveyor 1
        pyxel.blt(174, 152, 2, 152, 40, 37, 10)  # conveyor 2
        pyxel.blt(171, 171, 2, 149, 60, 40, 10)  # conveyor 3
        pyxel.blt(174, 190, 2, 152, 80, 37, 10)  # conveyor 4
        pyxel.blt(171, 209, 2, 149, 100, 40, 10)  # conveyor 5
        #floors
        pyxel.blt(286, 148, 2, 8, 158, 23, 29)
        pyxel.blt(286, 186, 2, 8, 198, 23, 29)
        #pyxel.blt(23, 108, 2, 0, 0, 255, 119)  # left side esta elevado a 13 cm del suelo
        #pyxel.blt(278, 108, 2, 0, 118, 255, 119)#right side
        pyxel.blt(313, 171, 0, 0, 72, 49, 29)#second flor mario
        pyxel.blt(310, 220, 0, 58, 71, 37, 29)#first flor mario
        pyxel.blt(0, 0, 1, 0, 88, 223, 13) # marc
        pyxel.blt(223, 0, 1, 0, 88, 223, 13)
        pyxel.blt(0, 227, 1, 0, 88, 223, 13)
        pyxel.blt(223, 227, 1, 0, 88, 223, 13)






    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
