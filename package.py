import pyxel


class Package:
    def __init__(self, conveyor_y_position: list, start_floor: int = 0):  # do we need the start floor?
        self.conveyor_y_position = conveyor_y_position

        #SPAWN FROM PIPE
        self.state = "drop"
        self.x = 406  # труба справа
        self.y = 251  # drop road
        self.direction = -1
        self.conveyor_index = -1  # ще не на конвеєрі

        self.speed = 1
        self.active = True

        # Анімаційні кадри
        self.SPRITE_FRAMES = [
            (8, 140, 15, 9),  # 0
            (32, 140, 15, 9),  # 1
            (56, 140, 15, 9),  # 2
            (80, 140, 15, 9),  # 3
            (104, 138, 15, 11),  # 4
            (0, 117, 15, 9),  # 5
        ]

        self.current_frame_index = 0

    def update(self, mario, luigi):
        if not self.active:
            return

        # з труби виходить
        if self.state == "drop":
            self.x += self.speed * self.direction

            mario_catch_x = 313

            if self.x <= mario_catch_x:
                # Mario ловить тільки якщо стоїть на нижньому поверсі
                if mario.floor == 0 and mario.state == "idle":
                    mario.set_busy()
                    self.conveyor_index = 0
                    self.x = 283  # старт конвеєру
                    self.y = 234
                    self.direction = -1  # тепер їде до Luigi
                    self.state = "moving"
                else:
                    self.state = "falling"
            return

        #FALL
        if self.state == "falling":
            self.y += 3
            if self.y > 350:
                self.active = False
            return

        if self.state == "moving":
            self.x += self.speed * self.direction
            self._update_animation()
            self._check_edges(mario, luigi)

    def _update_animation(self):
        if self.conveyor_index <= 0:
            base = 0
        elif self.conveyor_index == 1:
            base = 2
        else:
            base = 4

        center_x = 236
        passed_center = (self.direction == 1 and self.x > center_x) or \
                        (self.direction == -1 and self.x < center_x)

        self.current_frame_index = base + (1 if passed_center else 0)

    def _check_edges(self, mario, luigi):
        #MARIO SIDE (праворуч)

        # Para luigi:  si el conveyer es par->dividimos entre 2 y si coincide con el numero de piso entonces se pasa el paquete
        #Para mario: como el piso cero en este momento no se tiene en cuanta ya que no es par, usamos la siguiete formula de relación entre pisos e indice de conveyors. mario.floor == (self.conveyor_index  + 1) / 2

        if self.conveyor_index % 2 != 0 and self.x >= 283:
            if mario.floor == (self.conveyor_index + 1) / 2 and mario.state == "idle":
                mario.set_busy()
                self.conveyor_index += 1

                # truck?
                if self.conveyor_index >= len(self.conveyor_y_position):
                    self.active = False
                    return

                # переходимо на наступний конвеєр
                self.y = self.conveyor_y_position[self.conveyor_index]
                self.direction = -1
                self.x = 283
            else:
                self.state = "falling"
            return

        # LUIGI SIDE (зліва)

        if self.conveyor_index % 2 == 0 and self.x <= 203:
            if luigi.floor == self.conveyor_index / 2 and luigi.state == "idle":
                luigi.set_busy()
                self.conveyor_index += 1

                if self.conveyor_index >= len(self.conveyor_y_position):
                    self.active = False
                    return

                self.y = self.conveyor_y_position[self.conveyor_index]
                self.direction = 1
                self.x = 203
            else:
                self.state = "falling"

    def draw(self):
        if not self.active:
            return

        u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]
        pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)
