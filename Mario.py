import pyxel


class Mario:
    def __init__(self, x: int, y: int, max_floor: int):
        self._x = x
        self._y = y
        self._floor = 0
        self._max_floor = max_floor
        self._state = 'idle'  #initialy mario wil be idle

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position x must be an integer")
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position y must be an integer")
        self._y = value

    @property
    def floor(self) -> int:
        return self._floor

    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Floor must be an integer")
        elif not (0 <= value <= self._max_floor):
            raise ValueError(f"Floor must be between 0 and {self._max_floor}")
        else:
            self._floor = value

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str):
        if value not in ('idle', 'moving', 'busy'):
            raise ValueError(f"Invalid state {value}")
        self._state = value

    def update(self):
        # We will add movement logic here later
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 2, 0, 16, 28)
