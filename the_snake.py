"""Модуль содержит классы игровых объектов.

И функцию для обработки нажатия клавиш.
"""


from random import choice, randrange

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_OF_SCREEN = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption("Змейка")

clock = pg.time.Clock()


class GameObject:
    """Базовый класс для будущих игровых объектов."""

    def __init__(self, color=None):
        """Инициализирует базовые атрибуты позиция и цвет."""
        self.position = CENTER_OF_SCREEN
        self.body_color = color

    def draw(self):
        """Абстрактный метод для переопределения в дочерних классах.

        Используется для отрисовки объекта на экране.
        """
        raise NotImplementedError(
            f'Метод отсутствует в классе {self.__class__.__name__}. '
            'Необходимо определить в дочернем классе.')


class Apple(GameObject):
    """Метод описывает яблоко и действия с ним."""

    def __init__(self, color=APPLE_COLOR):
        """Инициализирует атрибуты яблока.

        Задаёт цвет яблока
        и вызывает метод randomize_position
        для установки начального положения яблока.
        """
        super().__init__(color)

        self.randomize_position()

    def randomize_position(self, occupied_position=[CENTER_OF_SCREEN]):
        """Устанавливает случайное положение яблока.

        Координаты в пределах игрового поля.
        """
        while self.position in occupied_position:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Метод описывает змейку и её поведение."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализирует начальное положение змейки.

        Задаёт её длину, начальное положение, направление движения,
        новое направление движения, цвет, последний элемент.
        """
        super().__init__(color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки.

        Добавляет новую голову в начало списка
        и удаляет последний элемент, если длина не увеличилась.
        """
        width_head_position, height_head_position = self.get_head_position()
        x_direction, y_direction = self.direction

        width_head_position = (width_head_position
                               + (x_direction * GRID_SIZE)) % SCREEN_WIDTH
        height_head_position = (height_head_position
                                + (y_direction * GRID_SIZE)) % SCREEN_HEIGHT

        self.positions.insert(0, (width_head_position, height_head_position))

        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш.

    Изменяет направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описывает цикл игры Змейка."""
    pg.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position()

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == "__main__":
    main()
