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

        self.speed = 0.7
        self.active = True
        self.passed_center = False

        # Анімаційні кадри
        self.SPRITE_FRAMES = [
            (8, 140, 15, 9),  # 0
            (32, 140, 15, 9),  # 1
            (56, 140, 15, 9),  # 2
            (80, 140, 15, 9),  # 3
            (104, 139, 15, 10),  # 4
            (0, 116, 15, 9),  # 5
        ]

        self.current_frame_index = 0

    def update(self, mario, luigi):
        if not self.active:
            return

        # з труби виходить
        if self.state == "drop":
            self.x += self.speed * self.direction

            mario_catch_x = 327

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
        center_x = 236

        # comprobamos si el paquete ha cruzado el centro
        if not self.passed_center:
            if (self.direction == -1 and self.x <= center_x) or \
                    (self.direction == 1 and self.x >= center_x):
                # change sprite after center
                self.current_frame_index = (self.current_frame_index + 1) # % len(self.SPRITE_FRAMES) <- this is to return to the first one if we reach the end

                self.passed_center = True
        else:
            # si se aleja del centro, reseteamos para poder detectar al volver
            if (self.direction == -1 and self.x > center_x) or \
                    (self.direction == 1 and self.x < center_x):
                self.passed_center = False

    def _check_edges(self, mario, luigi):
        #MARIO SIDE (праворуч)

        # Para luigi:  si el conveyer es par->dividimos entre 2 y si coincide con el numero de piso entonces se pasa el paquete
        #Para mario: como el piso cero en este momento no se tiene en cuanta ya que no es par, usamos la siguiete formula de relación entre pisos e indice de conveyors. mario.floor == (self.conveyor_index  + 1) / 2

        if self.conveyor_index % 2 != 0 and self.x >= 289:
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
                self.x = 289
            else:
                self.state = "falling"
            return

        # LUIGI SIDE (зліва)

        if self.conveyor_index % 2 == 0 and self.x <= 192:
            if luigi.floor == self.conveyor_index / 2 and luigi.state == "idle":
                luigi.set_busy()
                self.conveyor_index += 1

                if self.conveyor_index >= len(self.conveyor_y_position):
                    self.active = False
                    return

                self.y = self.conveyor_y_position[self.conveyor_index]
                self.direction = 1
                self.x = 205
            else:
                self.state = "falling"

    def draw(self):
        if not self.active:
            return

        u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]
        pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)
