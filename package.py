import pyxel


class Package:
    def __init__(self, conveyor_y_position: list, start_floor: int = 0):
        self.conveyor_y_position = conveyor_y_position

        # SPAWN FROM PIPE
        self.state = "drop"
        self.x = 406
        self.y = 251
        self.direction = -1
        self.conveyor_index = -1

        self.speed = 10
        self.active = True
        self.passed_center = False

        # sprite frames
        self.SPRITE_FRAMES = [
            (8, 140, 15, 9),  # 0
            (32, 140, 15, 9),  # 1
            (56, 140, 15, 9),  # 2
            (80, 140, 15, 9),  # 3
            (104, 139, 15, 10),  # 4
            (0, 116, 15, 9),  # 5
        ]
        self.current_frame_index = 0
        self.move_timer = 0  # contador de frames
        self.move_interval = 50  # cada cuántos frames se mueve un pixel (ajusta para “saltado”)

    def update(self, mario, luigi):
        if not self.active:
            return

        # DROP: from pipe to mario catch point
        if self.state == "drop":
            self.move_timer += 1
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.x += self.speed * self.direction
            mario_catch_x = 327


            if self.x <= mario_catch_x:
                if mario.floor == 0 and mario.state == "idle":
                    mario.set_busy()
                    self.conveyor_index = 0
                    self.x = 283
                    self.y = 234
                    self.direction = -1
                    self.state = "moving"
                else:
                    self.state = "falling"
            return

        # FALL
        if self.state == "falling":
            self.move_timer += 7
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.y += 3
            if self.y > 280:
                self.active = False
            return

        # MOVING on conveyor
        if self.state == "moving":
            self.move_timer += 1
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.x += self.speed * self.direction
                self._update_animation()
                self._check_edges(mario, luigi)

    def _update_animation(self):
        # simple: toggle frame when crossing center; safe wrap
        center_x = 236
        if not self.passed_center:
            if (self.direction == -1 and self.x <= center_x) or (self.direction == 1 and self.x >= center_x):
                # advance (circular) once per center crossing
                self.current_frame_index = (self.current_frame_index + 1) % len(self.SPRITE_FRAMES)
                self.passed_center = True
        else:
            if (self.direction == -1 and self.x > center_x) or (self.direction == 1 and self.x < center_x):
                self.passed_center = False

    def _check_edges(self, mario, luigi):
        # MARIO side (right)
        if self.conveyor_index % 2 != 0 and self.x >= 291:
            if mario.floor == (self.conveyor_index + 1) / 2 and mario.state == "idle":
                mario.set_busy()
                self.conveyor_index += 1

                self.y = self.conveyor_y_position[self.conveyor_index]
                self.direction = -1
                self.x = 289
            else:
                self.state = "falling"
            return

        # LUIGI side (left)
        if self.conveyor_index % 2 == 0 and self.x <= 195:
            if luigi.floor == self.conveyor_index / 2 and luigi.state == "idle":
                luigi.set_busy()
                self.conveyor_index += 1

                if self.conveyor_index >= len(self.conveyor_y_position):
                    self.state = "delivered"
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
