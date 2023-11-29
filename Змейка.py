import pygame
import sys
import random
import time


GAME_TITLE="Snake" #название
WIGHT, HIGHT = 800, 800 #размер окна
BLOCK_SIZE = 20 #размер блока
WALL_BLOCKS = 1 #количество блоков на стенках
SNAKE_ICON = "snake.png" #иконка игры
START_GAME_SPEED = 5 #кол-во кадров за секунду, скорость змеи
SPEED_UP = 1.1 #множитель скорости
MAX_SPEED = 13
BACKGROUND_COLOR = (193,154,107) #Задний фон
WALL_COLOR = (77,34,14) #цвет стенок
SIZE_X = WIGHT//BLOCK_SIZE - WALL_BLOCKS*2 #Количество блоков в ширину
SIZE_Y = HIGHT//BLOCK_SIZE - WALL_BLOCKS*2 #Кол-во блоков в высоту


START_APPLES = 10 # кол-во яблок на поле
#Цвет фруктов
APPLE_COLOR = (123, 0, 28) #яблоко
ORANGE_COLOR = (210,105,30) #апельсин
MARAK_COLOR = (43, 0, 61) #маракуя
PAPAYA_COLOR= (31, 97,53) #папайя


FRUIT_RADIUS = BLOCK_SIZE // 1 #Радиус яблок, чем меньше радиус, тем идеальнее круг

START_SNAKE_LENGHT = 1 #стартовая длина змеи
SNAKE_COLOR = (40,199,119) #цвет змеи
SNAKE_RADIUS = BLOCK_SIZE // 3 #радуис змеи, то насколько круглые её фрагменты
EYE_COLOR = (0,0,0)
EYE_SIZE = BLOCK_SIZE//5

TEXT_COLOR = (255, 255, 255) #цвет текста
TEXT_SIZE = int(WALL_BLOCKS * BLOCK_SIZE * 0.75) #размер текста
PAUSE_COLOR = (121,85,61)



def main():
    screen, clock = initialization_pygame() #инициализация pygame
    game_state = initialization_game_state() #инициализация состояния игры, где находится змейка, где находятся яблоки, какое у нас количество очков
    while game_state["program_running"]:
        clock.tick(game_state["game_speed"]) #Указываем с какой скоростью работают часы
        #считываем все события
        events = get_events() #все полученные события хранятся в events
        update_game_state(events, game_state) #функция обновления состояния игры, изменение game_state изходя из событий
        update_screen(screen, game_state) #функция обновления экрана, обязательно добавляем сюда game_state потому что все изменения,
        #происходящие на экране, они очевидно будут влиять и на изображение на экране
    perform_shutdown() #выход из игры, закрытие проги

def initialization_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIGHT, HIGHT)) #создание экрана
    icon = pygame.image.load(SNAKE_ICON) #создание иконки
    pygame.display.set_icon(icon) #вывод иконки
    pygame.display.set_caption(GAME_TITLE) #вывод названия
    clock = pygame.time.Clock()
    return screen, clock

def initialization_game_state():
    game_state = {
        "program_running": True,
        "game_running": False,
        "game_paused": False,
        "game_speed": START_GAME_SPEED,
        "score": 0
    }
    return game_state

def get_events():
    events=[]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append("quit")
        elif event.type == pygame.KEYDOWN: #тип события, когда мы нажимаем на любую кнопку
            #стрелки wsad
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                events.append("up")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                events.append("down")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                events.append("left")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                events.append("right")
            elif event.key == pygame.K_SPACE:
                events.append("space")
            elif event.key == pygame.K_RETURN:
                events.append("enter")
            elif event.key == pygame.K_ESCAPE:
                events.append("escape")


    return events

def update_game_state(events, game_state): #обновление состояния игры
    check_key_presses(events, game_state) #проверка использованны= кнопок
    if game_state["game_paused"]:
        return
    if game_state["game_running"]:
        move_snake(game_state)
        check_collisions(game_state) #Проверка столкновений
        check_fruits_consumption(game_state)#Проверка на сожранные яблоки

