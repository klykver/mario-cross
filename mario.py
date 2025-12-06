import pyxel

class Mario:
    def __init__(self, x: int, y: int):
        self.x = x
        self.floor_y_position = [243, 195, 148]
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
        self.busy_timer = 60  # lasts while pause is active (approx 2s)

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
        # busy or scared -> count down but don't accept input
        if self.state == 'busy':
            self._update_busy()
            return
        if self.state == 'scared':
            if self.busy_timer > 0:
                self.busy_timer -= 1
            return

        # normal input
        if self.state == 'idle':
            if pyxel.btn(pyxel.KEY_UP) and self.floor < self.max_floor:
                self.floor += 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = 'climbing'
            elif pyxel.btn(pyxel.KEY_DOWN) and self.floor > 0:
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
        # scared state: show lying sprite shifted slightly down
        if self.state == "scared":
            pyxel.blt(self.x, self.y + 10, 0, 207, 8, 24, 22, 0)
            return

        if self.state == 'busy':
            if (pyxel.frame_count % 60) < 15:
                pyxel.blt(self.x, self.y, 0, 103, 8, 25, 22, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 143, 0, 24, 30, 0)
            return

        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 0, 17, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30, 0)
            return

        if self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 55, 0, 15, 28, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 80, 0, 15, 28, 0)
            return