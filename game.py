from mario import Mario
from luigi import Luigi
from package import Package
from boss import Boss
from truck import Truck
import pyxel
import random


class Game:
    def __init__(self):
        """
        Main game controls states, objects and global logic.
        """
        #screen
        pyxel.init(504, 280, title="Mario Bros Factory")
        pyxel.load("assets/sprites.pyxres")

        #game state and attributes default values
        self.state = "menu"
        self.mario_luigi_lives = 3
        self.packages = []
        self.spawn_timer = 0
        self.score = 0
        self.failed_packages = 0
        self.number_of_deliveries = 0
        self.pause_timer = 0
        self.guilty = None
        self.min_packages = 1
        self.conveyor_y_positions = [234, 210, 186, 162, 138]

        """
        difficulty table:
        "invert" charges the keys that moves Mario and Luigi
        "spd_odd" and "spd_even" charge the conveyor speed
        "increase_min_pkg_per_score" charges the minimum number of packages that are on the belts per score
        "truck_eliminate_fail" changes the number of failed packages after the truck delivers the packages
        """
        self.levels = {
            "Easy": {
                "invert": False,
                "spd_odd": 1.0,
                "spd_even": 1.0,
                "increase_min_pkg_per_score": 50,
                "truck_eliminate_fail": 3
            },
            "Medium": {
                "invert": False,
                "spd_odd": 1.5,
                "spd_even": 1,
                "increase_min_pkg_per_score": 30,
                "truck_eliminate_fail": 5
            },
            "Extreme": {
                "invert": False,
                "spd_odd": 2,
                "spd_even": 1.5,
                "increase_min_pkg_per_score": 30,
                "truck_eliminate_fail": 5
            },
            "Crazy": {
                "invert": True,
                "spd_odd": random.randint(1, 2),
                "spd_even": random.randint(1, 2),
                "increase_min_pkg_per_score": 20,
                "truck_eliminate_fail": None
            }
        }

        # apply default values
        self.selected_level_name = "Easy"
        self.current_settings = self.levels["Easy"]

        # characters/objects
        self.mario = Mario(313, self.current_settings["invert"])
        self.luigi = Luigi(173, self.current_settings["invert"])
        self.boss = Boss()
        self.truck = Truck(50, 157)

        #  initial package displayed on the screen
        first_pack = Package(
            self.conveyor_y_positions,
            10,
            self.current_settings["spd_even"],
            self.current_settings["spd_odd"]
        )
        self.packages.append(first_pack)

        pyxel.run(self.update, self.draw)

    # ============================================================
    #                       PROPERTIES
    # ============================================================

    # ---------------- STATE ----------------
    @property
    def state(self):
        """Return the current game state."""
        return self.__state

    @state.setter
    def state(self, value):
        """
        Must be one of: "menu", "playing", "paused", "gameover".
        """
        if value not in ("menu", "playing", "paused", "gameover"):
            raise ValueError("Invalid game state.")
        self.__state = value

    # ---------------- SELECTED LEVEL ----------------
    @property
    def selected_level_name(self):
        """Return the name of the selected difficulty level."""
        return self.__selected_level_name

    @selected_level_name.setter
    def selected_level_name(self, value):
        """
        Must be the existing difficulty level name inside the level dictionary: "Easy", "Medium", "Extreme", "Crazy".
        """
        if value not in self.levels:
            raise ValueError("Difficulty level does not exist.")
        self.__selected_level_name = value

    # ---------------- CURRENT SETTINGS ----------------
    @property
    def current_settings(self):
        """Return the active difficulty parameter dictionary."""
        return self.__current_settings

    @current_settings.setter
    def current_settings(self, value):
        """
        Must contain all required fields.
        """
        required = [
            "invert",
            "spd_odd",
            "spd_even",
            "increase_min_pkg_per_score",
            "truck_eliminate_fail"
        ]
        for key in required:
            if key not in value:
                raise ValueError(f"Missing level parameter: {key}")
        self.__current_settings = value

    # ---------------- LIVES ----------------
    @property
    def mario_luigi_lives(self):
        """Return total lives for Mario and Luigi."""
        return self.__mario_luigi_lives

    @mario_luigi_lives.setter
    def mario_luigi_lives(self, value):
        """Must be non-negative."""
        if value < 0:
            raise ValueError("Lives cannot be negative.")
        self.__mario_luigi_lives = value

    # ---------------- PACKAGES LIST ----------------
    @property
    def packages(self):
        """Return the list of active packages in the game."""
        return self.__packages

    @packages.setter
    def packages(self, value):
        """ Must be a list."""
        if not isinstance(value, list):
            raise TypeError("packages must be a list.")
        self.__packages = value

    # ---------------- SCORE ----------------
    @property
    def score(self):
        """Return the current score."""
        return self.__score

    @score.setter
    def score(self, value):
        """Cannot be negative."""
        if value < 0:
            raise ValueError("Score cannot be negative.")
        self.__score = value

    # ---------------- FAILED PACKAGES ----------------
    @property
    def failed_packages(self):
        """Return the number of failed packages."""
        return self.__failed_packages

    @failed_packages.setter
    def failed_packages(self, value):
        """Cannot be negative."""
        if value < 0:
            raise ValueError("Cannot have negative failed packages.")
        self.__failed_packages = value

    # ---------------- DELIVERIES ----------------
    @property
    def number_of_deliveries(self):
        """Return the number of completed truck deliveries."""
        return self.__number_of_deliveries

    @number_of_deliveries.setter
    def number_of_deliveries(self, value):
        """Cannot be negative."""
        if value < 0:
            raise ValueError("Deliveries cannot be negative.")
        self.__number_of_deliveries = value

    # ---------------- PAUSE TIMER ----------------
    @property
    def pause_timer(self):
        """Return remaining pause frames."""
        return self.__pause_timer

    @pause_timer.setter
    def pause_timer(self, value):
        """Must be >= 0."""
        if value < 0:
            value = 0
        self.__pause_timer = value

    # ---------------- GUILTY ----------------
    @property
    def guilty(self):
        """Return which character caused the pause/did not catch the package: 'mario' or 'luigi'."""
        return self.__guilty

    @guilty.setter
    def guilty(self, value):
        """Must be: None, "mario" or "luigi"."""
        if value not in (None, "mario", "luigi"):
            raise ValueError("Invalid guilty value.")
        self.__guilty = value

    # ---------------- MIN PACKAGES ----------------
    @property
    def min_packages(self):
        """Return the minimum number of packages allowed on conveyors."""
        return self.__min_packages

    @min_packages.setter
    def min_packages(self, value):
        """Minimum allowed packages (must be >= 1)."""
        if value < 1:
            raise ValueError("min_packages must be >= 1.")
        self.__min_packages = value


    # ============================================================
    #                       DRAWING METHODS
    # ============================================================

    def draw_background_static(self):
        """Draw all static background elements."""
        # pipe (generator of packages)
        pyxel.blt(406, 180, 0, 0, 184, 24, 72, 0)

        # Mario platforms
        pyxel.blt(313, 177, 0, 0, 72, 49, 29, 0)
        pyxel.blt(313, 224, 0, 0, 72, 49, 29, 0)
        pyxel.blt(313, 272, 0, 3, 152, 200, 14, 0)

        # Luigi platforms
        pyxel.blt(139, 195, 0, 63, 72, 49, 29, 0)
        pyxel.blt(139, 147, 0, 63, 72, 49, 29, 0)
        pyxel.blt(139, 243, 0, 64, 168, 48, 39, 0)

        # Additional path elements
        pyxel.blt(0, 195, 0, 4, 152, 150, 15, 0)
        pyxel.blt(0, 265, 0, 4, 152, 140, 15, 0)
        pyxel.blt(350, 177, 0, 4, 152, 195, 15, 0)
        pyxel.blt(350, 224, 0, 4, 152, 57, 15, 0)
        pyxel.blt(130, 147, 0, 129, 168, 15, 49)

        # Conveyors
        pyxel.blt(200, 232, 1, 0, 16, 95, 26)
        pyxel.blt(208, 208, 1, 0, 16, 95, 26)
        pyxel.blt(200, 184, 1, 0, 16, 95, 26)
        pyxel.blt(208, 160, 1, 0, 16, 95, 26)
        pyxel.blt(200, 136, 1, 0, 16, 95, 26)

        # Conveyor top
        pyxel.blt(230, 127, 2, 176, 0, 47, 11)

        # Decorative objects
        pyxel.blt(493, 145, 1, 0, 192, 11, 32)
        pyxel.blt(0, 233, 1, 16, 192, 12, 32)
        pyxel.blt(459, 130, 1, 144, 112, 25, 20)
        pyxel.blt(0, 132, 1, 0, 120, 32, 63, 0)


    def draw_foreground_pillars(self):
        """Draw pillars that appear in front of characters and packages."""
        pyxel.blt(243, 137, 2, 189, 10, 22, 108)
        pyxel.blt(243, 242, 2, 189, 106, 22, 9)
        pyxel.blt(243, 251, 2, 189, 106, 22, 9)
        pyxel.blt(243, 260, 2, 189, 106, 22, 9)
        pyxel.blt(243, 269, 2, 189, 106, 22, 9)
        pyxel.blt(243, 278, 2, 189, 106, 22, 9)

        # conveyor0 (in front)
        pyxel.blt(341, 260, 0, 141, 112, 92, 10, 0)


    # ---------------- spawn ----------------
    def package_generator(self):
        # spawn only in playing state
        if self.state != "playing":
            return

        # the counter grows every frame. After 400 frames, (30fps -> 400/30=13.33 seconds) a new package is spawned.
        self.spawn_timer += 1
        if self.spawn_timer > 400:
            self.spawn_timer = 0
            new_pack = Package(self.conveyor_y_positions,10,self.current_settings["spd_even"],self.current_settings["spd_odd"])
            # packages are stored in the package list.
            self.packages.append(new_pack)

    def check_min_packages(self):
        # check only in playing state
        if self.state != "playing":
            return
        # the minimum will change as the score increases
        changing_min = 1 + self.score // self.current_settings["increase_min_pkg_per_score"]

        # if the number of packages is less than the changing minimum, a new package is spawned.
        if len(self.packages) < changing_min:
            self.packages.append(Package(self.conveyor_y_positions,10,self.current_settings["spd_even"],self.current_settings["spd_odd"]))


    # ------------- finding packages on the end of conveyor ----------------
    def find_package_on_end(self):
        """return the list of packages that are at the end of the conveyors.
        When the truck is full, they will be removed."""
        packages_on_end = []
        for p in self.packages:
            if p.active:
                #right side. 10 px were removed from the end of the conveyor.
                if p.x >=291 and p.direction == 1:
                    packages_on_end.append(p)
                #left side 10 px were added to the end of the conveyor.
                if p.x <= 195 and p.direction == -1:
                    packages_on_end.append(p)
        return packages_on_end


    # ---------------- select difficulties ----------------
    def select_difficulty(self):
        """Change difficulty using 1-4 numbers on the keyboard."""

        if pyxel.btnp(pyxel.KEY_1):
            self.selected_level_name = "Easy"

        if pyxel.btnp(pyxel.KEY_2):
            self.selected_level_name = "Medium"

        if pyxel.btnp(pyxel.KEY_3):
            self.selected_level_name = "Extreme"

        if pyxel.btnp(pyxel.KEY_4):
            self.selected_level_name = "Crazy"

        # the difficulty parameters are stored in the current_settings variable
        self.current_settings = self.levels[self.selected_level_name]

    # ---------------- package updates ----------------
    def update_packages(self):
        if self.state != "playing":
            return

        # update every package
        for p in self.packages:
            prev_index = p.conveyor_index
            p.update(self.mario, self.luigi)
            # add score when package moves to next conveyor by comparing the previous conveyor index with the current one.
            if p.conveyor_index > prev_index:
                self.score += 1


        # check states AFTER updates
        new_list = []
        for p in self.packages:
            # package finished falling => boss appears /pause
            # this package will be eliminated from packages list
            if not p.active and p.state == "falling":
                # decide guilty based on x position (where it fell)
                if p.x > 240:
                    self.mario_luigi_lives -= 1
                    self.boss.appear("right")
                    # mario is scared. He does not rise until the pause is over (this logic is in the update method)
                    self.mario.set_scared()
                    self.guilty = "mario"

                else:
                    self.mario_luigi_lives -= 1
                    self.boss.appear("left")
                    self.luigi.set_scared()
                    self.guilty = "luigi"

                # pause the game
                self.state = "paused"
                self.pause_timer = 60  # 2 seconds at 30 FPS
                self.failed_packages += 1


            # successful delivery: if package became inactive, because it reached the truck
            if not p.active and p.state != "falling":
                # Add package on truck if truck is not full
                if not self.truck.is_full:
                    self.truck.add_package()
                    #check if truck is full
                    if self.truck.is_full:
                        # remove only the packages that are at the end of the conveyors
                        for p in self.find_package_on_end():
                            p.active = False
                        # pause the game
                        self.state = "paused"
                        # 4 seconds at 30 FPS. This is the time truck spend for delivery
                        self.pause_timer = self.truck.DELIVERY_DURATION
                        # add 10 points
                        self.score += 10
                        self.number_of_deliveries += 1

            # keep active packages
            if p.active:
                new_list.append(p)
        self.packages = new_list

    # ---------------- main update ----------------
    def update(self):
        # To exit the game press Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Checking states of the menu.
        if self.state == "menu":
            self.select_difficulty()

            # To start the game press space
            if pyxel.btnp(pyxel.KEY_SPACE):
                # reset game: reset all variables except the selected difficulty
                self.reset_game()
                self.state = "playing"
            return

        # state: paused (boss and truck active)
        if self.state == "paused":
            self.boss.update()
            self.truck.update()
            # decreasing pause timer
            self.pause_timer -= 1
            # during pause: do not update packages or players
            if self.pause_timer <= 0:
                # end pause
                self.state = "playing"
                self.boss.active = False
                # rise the guilty player
                if self.guilty == "mario":
                    # now mario state is "idle" and is placed on the corresponding floor.
                    self.mario.end_scared()
                elif self.guilty == "luigi":
                    # now luigi state is "idle" and is placed on the corresponding floor.
                    self.luigi.end_scared()
                self.guilty = None
            return

        # playing state
        if self.state == "playing":
            self.mario.update()
            self.luigi.update()
            self.package_generator()
            self.update_packages()
            self.truck.update()

            # check lives -> game over
            # if the number of deliveries is equal to the number of deliveries to reset one fail,
            # the number of deliveries is reset and the lives are increased by 1.
            if self.number_of_deliveries == self.current_settings["truck_eliminate_fail"]:
                self.number_of_deliveries = 0
                self.mario_luigi_lives += 1
            if self.mario_luigi_lives <= 0 :
                self.state = "gameover"
            return

        # state: gameover (after 3 fails)
        if self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                self.state = "playing"
            return

    # ---------------- reset ----------------
    """Reset all variables except the selected difficulty."""
    def reset_game(self):
        self.mario = Mario(313, self.current_settings["invert"])
        self.luigi = Luigi(173, self.current_settings["invert"])
        self.boss = Boss()
        self.mario_luigi_lives = 3
        self.packages = []
        self.packages = [Package(self.conveyor_y_positions,10,self.current_settings["spd_even"],self.current_settings["spd_odd"])]
        self.spawn_timer = 0
        self.score = 0
        self.failed_packages = 0
        self.pause_timer = 0
        self.guilty = None
        self.number_of_deliveries = 0
        self.truck.packages_on_truck = []
        self.truck.is_full = False

    # ---------------- draw ----------------
    """Draw the game."""
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
        for i in range(self.mario_luigi_lives):
            pyxel.blt(225 + i * 20, 20, 1, 2, 64, 15, 16, 0)

        # overlays
        if self.state == "menu":
            # centered title & instruction
            pyxel.text(220, 70, "MARIO BROS FACTORY", 7)
            pyxel.text(220, 80, "PRESS SPACE TO START", 8)
            pyxel.text(220, 90, "SELECT DIFFICULTY:", 10)
            pyxel.text(300, 90, "1 - EASY",7)
            pyxel.text(300, 100, "2 - MEDIUM",7)
            pyxel.text(300, 110, "3 - EXTREME", 7)
            pyxel.text(300, 120, "4 - CRAZY", 7)

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

