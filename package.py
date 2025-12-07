import pyxel
from typing import List, Tuple


class Package:
    # Simple Package class representing a package moving through conveyors.
    def __init__(self, conveyor_y_position: List[int], start_floor: int = 0):
        self.conveyor_y_position = conveyor_y_position

        # SPAWN FROM PIPE state
        self.state = "drop"            # 'drop', 'moving', 'falling', 'delivered'
        self.x = 406
        self.y = 251
        self.direction = -1            # -1 = move left, 1 = move right
        self.conveyor_index = -1

        self.speed = 10
        self.active = True
        self.passed_center = False

        # sprite frames (tuples u, v, w, h)
        self.SPRITE_FRAMES = [
            (8, 140, 15, 9),  # 0
            (32, 140, 15, 9),  # 1
            (56, 140, 15, 9),  # 2
            (80, 140, 15, 9),  # 3
            (104, 139, 15, 10),  # 4
            (0, 116, 15, 9),  # 5
        ]
        self.current_frame_index = 0
        self.move_timer = 0
        self.move_interval = 50

    # ---------------- properties ----------------
    @property
    def conveyor_y_position(self) -> List[int]:
        return self.__conveyor_y_position

    @conveyor_y_position.setter
    def conveyor_y_position(self, val):
        if not isinstance(val, list):
            raise TypeError("conveyor_y_position must be a list[int]")
        self.__conveyor_y_position = val

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
    def direction(self) -> int:
        return self.__direction

    @direction.setter
    def direction(self, val: int):
        if not isinstance(val, int):
            raise TypeError("direction must be int (-1 or 1)")
        if val not in (-1, 1):
            raise ValueError("direction must be either -1 (left) or 1 (right)")
        self.__direction = val

    @property
    def conveyor_index(self) -> int:
        return self.__conveyor_index

    @conveyor_index.setter
    def conveyor_index(self, val: int):
        if not isinstance(val, int):
            raise TypeError("conveyor_index must be int")
        self.__conveyor_index = val

    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, val: int):
        if not isinstance(val, int):
            raise TypeError("speed must be int")
        if val < 0:
            raise ValueError("speed cannot be negative")
        self.__speed = val

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("active must be bool")
        self.__active = val

    @property
    def current_frame_index(self) -> int:
        return self.__current_frame_index

    @current_frame_index.setter
    def current_frame_index(self, val: int):
        if not isinstance(val, int):
            raise TypeError("current_frame_index must be int")
        # Make sure the value stays within the allowed frame limits
        self.__current_frame_index = val % len(self.SPRITE_FRAMES)

    @property
    def move_interval(self) -> int:
        return self.__move_interval

    @move_interval.setter
    def move_interval(self, val: int):
        if not isinstance(val, int):
            raise TypeError("move_interval must be int")
        if val <= 0:
            raise ValueError("move_interval must be positive")
        self.__move_interval = val

    # ---------------- behavior ----------------
    def update(self, mario, luigi):
        """Update package state each frame"""
        if not self.active:
            return

        # DROP: from pipe to Mario catch point
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
                    # Mario missed it, package falls
                    self.state = "falling"
            return

        # FALL
        if self.state == "falling":
            self.move_timer += 7
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.y += 3
            if self.y > 350:
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
        """Switch to the next frame when the package crosses the center point."""
        center_x = 236
        if not self.passed_center:
            if (self.direction == -1 and self.x <= center_x) or (self.direction == 1 and self.x >= center_x):
                self.current_frame_index = (self.current_frame_index + 1) % len(self.SPRITE_FRAMES)
                self.passed_center = True
        else:
            if (self.direction == -1 and self.x > center_x) or (self.direction == 1 and self.x < center_x):
                self.passed_center = False

    def _check_edges(self, mario, luigi):
        """Check conveyors edges to hand package to the player or make it fall."""
        # MARIO side (right)
        # note: conveyor_index odd means package heading right side
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
        """Draw current package frame if active."""
        if not self.active:
            return
        u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]
        pyxel.blt(self.x, self.y, 0, u, v, w, h, 0)
