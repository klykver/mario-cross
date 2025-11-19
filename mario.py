import pyxel


class Mario:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.floor = 0
        self.max_floor = 5
        self.state = 'idle'  #initialy mario wil be idle

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position x must be an integer")
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position y must be an integer")
        self.__y = value

    @property
    def floor(self) -> int:
        return self.__floor

    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Floor must be an integer")
        elif not (0 <= value <= self.max_floor):
            raise ValueError(f"Floor must be between 0 and {self.max_floor}")
        else:
            self.__floor = value

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str):
        if value not in ('idle', 'moving', 'busy'):
            raise ValueError(f"Invalid state {value}")
        self.__state = value

    def update(self):
        # We will add movement logic here later
        pass

    def draw(self):
        if self.state == 'idle':
            # We use % 30 to create a repeating cycle of 30 frames
            # If we are in the first half of the cycle (0-14)...
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 0, 17, 30)
            else:
                # ...otherwise (we are in the second half, 15-29)
                pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30)

        else:
            # If state is not 'idle' (e.g., 'moving' or 'busy')
            # just draw the main frame all the time.
            pyxel.blt(self.x, self.y, 0, 24, 0, 24, 30)

