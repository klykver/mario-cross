import pyxel

class Package:
    def __init__(self, conveyor_y_position: list, start_floor: int = 0):
        self.conveyor_y_position = conveyor_y_position

        #SPAWN FROM PIPE
        self.state = "drop"
        self._x = 406       # труба справа
        self._y = 253       # drop road
        self._direction = -1
        self._conveyor_index = -1  # ще не на конвеєрі

        self.speed = 1
        self.active = True

        # Анімаційні кадри
        self.SPRITE_FRAMES = [
            (8, 142, 15, 7),   # 0
            (32, 140, 15, 9),  # 1
            (56, 140, 15, 9),  # 2
            (80, 140, 15, 9),  # 3
            (104, 138, 15, 11),# 4
            (0, 117, 15, 9),   # 5
        ]

        self.current_frame_index = 0

    def update(self, mario, luigi):
        if not self.active:
            return

        # з труби виходить
        if self.state == "drop":
            self._x += self.speed * self._direction

            mario_catch_x = 313

            if self._x <= mario_catch_x:
                # Mario ловить тільки якщо стоїть на нижньому поверсі
                if mario.floor == 0 and mario.state == "idle":
                    mario.set_busy()
                    self._conveyor_index = 0
                    self._x = 283          # старт конвеєру
                    self._y = 236
                    self._direction = -1    # тепер їде до Luigi
                    self.state = "moving"
                else:
                    self.state = "falling"
            return

        #FALL
        if self.state == "falling":
            self._y += 3
            if self._y > 350:
                self.active = False
            return

        if self.state == "moving":
            self._x += self.speed * self._direction
            self._update_animation()
            self._check_edges(mario, luigi)

    def _update_animation(self):
        if self._conveyor_index <= 0:
            base = 0
        elif self._conveyor_index == 1:
            base = 2
        else:
            base = 4

        center_x = 236
        passed_center = (self._direction == 1 and self._x > center_x) or \
                        (self._direction == -1 and self._x < center_x)

        self.current_frame_index = base + (1 if passed_center else 0)


    def _check_edges(self, mario, luigi):
        #MARIO SIDE (праворуч)
        if self._direction == 1 and self._x <= 283:
            if mario.floor == self._conveyor_index and mario.state == "idle":
                mario.set_busy()
                self._conveyor_index += -1

                # truck?
                if self._conveyor_index >= len(self.conveyor_y_position):
                    self.active = False
                    return

                # переходимо на наступний конвеєр
                self._y = self.conveyor_y_position[self._conveyor_index]
                self._direction = -1
                self._x = 203
            else:
                self.state = "falling"
            return

        # LUIGI SIDE (зліва)

        if self._direction == -1 and self._x >= 283:
            if luigi.floor == self._conveyor_index and luigi.state == "idle":
                luigi.set_busy()
                self._conveyor_index += 1

                if self._conveyor_index >= len(self.conveyor_y_position):
                    self.active = False
                    return

                self._y = self.conveyor_y_position[self._conveyor_index]
                self._direction = 1
                self._x = 283
            else:
                self.state = "falling"

    def draw(self):
        if not self.active:
            return

        u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]
        pyxel.blt(self._x, self._y, 0, u, v, w, h, 0)
