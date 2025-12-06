import pyxel

class Luigi:
    def __init__(self, x: int, y: int):
        self.x = x
        self.floor_y_position = [210, 162, 114]
        self.floor = 0
        self.max_floor = len(self.floor_y_position) - 1

        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 3

        self.state = 'idle'
        self.busy_timer = 0

    def set_busy(self):
        self.state = "busy"
        self.busy_timer = 10

    def set_scared(self):
        self.state = "scared"
        self.busy_timer = 60

    def end_scared(self):
        self.state = "idle"
        self.busy_timer = 0
        self.y = self.floor_y_position[self.floor]

    def _update_busy(self):
        if self.busy_timer > 0:
            self.busy_timer -= 1
        else:
            self.state = "idle"

    def update(self):
        if self.state == 'busy':
            self._update_busy()
            return
        if self.state == 'scared':
            if self.busy_timer > 0:
                self.busy_timer -= 1
            return

        if self.state == 'idle':
            if pyxel.btn(pyxel.KEY_W) and self.floor < self.max_floor:
                self.floor += 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = 'climbing'
            elif pyxel.btn(pyxel.KEY_S) and self.floor > 0:
                self.floor -= 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = 'climbing'

        elif self.state == 'climbing':
            dist = self.target_y - self.y
            if abs(dist) <= self.climb_speed:
                self.y = self.target_y
                self.state = 'idle'
            else:
                self.y += self.climb_speed if dist > 0 else -self.climb_speed

    def draw(self):
        if self.state == "scared":
            pyxel.blt(self.x, self.y + 5, 0, 119, 35, 17, 29, 0)
            return

        if self.state == 'busy':
            if (pyxel.frame_count % 60) < 15:
                pyxel.blt(self.x, self.y+ 11, 0, 144, 43, 24, 23, 0)
            else:
                pyxel.blt(self.x, self.y , 0, 89, 32, 23, 31, 0)
            return

        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 32, 14, 34, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 0, 32, 16, 34, 0)
            return

        if self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 72, 32, 15, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 48, 32, 15, 33, 0)
            return
