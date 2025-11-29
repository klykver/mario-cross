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
    #   Mario стає зайнятим (коли бере пакунок)

    def set_busy(self):
        self.state = "busy"
        self.busy_timer = 10  # тримає пакунок 10 кадрів

    def _update_busy(self):
        if self.busy_timer > 0:
            self.busy_timer -= 1
        else:
            self.state = "idle"

    def update(self):
        # Якщо Mario переносить пакунок → не рухається
        if self.state == 'busy':
            self._update_busy()
            return

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
        if self.state == 'busy':
            pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30, 0)
            return

        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 0, 17, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30, 0)

        elif self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 55, 0, 15, 28, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 80, 0, 15, 28, 0)