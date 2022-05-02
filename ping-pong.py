# Добавить возможность играть с ботом
# Одна картинка с победой слева, для игрока справа проигрыш
# Добавить Menu
# Таблицу лидеров
# Жизни
# Выбрать более приятный цвет


# Pause
# Input Boxes

from tkinter import ACTIVE
from pygame import *
from random import *
from time import time as now_time
import os
import json

clock = time.Clock()

COLOR_INACTIVE = (77, 255, 136)
COLOR_ACTIVE = (172, 57, 172)

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
        print("ИДУ")
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

# Кнопка
class Area():
    def __init__(self, x=0, y=0, width=100, height=30, color=(0,0,0)):
        self.rect = Rect(x, y, width, height)
        self.fill_color = color
        self.color = COLOR_INACTIVE

    def set_text(self, text, fsize=30, text_color=(0, 0, 0)):
        self.text = text
        self.image = font.Font(None, fsize).render(text, True, text_color)

    def draw(self,fill_color=(204, 51, 153),border_color=(204, 51, 153)):
        draw.rect(window,fill_color, self.rect)
        draw.rect(window,border_color, self.rect,5)

    def draw_text(self,shift_x=0, shift_y=0):
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))      


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, (255, 153, 153))
        self.active = False
        self.returning = 0
        self.input_text = ''
        self.global_name = ''

    def handle_event(self, event):
        global Menu
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.color = COLOR_ACTIVE 
                self.txt_surface = FONT.render("", True, (255, 153, 153))

            else:
                self.color = COLOR_INACTIVE
                self.txt_surface = FONT.render("Write your name here:", True, (255, 153, 153))

            # Введите имя
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    self.returning = 1
                    global_name = self.input_text
                    print(global_name) #NAME
                    self.global_name = self.input_text
                    self.input_text = ''

                    if MODE == 1 or MODE == 0:
                        Menu = False
                        for box in input_boxes:
                            box.returning = 0

                    elif MODE == 2:
                        returnings = 0
                        for box in input_boxes:
                            print(box, box.returning)
                            returnings += box.returning 
                            if returnings == 2:
                                Menu = False
                                for box in input_boxes:
                                    box.returning = 0
                            print(returnings)
 
                elif event.key == K_BACKSPACE:
                    self.input_text = self.input_text[:-1]

                else: 
                    self.input_text += event.unicode
                # Re-render the text.

                self.txt_surface = FONT.render(self.input_text, True, (255, 153, 153))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the rect.
        draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

