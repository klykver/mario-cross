from mario import Mario
from luigi import Luigi
from package import Package
from boss import Boss
from truck import Truck
import pyxel


class Game:
    def __init__(self):
        pyxel.init(504, 280, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")

        self.mario = Mario(313, 235)
        self.luigi = Luigi(173, 210)
        self.boss = Boss()
        self.truck = Truck(50, 157)

        # game states: "menu", "playing", "paused", "gameover"
        self.state = "menu"

        self.mario_lives = 3
        self.luigi_lives = 3

        # Координати Y конвеєрів
        self.conveyor_y_positions = [234, 210, 186, 162, 138]

        self.packages = []
        self.spawn_timer = 0
        self.score = 0
        self.failed_packages = 0

        # pause timer when boss appears / fall happens (frames)
        self.pause_timer = 0
        self.guilty = None  # "mario" or "luigi"

        # стартовий пакунок
        self.packages.append(Package(self.conveyor_y_positions))

        self.min_packages = 1  # minimum of packages in game
        self.rise_min_per_score = 20  # after how many points the minimum increases


        pyxel.run(self.update, self.draw)


    # ---------------- background ----------------
    def draw_background_static(self):
        # Вантажівка
        #pyxel.blt(35, 157, 2, 178, 122, 70, 38, 0)
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
        # left
        pyxel.blt(493, 145, 1, 0, 192, 11, 32)
        # right
        pyxel.blt(0, 233, 1, 16, 192, 12, 32)

        # WINDOWS
        pyxel.blt(459, 130, 1, 144, 112, 25, 20)

        # exit TRUCK
        pyxel.blt(0, 132, 1, 0, 120, 32, 63, 0)

    # ---------------- foreground pillars ----------------
    def draw_foreground_pillars(self):
        pyxel.blt(243, 137, 2, 189, 10, 22, 108)
        pyxel.blt(243, 242, 2, 189, 106, 22, 9)
        pyxel.blt(243, 251, 2, 189, 106, 22, 9)
        pyxel.blt(243, 260, 2, 189, 106, 22, 9)
        pyxel.blt(243, 269, 2, 189, 106, 22, 9)
        pyxel.blt(243, 278, 2, 189, 106, 22, 9)

        # small conveyor drawn over pillar to match your layout
        pyxel.blt(341, 260, 0, 141, 112, 92, 10, 0)  # conveyor 0

    # ---------------- spawn ----------------
    def package_generator(self):
        # spawn only in playing state
        if self.state != "playing":
            return

        self.spawn_timer += 1
        if self.spawn_timer > 400:
            self.spawn_timer = 0
            new_pack = Package(self.conveyor_y_positions)
            self.packages.append(new_pack)

    def check_min_packages(self):
        if self.state != "playing":
            return
        # calcular mínimo dinámico según score
        changing_min = 1 + self.score // self.rise_min_per_score

        if len(self.packages) < changing_min:
            self.packages.append(Package(self.conveyor_y_positions))

    # ------------- finding packages on the end of conveyor ----------------
    def find_package_on_end(self):
        """return the list of packages that are at the end of the conveyors"""
        packages_on_end = []

        for p in self.packages:
            if p.active:
                #right side
                if p.x >=281 and p.direction == 1: #10 px from the end
                    packages_on_end.append(p)
                #left side
                if p.x <= 205 and p.direction == -1:
                    packages_on_end.append(p)
        return packages_on_end


    # ---------------- package updates ----------------
    def update_packages(self):
        if self.state != "playing":
            return

        # update every package
        for p in self.packages:
            prev_index = p.conveyor_index
            p.update(self.mario, self.luigi)
            # add score when package moves to next conveyor by comparing the previous conveyor index with the current one.
            if p.active and p.conveyor_index > prev_index:
                self.score += 1

        # check results AFTER updates
        new_list = []
        for p in self.packages:
            # package finished falling => trigger boss/pause
            if not p.active and p.state == "falling":
                # decide guilty based on x position (where it fell)
                if p.x > 240:
                    self.mario_lives -= 1
                    self.boss.appear("right")
                    self.mario.set_scared()
                    self.guilty = "mario"

                else:
                    self.luigi_lives -= 1
                    self.boss.appear("left")
                    self.luigi.set_scared()
                    self.guilty = "luigi"

                # pause the game
                self.state = "paused"
                self.pause_timer = 60  # 2 seconds at 30 FPS
                self.failed_packages += 1

                # don't keep this package
                continue

            # successful delivery: if package became inactive via being delivered
            if not p.active and p.state != "falling":
                # Add package on truck
                if not self.truck.is_full:
                    self.truck.add_package()
                    #check if truck is full
                    if self.truck.is_full:
                        # remove only the packages that are at the end of the conveyors
                        for p in self.find_package_on_end():
                            p.active = False
                        # pause the game
                        self.state = "paused"
                        self.pause_timer = self.truck.DELIVERY_DURATION  # 4 seconds at 30 FPS
                        self.score += 10        # add 10 points

                continue

            # keep active packages
            if p.active:
                new_list.append(p)

        self.packages = new_list

    # ---------------- main update ----------------
    def update(self):
        # handle quitting
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # state: menu
        if self.state == "menu":
            if pyxel.btnp(pyxel.KEY_SPACE):
                # reset everything and start
                self.reset_game()
                self.state = "playing"
            return

        # state: paused (boss active)
        if self.state == "paused":
            self.boss.update()
            self.truck.update()
            # decrement pause timer
            self.pause_timer -= 1
            # during pause: do not update packages or players
            if self.pause_timer <= 0:
                # end pause
                self.state = "playing"
                self.boss.active = False
                # wake up guilty
                if self.guilty == "mario":
                    self.mario.end_scared()
                elif self.guilty == "luigi":
                    self.luigi.end_scared()
                self.guilty = None
            return

        # state: gameover
        if self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                self.state = "playing"
            return

        # playing state
        if self.state == "playing":
            self.mario.update()
            self.luigi.update()
            self.package_generator()
            self.check_min_packages()
            self.update_packages()
            self.truck.update()


            # check lives -> game over
            if self.mario_lives <= 0 or self.luigi_lives <= 0:
                self.state = "gameover"
            return

    # ---------------- reset ----------------
    def reset_game(self):
        self.mario = Mario(313, 235)
        self.luigi = Luigi(173, 210)
        self.boss = Boss()
        self.mario_lives = 3
        self.luigi_lives = 3
        self.packages = [Package(self.conveyor_y_positions)]
        self.spawn_timer = 0
        self.score = 0
        self.failed_packages = 0
        self.pause_timer = 0
        self.guilty = None

    # ---------------- draw ----------------
    def draw(self):
        pyxel.cls(0)

        # background
        self.draw_background_static()

        # characters
        self.mario.draw()
        self.luigi.draw()

        # packages (always drawn)
        for p in self.packages:
            p.draw()

        # truck and packages on truck
        self.truck.draw()
        self.truck.draw_packages()

        # foreground pillars + small conveyor
        self.draw_foreground_pillars()

        # boss drawn on top if active
        self.boss.draw()

        # HUD: score & fails
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(5, 15, f"FAILED: {self.failed_packages}", 8)

        # lives
        for i in range(self.mario_lives):
            pyxel.blt(300 + i * 20, 20, 1, 2, 64, 15, 16, 0)
        for i in range(self.luigi_lives):
            pyxel.blt(160 + i * 20, 20, 1, 26, 64, 15, 16, 0)

        # overlays
        if self.state == "menu":
            # centered title & instruction
            pyxel.text(220, 70, "MARIO BROS FACTORY", 7)
            pyxel.text(220, 80, "PRESS SPACE TO START", 8)
        elif self.state == "paused":
            # full-truck / boss / guilty overlay: show message
            if self.truck.is_full == True:
                pyxel.text(200, 100, "TRUCK FULL! Delivering packages...", 8)
            else:
                pyxel.text(200, 100, "BOSS! He punished the worker!", 8)
                pyxel.text(200, 110, "Game will resume soon...", 7)

        elif self.state == "gameover":
            pyxel.text(200, 100, "GAME OVER", 8)
            pyxel.text(200, 110, "PRESS SPACE TO RESTART", 7)

