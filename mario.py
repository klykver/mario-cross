import pyxel


class Mario:
    def __init__(self, x: int, y: int, max_floor: int):
        self.x = x
        self.y = y
        self.max_floor = max_floor
        self.floor = 0
        self.state = 'idle'  #initialy mario wil be idle
        self.floor_y_position = [289, 240]
        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 4

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
        if value not in ('idle', 'moving', 'busy', 'climbing'):
            raise ValueError(f"Invalid state {value}")
        self.__state = value

    def update(self):
        # 1. ЯКЩО МИ СТОЇМО (IDLE) -> ЧЕКАЄМО КНОПКУ
        if self.state == 'idle':
            if pyxel.btnp(pyxel.KEY_UP):
                # Якщо не на даху -> ліземо вгору
                if self.floor < self.max_floor:
                    self.state = 'climbing'
                    # Наша ціль - Y наступного поверху (+1)
                    self.target_y = self.floor_y_position[self.floor + 1]


            elif pyxel.btnp(pyxel.KEY_DOWN):
                # Якщо не на підлозі -> ліземо вниз
                if self.floor > 0:
                    self.state = 'climbing'
                    # Наша ціль - Y попереднього поверху (-1)
                    self.target_y = self.floor_y_position[self.floor - 1]


        # 2. ЯКЩО МИ ЛІЗЕМО (CLIMBING) -> РУХАЄМОСЯ ДО ЦІЛІ
        elif self.state == 'climbing':

            # Якщо ми нижче цілі -> рухаємося вгору (зменшуємо Y)
            if self.y > self.target_y:
                self.y -= self.climb_speed
                # Щоб не проскочити
                if self.y < self.target_y:
                    self.y = self.target_y


            # Якщо ми вище цілі -> рухаємося вниз (збільшуємо Y)
            elif self.y < self.target_y:
                self.y += self.climb_speed
                if self.y > self.target_y:
                    self.y = self.target_y

            # 3. ПЕРЕВІРКА ФІНІШУ
            if self.y == self.target_y:
                self.state = 'idle'
                # Оновлюємо номер поверху (шукаємо індекс по Y)
                if self.y in self.floor_y_position:
                    self.floor = self.floor_y_position.index(self.y)

    def draw(self):
        # 1. (IDLE)
        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 0, 17, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 1, 0, 17, 30, 0)

                # 2.(CLIMBING)
        elif self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 55, 0, 15, 28, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 80, 0, 15, 28, 0)