def check_key_presses(events, game_state): #Проверка использованных кнопо
    #Два способа выйти из игры
    if "quit" in events:
        game_state["program_running"] = False
    elif not game_state["game_running"]:
        if "escape" in events:
            game_state["program_running"] = False
        elif "enter" in events:
            initialization_new_game(game_state)
            game_state["game_running"] = True
    elif game_state["game_paused"]:
        if "escape" in events:
            game_state["game_paused"] = False
            game_state["game_running"] = False
        elif "space" in events:
            game_state["game_paused"] = False
    else:
        if "escape" in events:
            game_state["game_running"] = False
        if "space" in events:  # Теперь змейка будет продолжать движение после паузы.
            game_state["game_paused"] = True
        if "up" in events and game_state["direction"] != (0, 1):  # добавил проверку, чтобы не разворачиваться на 180 градусов
            game_state["direction"] = (0, -1)
        if "down" in events and game_state["direction"] != (0, -1):  # то же для других направлений
            game_state["direction"] = (0, 1)
        if "left" in events and game_state["direction"] != (1, 0):
            game_state["direction"] = (-1, 0)
        if "right" in events and game_state["direction"] != (-1, 0):
            game_state["direction"] = (1, 0)

def move_snake(game_state): #движение змеи

    x = game_state["snake"][0][0] + game_state["direction"][0]
    y = game_state["snake"][0][1] + game_state["direction"][1]
    game_state["snake"].insert(0, (x,y))

def check_collisions(game_state): #Проверка столкновений

    x,y = game_state["snake"][0]
    if x <0 or y<0 or x>= SIZE_X or y >=SIZE_Y:
        game_state["game_running"] = False
    if len(game_state["snake"]) > len(set(game_state["snake"])):
        game_state["game_running"] = False

def change_speed(game_state, score): #изменение скорости, максимальная скорость
    min_score = 50
    max_score = 70
    if score >= 50 and score <=250 and game_state["game_speed"]<=MAX_SPEED:
        game_state["game_speed"] = round(game_state["game_speed"] * SPEED_UP)

def check_fruits_consumption(game_state):
    #Проверка на сожранные яблоки
    fruits_eaten = 0
    for fruit in game_state["fruits"]:
        fruit_position = fruit[:2]
        if fruit_position == game_state["snake"][0]:
            game_state["fruits"].remove(fruit)
            fruits_eaten +=1
            place_fruits(1, game_state)
            if fruit[2] == "apple":
                game_state["score"] +=20 #20 очков за 1 ялоко
            elif fruit[2] == "orange":
                game_state["score"] -=10 #10 очков за 1 апельсин
            elif fruit[2] == "passion_fruit":
                game_state["score"] +=50 #50 очков за 1 маракую
            elif fruit[2] == "papaya":
                game_state["score"] +=15 #15 очков за 1 папайю
            change_speed(game_state, game_state["score"])
    if fruits_eaten ==0:
        game_state["snake"].pop()

def initialization_new_game(game_state):
    # пауза или нет?
    game_state["game_paused"] = False
    #Сколько очков?
    game_state["score"] = 0
    #Скорость игры
    game_state["game_speed"] = START_GAME_SPEED
    #положение змейки
    game_state["snake"]=[]
    place_snake(START_SNAKE_LENGHT, game_state)
    #положение яблок
    game_state["fruits"]=[]
    place_fruits(START_APPLES, game_state)
    #game_state["apple_colors"] = [APPLE_COLORS, ORANGE_COLOR, MARAK_COLOR, PAPAYA_COLOR]


    #направление движения змейки
    game_state["direction"] = (1,0) #(0,1) - змейка движется вниз, (1,0) - вправо, (-1,0) - влево , (0,-1) - вверх

def place_snake(lenght, game_state):
    x = SIZE_X//2
    y = SIZE_Y//2
    game_state["snake"].append((x,y))
    for i in range(1, lenght):
        game_state["snake"].append((x-i,y))

def place_fruits(fruits, game_state):
    for i in range(fruits):
        x = random.randint(0, SIZE_X-1)
        y = random.randint(0, SIZE_Y-1)
        while (x,y) in game_state["fruits"] or (x, y) in game_state["snake"]:
            x = random.randint(0, SIZE_X-1)
            y = random.randint(0, SIZE_Y-1)
        fruit = random.choice(["apple", "orange", "passion_fruit", "papaya"])
        game_state["fruits"].append((x,y, fruit))

def update_screen(screen, game_state):
    screen.fill(BACKGROUND_COLOR)
    if not game_state["game_running"]:
        print_new_game_message(screen)
    elif game_state["game_paused"]:
        print_game_paused_message(screen)
    else:
        draw_fruits(screen, game_state["fruits"])

        draw_snake(screen, game_state["snake"], game_state["direction"])
    draw_walls(screen)
    print_score(screen, game_state["score"])
    pygame.display.flip()

