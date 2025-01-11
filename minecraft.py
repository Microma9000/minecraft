import pygame
import sys
import random
import time
# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1366, 768#разрешение
BACKGROUND_COLOR = (50, 205, 50)  # Небесно-голубой цвет
BLOCK_COLOR = (139, 69, 19)  # Коричневый цвет для блоков дерево
#BLOCK_COLOR2 = (128, 128, 128)  # Коричневый цвет для блоков камень
PLAYER_COLOR = (0, 250, 154)  # Зеленый цвет для игрока
BLOCK_SIZE = 50
REGENERATION_INTERVAL = 5000  # Интервал в миллисекундах (5 секунды)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft на Python")

# Позиция "персонажа"
player_pos = [WIDTH // 2, HEIGHT // 2]  # Начальная позиция по центру экрана

# Инвентарь
resources = {'wood':0}
resources = {'stone':0}
resources = {'sand':0}
resources = {'land':0}
# Список блоков на экране
blocks = [(100, 100), (200, 100)]  # Пример блоков (координаты)

def gather_resource(resource_type):
    """Функция для добычи ресурсов."""
    if resource_type in resources:
        resources[resource_type] += 1
    else:
        resources[resource_type] = 1

def open_inventory():
    """Функция для открытия инвентаря."""
    print("Инвентарь:", resources)

def regenerate_resources():
    """Функция для добавления новых блоков на экран через определенные промежутки времени."""
    new_block_x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
    new_block_y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
    new_block_position = (new_block_x, new_block_y)
    
    # Проверяем, не занят ли это место другим блоком
    if new_block_position not in blocks:
        blocks.append(new_block_position)
    else:
        print("Блок уже существует в этой позиции:", new_block_position)

# Устанавливаем таймер для регенерации ресурсов
pygame.time.set_timer(pygame.USEREVENT, REGENERATION_INTERVAL)

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Проверка на событие регенерации
        if event.type == pygame.USEREVENT:
            regenerate_resources()

        # Обработка клика мыши для добычи ресурсов и строительства
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:  # Левый клик
                for block in blocks:
                    if block[0] <= mouse_x <= block[0] + BLOCK_SIZE and block[1] <= mouse_y <= block[1] + BLOCK_SIZE:
                        gather_resource('wood')  # Добываем 'дерево'
                        blocks.remove(block)  # Удаляем блок из списка
                        break
                else:
                    if resources['wood'] > 0:  # Если есть ресурсы
                        new_block_position = (mouse_x // BLOCK_SIZE * BLOCK_SIZE, mouse_y // BLOCK_SIZE * BLOCK_SIZE)
                        blocks.append(new_block_position)  # Добавляем новый блок
                        resources['wood'] -= 1  # Уменьшаем количество ресурсов

    # Обработка клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5  # Двигаемся влево
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5  # Двигаемся вправо
    if keys[pygame.K_UP]:
        player_pos[1] -= 5  # Двигаемся вверх
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5  # Двигаемся вниз

    # Ограничение движения внутри окна
    player_pos[0] = max(0, min(player_pos[0], WIDTH - BLOCK_SIZE))
    player_pos[1] = max(0, min(player_pos[1], HEIGHT - BLOCK_SIZE))

    # Открытие инвентаря по нажатию 'I'
    if keys[pygame.K_i]:
        open_inventory()

    # Заливка фона
    screen.fill(BACKGROUND_COLOR)

    # Рисуем блоки
    for block in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))


    # Рисуем "игрока"
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Обновление экрана
    pygame.display.flip()
