import pyxel


class Package:
    def __init__(self, floor_y_positions: list, start_floor: int = 0):
        # Приймаємо список висот (має бути той самий, що у Маріо)
        self.floor_y_position = floor_y_positions

        self._conveyor_index = start_floor

        # Визначаємо Y (безпечно беремо зі списку)
        if self._conveyor_index < len(self.floor_y_position):
            self._y = self.floor_y_position[self._conveyor_index]
        else:
            self._y = 0

            # --- НАПРЯМОК І СТАРТ X ---
        # Парні (0, 2) -> ВПРАВО. Непарні (1) -> ВЛІВО.
        if self._conveyor_index % 2 == 0:
            self._direction = 1
            self._x = 40  # Зліва (біля труби)
        else:
            self._direction = -1
            self._x = 280  # Справа (підлаштуй під ширину свого екрану 386)

        self.active = True
        self.state = 'moving'  # 'moving', 'falling'
        self.speed = 1.5

        # --- СИСТЕМА КАДРІВ (6 ШТУК) ---
        # Тут треба вписати координати для всіх 6 стадій торта:
        # (u, v, w, h)
        self.SPRITE_FRAMES = [
            (8, 142, 23, 7),  # 0: Тісто (Поверх 0, початок)
            (8, 142, 23, 7),  # 1: Корж (Поверх 0, після центру) - ЗМІНИ ЦЕ

            (8, 142, 23, 7),  # 2: Торт (Поверх 1, початок) - ЗМІНИ ЦЕ
            (8, 142, 23, 7),  # 3: Торт з кремом (Поверх 1, після центру) - ЗМІНИ ЦЕ

            (8, 142, 23, 7),  # 4: Коробка (Поверх 2, початок) - ЗМІНИ ЦЕ
            (8, 142, 23, 7)  # 5: Запаковано (Поверх 2, після центру) - ЗМІНИ ЦЕ
        ]

        self.current_frame_index = 0

    # --- PROPERTIES ---
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def conveyor_index(self) -> int:
        return self._conveyor_index

    # --- UPDATE ---
    def update(self, mario):
        if not self.active:
            return

        # 1. РУХ
        if self.state == 'moving':
            self._x += self.speed * self._direction

            # --- ЛОГІКА ЗМІНИ КАДРУ (0-5) ---
            # Базовий індекс для поверху (Поверх 0->0, Поверх 1->2, Поверх 2->4)
            base_frame = self._conveyor_index * 2

            # Центр екрану (приблизно 386 / 2 = 193)
            center_x = 193

            passed_center = False
            if self._direction == 1 and self._x > center_x:
                passed_center = True
            elif self._direction == -1 and self._x < center_x:
                passed_center = True

            # Якщо проїхали центр, додаємо +1 до індексу кадру
            if passed_center:
                self.current_frame_index = base_frame + 1
            else:
                self.current_frame_index = base_frame

            # --- ПЕРЕВІРКА КРАЇВ (ВЗАЄМОДІЯ) ---
            # Край МАРІО (Права сторона)
            if self._direction == 1 and self._x > 250:  # Підлаштуй цю цифру під кінець ленти
                if mario.floor == self.conveyor_index and mario.state != 'busy':
                    self.transfer_up(mario)
                else:
                    self.state = 'falling'


        # 2. ПАДІННЯ
        elif self.state == 'falling':
            self._y += 4
            if self._y > 360:  # Низ екрану
                self.active = False
                # Тут можна віднімати життя

    def transfer_up(self, character):
        """Переміщення на поверх вище"""
        # Тут можна додати: character.state = 'busy' (щоб він підняв руки)

        self._conveyor_index += 1

        # Перевірка на вантажівку (якщо поверхи закінчились)
        if self._conveyor_index >= len(self.floor_y_position):
            self.active = False  # Успіх!
            return

        # Нова висота
        self._y = self.floor_y_position[self._conveyor_index]

        # Змінюємо напрямок
        self._direction *= -1

        # Ставимо на початок нової стрічки
        if self._direction == 1:
            self._x = 40
        else:
            self._x = 280

    # --- DRAW ---
    def draw(self):
        if not self.active:
            return

            # Перевіряємо, чи індекс кадру правильний
        if 0 <= self.current_frame_index < len(self.SPRITE_FRAMES):
            u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]

            # Малюємо пакунок
            # colkey=0 означає, що чорний колір буде прозорим
            pyxel.blt(self._x, self._y, 0, u, v, w, h, 0) # 0 в кінці - прозорий колір