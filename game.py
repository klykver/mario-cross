from mario import Mario
from luigi import Luigi
from package import Package
import pyxel


class Game:
    def __init__(self):
        pyxel.init(504, 280, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")

        self.mario = Mario(313, 235)
        self.luigi = Luigi(173, 210)

        # Координати Y конвеєрів
        self.conveyor_y_positions = [234, 210, 186, 162, 138]

        self.packages = []
        self.spawn_timer = 0
        self.score = 0
        self.failed_packages = 0

        # Створюємо ОДИН пакунок для старту
        #self.packages.append(Package(self.mario.floor_y_position, start_floor=0))<- dont understant
        self.packages.append(Package(self.conveyor_y_positions)) #<- more sense?

        pyxel.run(self.update, self.draw)

    # --- МЕТОД 1: МАЛЮЄМО ТЕ, ЩО ПОЗАДУ ---
    def draw_background_static(self):
        # Вантажівка
        pyxel.blt(35, 157, 2, 178, 122, 70, 38, 0)
        # Труба
        pyxel.blt(406, 180, 0, 0, 184, 24, 72, 0)


        # Платформи Маріо
        pyxel.blt(313, 177, 0, 0, 72, 49, 29, 0)
        pyxel.blt(313, 224, 0, 0, 72, 49, 29, 0)
        pyxel.blt(313, 272, 0, 3, 152, 200, 14, 0)

        # Платформи Луїджі
        pyxel.blt(139, 195, 0, 63, 72, 49, 29, 0)
        pyxel.blt(139, 147, 0, 63, 72, 49, 29, 0)
        pyxel.blt(139, 243, 0, 64, 168, 48, 39, 0)

        # Додаткові дороги
        pyxel.blt(0, 195, 0, 4, 152, 150, 15, 0)
        pyxel.blt(0, 265, 0, 4, 152, 140, 15, 0)
        pyxel.blt(350, 177, 0, 4, 152, 195, 15, 0)
        pyxel.blt(350, 224, 0, 4, 152, 57, 15, 0)
        pyxel.blt(130, 147, 0, 129, 168, 15, 49)

        # Конвеєри (малюємо їх позаду пакунків)
        pyxel.blt(200, 232, 1, 0, 16, 95, 26)
        pyxel.blt(208, 208, 1, 0, 16, 95, 26)
        pyxel.blt(200, 184, 1, 0, 16, 95, 26)
        pyxel.blt(208, 160, 1, 0, 16, 95, 26)
        pyxel.blt(200, 136, 1, 0, 16, 95, 26)

        # Верхівка конвеєра
        pyxel.blt(230, 127, 2, 176, 0, 47, 11)

        # DOORS
        #left
        pyxel.blt(493, 145, 1, 0, 192, 11, 32)
        #right
        pyxel.blt(0, 233, 1, 16, 192, 12, 32)

        # WINDOWS
        pyxel.blt(459, 130, 1, 144, 112, 25, 20)

        #exit TRUCK
        pyxel.blt(0, 132, 1, 0, 120, 32, 63, 0)
        #FAILS
        pyxel.blt(300, 60, 1, 2, 64, 15, 16)
        pyxel.blt(320, 60, 1, 2, 64, 15, 16)
        pyxel.blt(340, 60, 1, 2, 64, 15, 16)
        pyxel.blt(200, 60, 1, 26, 64, 15, 16)
        pyxel.blt(180, 60, 1, 26, 64, 15, 16)
        pyxel.blt(160, 60, 1, 26, 64, 15, 16)


        #EXIT
        pyxel.blt(7, 119, 1, 176, 112, 24, 8)


        #SCORE
        pyxel.blt(440, 70, 1, 64, 85, 8, 15)
        pyxel.blt(460, 70, 1, 64, 85, 8, 15)
        pyxel.blt(480, 70, 1, 64, 85, 8, 15)




    # --- МЕТОД 2: МАЛЮЄМО ТЕ, ЩО СПЕРЕДУ (Щоб закрити пакунки) ---
    def draw_foreground_pillars(self):
        # Центральна колона (малюється ПОВЕРХ пакунків)
        pyxel.blt(243, 137, 2, 189, 10, 22, 108)
        pyxel.blt(243, 242, 2, 189, 106, 22, 9)
        pyxel.blt(243, 251, 2, 189, 106, 22, 9)
        pyxel.blt(243, 260, 2, 189, 106, 22, 9)
        pyxel.blt(243, 269, 2, 189, 106, 22, 9)
        pyxel.blt(243, 278, 2, 189, 106, 22, 9)

        pyxel.blt(341, 260, 0, 141, 112, 92, 10, 0)  # conveyor 0

    def package_generator(self):
        self.spawn_timer += 1

        # ВИПРАВЛЕННЯ: Прибрав while loop.
        # Пакунки мають з'являтися по одному, з інтервалом.
        # 180 кадрів = 6 секунд (при 30 FPS).
        if self.spawn_timer > 180:
            self.spawn_timer = 0
            new_pack = Package(self.conveyor_y_positions,0)
            self.packages.append(new_pack)

    def update_packages(self):
        for p in self.packages:
            p.update(self.mario, self.luigi)

            if not p.active:
                if p.state == "falling":
                    self.failed_packages += 1
            else:
                if p.state == "pass": #it is wrong as it will be adding until it fels.
                    self.score += 1

        self.packages = [p for p in self.packages if p.active]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.update()
        self.luigi.update()
        self.package_generator()
        self.update_packages()

    def draw(self):
        pyxel.cls(0)

        # 1. ШАР 1: Фон (Стіни, конвеєри)
        self.draw_background_static()

        # 2. ШАР 2: Персонажі
        self.mario.draw()
        self.luigi.draw()

        # 3. ШАР 3: Пакунки (вони будуть ПОВЕРХ фону, але ПІД колоною)
        for p in self.packages:
            p.draw()

        # 4. ШАР 4: Передній план (Колона закриває пакунки)
        self.draw_foreground_pillars()

        # HUD
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(5, 15, f"FAILED: {self.failed_packages}", 8)

