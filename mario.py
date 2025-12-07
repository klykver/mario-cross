import pyxel


class Mario:
    def __init__(self, x: int, y: int):
        self.x = x
        # allowed floor y positions
        self.floor_y_position = [243, 195, 148]
        self.floor = 0
        self.max_floor = len(self.floor_y_position) - 1

        # current and target vertical positions
        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 3

        # simple FSM for player
        self.state = "idle"   # 'idle', 'climbing', 'busy', 'scared'
        self.busy_timer = 0

    # ---------------- properties ----------------
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, val: int):
        if not isinstance(val, int):
            raise TypeError("x must be int")
        self.__x = val

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, val: int):
        if not isinstance(val, int):
            raise TypeError("y must be int")
        self.__y = val

    @property
    def floor(self) -> int:
        return self.__floor

    @floor.setter
    def floor(self, val: int):
        if not isinstance(val, int):
            raise TypeError("floor must be int")
        if val < 0 or val > len(self.floor_y_position) - 1:
            raise ValueError("floor out of range")
        self.__floor = val

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, val: str):
        if not isinstance(val, str):
            raise TypeError("state must be str")
        self.__state = val

    @property
    def busy_timer(self) -> int:
        return self.__busy_timer

    @busy_timer.setter
    def busy_timer(self, val: int):
        if not isinstance(val, int):
            raise TypeError("busy_timer must be int")
        if val < 0:
            raise ValueError("busy_timer cannot be negative")
        self.__busy_timer = val

    @property
    def climb_speed(self) -> int:
        return self.__climb_speed

    @climb_speed.setter
    def climb_speed(self, val: int):
        if not isinstance(val, int):
            raise TypeError("climb_speed must be int")
        if val <= 0:
            raise ValueError("climb_speed must be positive")
        self.__climb_speed = val

    # ---------------- actions ----------------
    def set_busy(self):
        """Player is busy (caught a package). Short timer to block input."""
        self.state = "busy"
        self.busy_timer = 10

    def set_scared(self):
        """Player is scared when boss appears. Longer timer while paused."""
        self.state = "scared"
        self.busy_timer = 60

    def end_scared(self):
        """Reset scared state back to idle and snap y to current floor."""
        self.state = "idle"
        self.busy_timer = 0
        self.y = self.floor_y_position[self.floor]

    def _update_busy(self):
        """Decrease the busy timer and clear the busy status once it reaches zero."""
        if self.busy_timer > 0:
            self.busy_timer -= 1
        else:
            self.state = "idle"

    def update(self):
        """Frame update for Mario: manages state-based behavior (busy/scared timers, idle input, climbing animation)."""
        # busy or scared -> count down but don't accept input
        if self.state == "busy":
            self._update_busy()
            return
        if self.state == "scared":
            if self.busy_timer > 0:
                self.busy_timer -= 1
            return

        # input when idle
        if self.state == "idle":
            if pyxel.btn(pyxel.KEY_UP) and self.floor < self.max_floor:
                self.floor += 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = "climbing"
            elif pyxel.btn(pyxel.KEY_DOWN) and self.floor > 0:
                self.floor -= 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = "climbing"

        elif self.state == "climbing":
            dist = self.target_y - self.y
            if abs(dist) <= self.climb_speed:
                self.y = self.target_y
                self.state = "idle"
            else:
                self.y += self.climb_speed if dist > 0 else -self.climb_speed

    def draw(self):
        """Draw Mario sprite depending on state."""
        if self.state == "scared":
            pyxel.blt(self.x, self.y + 10, 0, 207, 8, 24, 22, 0)
            return

        if self.state == "busy":
            if (pyxel.frame_count % 60) < 15:
                pyxel.blt(self.x, self.y, 0, 103, 8, 25, 22, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 143, 0, 24, 30, 0)
            return

        if self.state == "idle":
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 0, 17, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30, 0)
            return

        if self.state == "climbing":
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 55, 0, 15, 28, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 80, 0, 15, 28, 0)
            return
