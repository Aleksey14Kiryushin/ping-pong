# Добавить возможность играть с ботом
# Одна картинка с победой слева, для игрока справа проигрыш
# Добавить Menu
# Таблицу лидеров
# Жизни

from pygame import *
from random import *
from time import time as now_time
import os

clock = time.Clock()

# Place
x = 200
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# Object
class Character(sprite.Sprite):
    def __init__(self, width, height, x, y, picture, speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.picture = picture
        self.speed = speed
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def set_picture(self):
        self.image = transform.scale(image.load("break_heart.png"), (self.width, self.height))
# Player
class Player(Character):
    def __init__(self, width, height, x, y, picture, speed, skipped, count, amount_of_lives=3):
        super().__init__(width, height, x, y, picture[0], speed)

        self.picture = picture
        self.counter = 0

        self.x_speed = speed
        self.y_speed = speed 

        self.skipped = skipped
        self.count = count

        self.amount_of_lives = amount_of_lives

    def update(self):

        key_pressed = key.get_pressed()
        
        if key_pressed[K_UP] and self.rect.y > 0: 
            self.rect.y -= self.y_speed

        if key_pressed[K_DOWN] and self.rect.y < 700:
            self.rect.y += self.y_speed

class Enemy(Character):
    def __init__(self, width, height, x, y, picture, speed, skipped, count, amount_of_lives=3):
        super().__init__(width, height, x, y, picture[0], speed)

        self.picture = picture
        self.counter = 0

        self.x_speed = speed
        self.y_speed = speed 

        self.skipped = skipped
        self.count = count

        self.amount_of_lives = amount_of_lives

        self.returning = True

    def update(self):

        key_pressed = key.get_pressed()
        
        if key_pressed[K_w] and self.rect.y > 0: 
            self.rect.y -= self.y_speed

        if key_pressed[K_s] and self.rect.y < 700:
            self.rect.y += self.y_speed
# простой уровень
    def update_bot(self):
        if self.rect.y >= 775:
            self.returning = False

        if self.rect.y <= 25:
            self.returning = True

        if self.returning:
            self.rect.y += self.speed

        if not self.returning:
            self.rect.y -= self.speed 
#  невозможный уровень
    def extra_bot(self):
        self.rect.y = puck.rect.y

class Puck(Character):
    def __init__(self, width, height, x, y, picture, speed):
        super().__init__(width, height, x, y, picture[0], speed)
    
        self.speed_x = speed 

        self.speed_y = speed

        self.returning_back = True

        self.returning_top = True
    def update(self):
        # Касание левой и правой стены:
        self.rect.x += self.speed_x 

        # if self.rect.x >= 750:
        #     self.returning_back = False

        # if self.rect.x <= 25:
        #     self.returning_back = True

        # if self.returning_back:
        #     self.rect.x += self.speed_x 
            
        # if not self.returning_back:        
        #     self.rect.x -= self.speed_x 
        
        # Касание верхней и нижней стены:
        if self.rect.y >= 775:
            self.returning_top = False

        if self.rect.y <= 25:
            self.returning_top = True

        if self.returning_top:
            self.rect.y += self.speed_y 

        if not self.returning_top:
            self.rect.y -= self.speed_y 

        # Столкновение с игроком
        if sprite.collide_rect(player_1st, self) or sprite.collide_rect(player_2nd, self):
            self.speed_x *= -1
            
    def random_position(self):
        self.rect.y = randint(100, 700)
        self.rect.x = randint(300,500)

# Window
global_height = 800
global_width = 800
window = display.set_mode((global_width,global_height))

display.set_caption("Ping-Pong")
display.set_icon(image.load("background.jpg"))
background = transform.scale(image.load("background.jpg"), (global_height, global_width))

# Players
pictures_players = ["reflector.png"]

player_1st = Player(100, 100, 0, 400, pictures_players, 10, 0, 0)

player_2nd = Enemy(100, 100, 700, 400, pictures_players, 10, 0, 0)

# Puck
picture_puck = ["puck.png"]

puck = Puck(50, 50, 400, 500, picture_puck, 3)

# Hearts
heart_1st = Character(40, 40, 50, 30, "heart.png", 0)
heart_2nd = Character(40, 40, 100, 30, "heart.png", 0)
heart_3rd = Character(40, 40, 150, 30, "heart.png", 0)

heart_4th = Character(40, 40, 650, 30, "heart.png", 0)
heart_5th = Character(40, 40, 700, 30, "heart.png", 0)
heart_6th = Character(40, 40, 750, 30, "heart.png", 0)

hearts_group = sprite.Group()
hearts_group.add(heart_1st)
hearts_group.add(heart_2nd)
hearts_group.add(heart_3rd)
hearts_group.add(heart_4th)
hearts_group.add(heart_5th)
hearts_group.add(heart_6th)

# Font
font.init()
font_type = font.Font(None,36)

# Variables
game_Play = True
stopping = False
global_begin_time = now_time()

while game_Play:

    window.blit(background, (0,0))

    for event_get in event.get():
        if event_get.type == QUIT:
            game_Play = False

    if puck.rect.x <= 10 or puck.rect.x >= 785:
        if puck.rect.x <= 10:
            print("1ST LOST!")
            background_left = transform.scale(image.load("lose.jpg"), (global_height/2, global_width/2))
            background_right = transform.scale(image.load("win.jpg"), (global_height/2, global_width/2))
            player_1st.amount_of_lives -= 1

            # Отрисовка сердечек
            if player_1st.amount_of_lives == 2:
                heart_1st.set_picture()

            if player_1st.amount_of_lives == 1:
                heart_2nd.set_picture()

        if puck.rect.x >= 785:
            print("2RD LOST!")
            background_left = transform.scale(image.load("win.jpg"), (global_height/2, global_width/2))
            background_right = transform.scale(image.load("lose.jpg"), (global_height/2, global_width/2))
            player_2nd.amount_of_lives -= 1
        
            if player_2nd.amount_of_lives == 2:
                heart_4th.set_picture()

            if player_2nd.amount_of_lives == 1:
                heart_5th.set_picture()

        if player_1st.amount_of_lives == 0:
            stopping = True
            heart_3rd.set_picture()

            print("2-ой победил")

        elif player_2nd.amount_of_lives == 0:
            stopping = True
            heart_6th.set_picture()

            print("1-ый победил")

        else:   
            begin_time = now_time()

            while int(now_time()) - int(begin_time) <= 2:
                for heart in hearts_group:
                    heart.reset()
                window.blit(time_label, (350, 50))
                print("Показываю Fail")
                window.blit(background_left, (0,200))
                window.blit(background_right, (400,200))
                display.update() 
            # время показа картинок не учитывается   
            global_begin_time += now_time() - begin_time

            puck.random_position()

        display.update()
    if not stopping:
    # Players
        player_1st.reset()
        player_1st.update()

        player_2nd.reset()
        player_2nd.extra_bot()

    # Puck
        puck.reset()
        puck.update()

    
# Hearts
    for heart in hearts_group:
        heart.reset()

# Time
    time_label = font_type.render("Time: "+str(round(now_time()-global_begin_time,4)), True, (255,255,255))
    window.blit(time_label, (350, 50))

    display.update()

    clock.tick(60)
