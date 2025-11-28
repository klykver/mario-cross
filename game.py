from mario import Mario
from luigi import Luigi
from package import Package
import pyxel


class Game:
    def __init__(self):
        pyxel.init(504, 280, title="Mario Bros Factory") #326---440
        pyxel.load("assets/sprites.pyxres")
        self.mario = Mario(313, 235)
        self.luigi = Luigi(139, 210)
        self.packages = []
        self.spawn_timer = 0
        self.packages.append(Package(self.mario.floor_y_position, start_floor=0))
        pyxel.run(self.update, self.draw)  #must be last line in init

    def draw_background(self):
        # (x, y, img, u, v, w, h)
        pyxel.blt(30,157,2,178,122,70,38,0) #truck
        pyxel.blt(406, 180, 0, 0, 184, 24, 72,0)# pipe
        pyxel.blt(341, 260, 0, 141, 112, 92, 10,0) # conveyor 0

        pyxel.blt(313, 177, 0, 0, 72, 49, 29,0) #2º floor mario
        pyxel.blt(313, 224, 0, 0, 72, 49, 29,0) # 1º floor mario
        pyxel.blt(313, 272, 0, 3, 152, 200, 14,0) #graund mario
        pyxel.blt(139, 195, 0, 63, 72, 49,29,0 ) #1ºfloor luigi
        pyxel.blt(139, 147, 0, 63, 72, 49, 29,0) #2º floor luigi
        pyxel.blt(139, 243, 0, 64, 168, 48, 39,0)  # graund luigi


        pyxel.blt(0, 195, 0, 4, 152, 150, 15,0)  # complementary road for truck 1ºfloor
        pyxel.blt(0, 265, 0, 4, 152, 140, 15,0)  # complementary road for boss luigi
        pyxel.blt(350, 177, 0, 4, 152, 195, 15,0)  # complementary road for boss mario2º
        pyxel.blt(350, 224, 0, 4, 152, 57, 15, 0)  # complementary road connect pipe
        pyxel.blt(130, 147, 0, 129, 168, 15, 49) #horizontal wall luigi



        #for this one we need to make an for loop. nº of conveyors will depend on difficulty
        pyxel.blt(203, 232, 1, 0, 16, 95, 26) #1 conveyor from the bottom
        pyxel.blt(203, 208, 1, 0, 16, 95, 26) #2 conveyor from the bottom
        pyxel.blt(203, 184, 1, 0, 16, 95, 26) #3 conveyor from the bottom
        pyxel.blt(203, 160, 1, 0, 16, 95, 26) #4 conveyor from the bottom
        pyxel.blt(203, 136, 1, 0, 16, 95, 26) #5 conveyor from the bottom

    def package_generator(self):
        # --- СПАВН ПАКУНКІВ ---
        self.spawn_timer += 1
        # Кожні 120 кадрів (4 секунди) з'являється новий
        if self.spawn_timer > 120:
            self.spawn_timer = 0
            # Передаємо список висот з Маріо (вони там вже є)
            new_pack = Package(self.mario.floor_y_position, 0)
            self.packages.append(new_pack)
        active_packages = [p for p in self.packages if p.active] #we create this to now how many packages are in the game
        while len(active_packages) < 3:
            new_pack = Package(self.mario.floor_y_position, 0)
            self.packages.append(new_pack)
            active_packages.append(new_pack)

        # --- ОНОВЛЕННЯ ПАКУНКІВ ---
        for p in self.packages:
            # Передаємо маріо і луїджі для перевірки зіткнень
            p.update(self.mario,self.luigi)  # тут ще луіджі має бути


        # Видаляємо неактивні пакунки (щоб пам'ять не забивалась)
        self.packages = [p for p in self.packages if p.active]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()
        self.luigi.update()
        self.package_generator()



    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        self.mario.draw()
        self.luigi.draw()
        for p in self.packages:
            p.draw()