def Menu_Play():
    global Menu, game_Play, MODE, global_begin_time, data, stopping, player_1st, player_2nd, puck, heart_1st, heart_2nd, heart_3rd, heart_4th, heart_5th, heart_6th, hearts_group

    with open("records.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    background = transform.scale(image.load("background.jpg"), (global_height, global_width))

    all_text = show_records()

    while Menu:
        
        window.blit(background, (0,0))

        # Закрытие приложения
        for event_get in event.get():
            if event_get.type == QUIT:
                Menu = False
                game_Play = False

            if event_get.type == MOUSEBUTTONDOWN and event_get.button == 1:
                x,y = event_get.pos
                if menu_btn_1.rect.collidepoint(x,y):
                    MODE = 2
                    menu_btn_1.color = COLOR_ACTIVE
                    menu_btn_2.color = COLOR_INACTIVE
                    menu_btn_3.color = COLOR_INACTIVE

                elif menu_btn_2.rect.collidepoint(x,y):
                    MODE = 1
                    menu_btn_2.color = COLOR_ACTIVE
                    menu_btn_1.color = COLOR_INACTIVE
                    menu_btn_3.color = COLOR_INACTIVE

                elif menu_btn_3.rect.collidepoint(x,y):
                    MODE = 0
                    menu_btn_3.color = COLOR_ACTIVE
                    menu_btn_2.color = COLOR_INACTIVE
                    menu_btn_1.color = COLOR_INACTIVE

            
            input_box1.handle_event(event_get)
            
            if MODE == 2:
                input_box2.handle_event(event_get)
                input_box2.update()
                input_box2.draw(window) 

        input_box1.update()
        input_box1.draw(window) 
        if MODE == 2:
            input_box2.update()
            input_box2.draw(window) 
        y = 250
        for text in all_text:
            window.blit(text, (200, y))
            y += 30 

        menu_btn_1.draw(menu_btn_1.color)
        menu_btn_1.draw_text(20, 15)

        menu_btn_2.draw(menu_btn_2.color)
        menu_btn_2.draw_text(20, 15)

        menu_btn_3.draw(menu_btn_3.color)
        menu_btn_3.draw_text(20, 15)

        display.update()

        clock.tick(60) 

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

    # Players
    pictures_players = ["reflector.png"]

    player_1st = Player(100, 100, 0, 400, pictures_players, 10, 0, 0)

    player_2nd = Enemy(100, 100, 700, 400, pictures_players, 10, 0, 0)

    # Puck
    picture_puck = ["puck.png"]

    puck = Puck(50, 50, 400, 500, picture_puck, 3)

    global_begin_time = now_time()
    # Variables
    stopping = False

def show_records():
    global data
    all_text = list()
    # Сортировка от меньшего к большему
    data = dict(sorted(data.items(), key=lambda x: x[1]['time']))
    
    tittle = font_type.render("           Records:", True, (210, 121, 166))
    all_text.append(tittle)

    for player in data:
        text = font_type.render(str(player) + ': ' + str(data[player]["time"]), True, (255,255,255))
        all_text.append(text)
        if len(all_text) == 11:
            break

    return all_text

# Window
global_height = 800
global_width = 800
window = display.set_mode((global_width,global_height))

display.set_caption("Ping-Pong")
display.set_icon(image.load("background.jpg"))
background = transform.scale(image.load("background.jpg"), (global_height, global_width))

# Font
font.init()
FONT = font.Font(None, 32)
font_type = font.Font(None,36)

# Menu
input_box1 = InputBox(275, 150, 200, 32, "Write your name here:")
input_box2 = InputBox(275, 200, 200, 32, "Write name of another gamer:")

menu_btn_1 = Area(312,50,170,50,(255, 255, 0))
menu_btn_1.set_text('Playing 1 vs 1',30,(255, 153, 153))
menu_btn_1.draw()
menu_btn_1.color = COLOR_ACTIVE

menu_btn_2 = Area(25,50,270,50,(255, 255, 0))
menu_btn_2.set_text('Playing with stupid bot',30,(255, 153, 153))
menu_btn_2.draw()

menu_btn_3 = Area(500,50,270,50,(255, 255, 0))
menu_btn_3.set_text('Playing with clever bot',30,(255, 153, 153))
menu_btn_3.draw()

menu_boxes = [menu_btn_1, menu_btn_2, menu_btn_3]
input_boxes = [input_box1, input_box2]

# Pause
pause_btn = Character(50, 50, 50, 200, "pause.png", 0) 
pause = False 

# Variables
Menu = True
MODE = 2
game_Play = True

while game_Play:

    window.blit(background, (0,0))

    if Menu:
        Menu_Play()

    for event_get in event.get():
        if event_get.type == QUIT:
            game_Play = False
        if event_get.type == MOUSEBUTTONDOWN and event_get.button == 1:  
            x,y = event_get.pos
            if pause_btn.rect.collidepoint(x,y) and not stopping:
                print("PAUSE")
                begin_pause = now_time()
                pause = True
                stopping = True

            elif pause:
                pause = False
                stopping = False
                minus_time = now_time() - begin_pause
                global_begin_time += minus_time

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
        if player_1st.amount_of_lives == 0 or player_2nd.amount_of_lives == 0:
            if player_1st.amount_of_lives == 0:
                stopping = True
                heart_3rd.set_picture()

                print("2-ой победил")

                if MODE == 2:
                    data[input_box2.global_name] = {}
                    data[input_box2.global_name]["time"] = round(int(now_time()) - global_begin_time, 4)
                    
                    with open("records.json", "w", encoding='utf-8') as file:
                        json.dump(data, file)

            elif player_2nd.amount_of_lives == 0:
                stopping = True
                heart_6th.set_picture()

                print("1-ый победил")
                data[input_box1.global_name] = {}
                data[input_box1.global_name]["time"] = round(int(now_time()) - global_begin_time, 4)
                print(data)
                with open("records.json", "w", encoding='utf-8') as file:
                    json.dump(data, file)
            Menu = True
            
            print("MENU_PLAY")
            
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
    player_1st.reset()
    player_2nd.reset()
    puck.reset()

    if not stopping:
    # Players 
        player_1st.update()

        if MODE == 0:
            player_2nd.extra_bot()

        if MODE == 1:
            player_2nd.update_bot()

        if MODE == 2:
            player_2nd.update()
    # Puck
        puck.update()

    # Time
    if not pause:
        time_label = font_type.render("Time: "+str(round(now_time()-global_begin_time,4)), True, (255,255,255))
    window.blit(time_label, (350, 50))
     
# Hearts
    for heart in hearts_group:
        heart.reset()

    pause_btn.reset()

    display.update()

    clock.tick(60)
