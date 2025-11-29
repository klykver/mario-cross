import pyxel


class Mario:
    def __init__(self, x: int, y: int):  # max_floor тут можна і прибрати, але хай буде для сумісності
        self.x = x
        self.y = y

        # --- НАЛАШТУВАННЯ ПОВЕРХІВ ---
        # 1. Задаємо координати
        self.floor_y_position = [243, 194, 148]

        # 2. АВТОМАТИЧНО вираховуємо максимальний поверх
        # Якщо у списку 3 числа, то індекси: 0, 1, 2.
        # len() поверне 3, тому віднімаємо 1. Макс поверх = 2.
        self.max_floor = len(self.floor_y_position) - 1

        self.floor = 0
        self.state = 'idle'

        # Ставимо Маріо на старт
        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 3

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = value

    @property
    def floor(self) -> int:
        return self.__floor

    @floor.setter
    def floor(self, value: int):
        # Безпечний сеттер: ігнорує неправильні значення, замість помилки
        if 0 <= value <= self.max_floor:
            self.__floor = value
        else:
            print(f"Warning: Tried to set invalid floor {value}")

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
            if pyxel.btnp(pyxel.KEY_UP):
                # БЕЗПЕЧНА ПЕРЕВІРКА:
                # Чи є наступний поверх у нашому списку координат?
                if self.floor < self.max_floor:
                    self.state = 'climbing'
                    self.target_y = self.floor_y_position[self.floor + 1]

            elif pyxel.btnp(pyxel.KEY_DOWN):
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
                    print("Error: Mario reached unknown height!")

    def draw(self):
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
