import pyxel
class Luigi:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.floor_y_position = [210, 162, 114] #+33
        self.max_floor = len(self.floor_y_position) - 1
        self.floor = 0
        self.state = 'idle'  # 'idle', 'moving', 'busy'
        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 3

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
            print(f"Invalid state: {value}")
        else:
            self.__state = value

    def update(self):
        # 1. ЯКЩО МИ СТОЇМО (IDLE) -> ЧЕКАЄМО КНОПКУ
        if self.state == 'idle':
            if pyxel.btnp(pyxel.KEY_W):
                # БЕЗПЕЧНА ПЕРЕВІРКА:
                # Чи є наступний поверх у нашому списку координат?
                if self.floor < self.max_floor:
                    self.state = 'climbing'
                    self.target_y = self.floor_y_position[self.floor + 1]

            elif pyxel.btnp(pyxel.KEY_S):
                # БЕЗПЕЧНА ПЕРЕВІРКА:
                # Чи не впадемо ми нижче нуля?
                if self.floor > 0:
                    self.state = 'climbing'
                    self.target_y = self.floor_y_position[self.floor - 1]

        # 2. ЯКЩО МИ ЛІЗЕМО (CLIMBING)
        elif self.state == 'climbing':
            if self.y > self.target_y:
                self.y -= self.climb_speed
                if self.y < self.target_y:
                    self.y = self.target_y

            elif self.y < self.target_y:
                self.y += self.climb_speed
                if self.y > self.target_y:
                    self.y = self.target_y

            # 3. ПЕРЕВІРКА ФІНІШУ
            if self.y == self.target_y:
                self.state = 'idle'
                # Оновлюємо поверх ТІЛЬКИ якщо такий Y існує
                if self.y in self.floor_y_position:
                    self.floor = self.floor_y_position.index(self.y)
                else:
                    # Якщо раптом координата не знайдена (глюк),
                    # просто нічого не робимо, щоб не було крашу
                    print("Error: Luigi reached unknown height!")

    def draw(self):
        # (Твій код малювання без змін)
        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 32, 14, 34, 0)

            else:
                pyxel.blt(self.x, self.y, 0, 0, 32, 16, 34, 0)
        elif self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 72,32, 15, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 48, 32, 15, 33, 0)
