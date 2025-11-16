class Package:
    def __init__(self, x: int, y: int, conveyor_index: int):
        self._x = x
        self._y = y
        self._conveyor_index = conveyor_index  # Which conveyor it's on

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
    def conveyor_index(self) -> int:
        return self._conveyor_index

    @conveyor_index.setter
    def conveyor_index(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Conveyor index must be an integer")
        elif value < 0:
            raise ValueError("Conveyor index cannot be negative")
        else:
            self._conveyor_index = value
            # When a package moves to a new conveyor,
            # its x/y position should be updated here