def print_new_game_message(screen):
    font = pygame.font.SysFont("Courier New", TEXT_SIZE*2, bold=True)
    text1 = font.render("Press ENTER to start new game", True, TEXT_COLOR)
    text2 = font.render("Press ESCAPE to quit", True, TEXT_COLOR)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text1_rect.center = (WIGHT //2, HIGHT//1.2 + BLOCK_SIZE//2)
    text2_rect.center = (WIGHT //2, HIGHT//1.1 + BLOCK_SIZE//2)
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

def draw_fruits(screen, fruits):
    fruits_color = {
        "apple": APPLE_COLOR,
        "orange": ORANGE_COLOR,
        "passion_fruit": MARAK_COLOR,
        "papaya": PAPAYA_COLOR
    }
    for fruit in fruits:
        x = fruit[0] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        y = fruit[1] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        rect = ((x, y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, fruits_color[fruit[2]], rect, border_radius=FRUIT_RADIUS)

def draw_snake(screen, snake, direction):
    for segment in snake:
        x = segment[0] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        y = segment[1] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        rect = ((x,y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, rect, border_radius = SNAKE_RADIUS)
    draw_snake_eyes(screen, snake[0], direction)

def draw_snake_eyes(screen, head, direction):
    wall_size = WALL_BLOCKS * BLOCK_SIZE
    eye_offers = BLOCK_SIZE // 9
    x, y = direction[0], direction[1]
    if x == -1 or y== -1:
        coord_x = head[0]*BLOCK_SIZE + wall_size + eye_offers
        coord_y = head[1]*BLOCK_SIZE + wall_size + eye_offers
        center = (coord_x, coord_y)
        pygame.draw.circle(screen, EYE_COLOR, center, EYE_SIZE)
    if x == -1 or y== 1:
        coord_x = head[0]*BLOCK_SIZE + wall_size + eye_offers
        coord_y = head[1]*BLOCK_SIZE + wall_size + (BLOCK_SIZE - eye_offers)
        center = (coord_x, coord_y)
        pygame.draw.circle(screen, EYE_COLOR, center, EYE_SIZE)
    if x == 1 or y== -1:
        coord_x = head[0]*BLOCK_SIZE + wall_size + (BLOCK_SIZE - eye_offers)
        coord_y = head[1]*BLOCK_SIZE + wall_size + eye_offers
        center = (coord_x, coord_y)
        pygame.draw.circle(screen, EYE_COLOR, center, EYE_SIZE)
    if x == 1 or y== 1:
        coord_x = head[0]*BLOCK_SIZE + wall_size + (BLOCK_SIZE - eye_offers)
        coord_y = head[1]*BLOCK_SIZE + wall_size + (BLOCK_SIZE - eye_offers)
        center = (coord_x, coord_y)
        pygame.draw.circle(screen, EYE_COLOR, center, EYE_SIZE)

def draw_walls(screen):
    wall_size = WALL_BLOCKS * BLOCK_SIZE
    pygame.draw.rect(screen, WALL_COLOR, ((0,0), (WIGHT, wall_size)))
    pygame.draw.rect(screen, WALL_COLOR, ((0,0), (wall_size, HIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((0,HIGHT - wall_size), (WIGHT, HIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((WIGHT -wall_size,0), (WIGHT, HIGHT)))

def print_score(screen, score):
    font = pygame.font.SysFont("Courier New", TEXT_SIZE, bold=True)
    text = font.render("Your score: " + str(score), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (WALL_BLOCKS * BLOCK_SIZE, 0)
    screen.blit(text, text_rect)

def print_game_paused_message(screen):
    screen.fill(PAUSE_COLOR)
    img = pygame.image.load("game_paus.jpg").convert()
    img = pygame.transform.scale(img, (WIGHT, HIGHT))

    font = pygame.font.SysFont("Courier New", TEXT_SIZE*2, bold=True)
    text1 = font.render("Press SPACE to continue", True, TEXT_COLOR)
    text2 = font.render("Press ESCAPE to start new game", True, TEXT_COLOR)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text1_rect.center = (WIGHT //2, HIGHT//1.2 + BLOCK_SIZE//2)
    text2_rect.center = (WIGHT //2, HIGHT//1.1 + BLOCK_SIZE//2)

    screen.blit(img, (0, 0))
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

def perform_shutdown():
    pygame.quit()
    sys.exit()

main()
