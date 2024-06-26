"""Модуль содержит классы игровых объектов.

И функцию для обработки нажатия клавиш.
"""


from random import randrange

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для будущих игровых объектов."""

    def __init__(self):
        """Инициализирует базовые атрибуты позиция и цвет."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод для переопределения в дочерних классах.

        Используется для отрисовки объекта на экране.
        """
        pass


class Apple(GameObject):
    """Метод описывает яблоко и действия с ним."""

    def __init__(self):
        """Инициализирует атрибуты яблока.

        Задаёт цвет яблока
        и вызывает метод randomize_position
        для установки начального положения яблока.
        """
        super().__init__()
        self.body_color = APPLE_COLOR

        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока.

        Координаты в пределах игрового поля.
        """
        width_position = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        height_position = randrange(0, SCREEN_HEIGHT, GRID_SIZE)

        self.position = (width_position, height_position)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Метод описывает змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное положение змейки.

        Задаёт её длину, начальное положение, направление движения,
        новое направление движения, цвет, последний элемент.
        """
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
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

        if self.direction == UP:
            height_head_position -= GRID_SIZE
            if height_head_position < 0:
                height_head_position = SCREEN_HEIGHT - GRID_SIZE
        elif self.direction == DOWN:
            height_head_position += GRID_SIZE
            if height_head_position == SCREEN_HEIGHT:
                height_head_position = 0
        elif self.direction == LEFT:
            width_head_position -= GRID_SIZE
            if width_head_position < 0:
                width_head_position = SCREEN_WIDTH - GRID_SIZE
        elif self.direction == RIGHT:
            width_head_position += GRID_SIZE
            if width_head_position == SCREEN_WIDTH:
                width_head_position = 0

        new_head_position = (width_head_position, height_head_position)
        self.positions.insert(0, new_head_position)

        if self.length < len(self.positions):
            self.last = self.positions.pop(-1)

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        head_position = self.positions[0]
        return head_position

    def reset(self):
        """Сбрасывает змейку в начальное состояние.

        Срабатывает при столкновении головы и тела.
        """
        if self.get_head_position() in self.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.__init__()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш.

    Изменяет направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описывает цикл игры Змейка."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        while apple.position in snake.positions[1:]:
            apple.randomize_position()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.reset()

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
