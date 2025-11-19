class Luigi:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.floor = 0
        self.max_floor = 5
        self.state = 'idle'  # 'idle', 'moving', 'busy'

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