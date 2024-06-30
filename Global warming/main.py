# -*- coding: utf8 -*-

import pygame
import random
import webbrowser

# Инициализация библиотеки
pygame.init()

# Указываем размер окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Задаем название окна
pygame.display.set_caption("Global Warming")

icon_image = pygame.image.load("gamico.jpg")
pygame.display.set_icon(icon_image)

# Загружаем изображение
background_image = pygame.image.load("background\sky1.jpg")

# Подгоняем масштаб под размер окна
background_image = pygame.transform.scale(background_image, (800, 800))

# Накладываем изображение на поверхность
screen.blit(background_image, (0, 0))

# Smoke object
smoke = pygame.image.load('sprites\smoke1.png')
object_width = 100
object_height = 100
smoke = pygame.transform.scale(smoke, (object_width, object_height))
smokeX = 0
smokeY = 800    
speed = 1

#pause object
pause = pygame.image.load('sprites\pause.png')
pause_width = 100
pause_height = 100
pause = pygame.transform.scale(pause, (pause_width, pause_height))
pause_Rect = pause.get_rect()
pause_Rect = pause_Rect.move(690, 480)
print(pause_Rect)

#restart object
restart = pygame.image.load('sprites/restart.png')
restart_width = 100
restart_height = 100
restart = pygame.transform.scale(restart, (restart_width, restart_height))
restart_Rect = restart.get_rect()
restart_Rect = restart_Rect.move(10, 480)
print(restart_Rect)

#logo object
ds_logo = pygame.image.load('sprites\ds_logo.png')
ds_logo = pygame.transform.scale(ds_logo, (150, 150))
ds_Rect = ds_logo.get_rect()
ds_Rect = ds_Rect.move(10, 300)
print(ds_Rect)

kod_logo = pygame.image.load('sprites\kodland_logo.png')
kod_logo = pygame.transform.scale(kod_logo, (150, 150))
kod_Rect = kod_logo.get_rect()
kod_Rect = kod_Rect.move(10, 150)
print(kod_Rect)

pygame.mixer.music.load('sounds\wind.mp3')
pygame.mixer.music.play(-1) 

s = pygame.mixer.Sound("sounds\smoke.mp3")
f = pygame.mixer.Sound("sounds\inf.mp3")
e = pygame.mixer.Sound("sounds\end.mp3")
w = pygame.mixer.Sound("sounds\win_s.mp3")

objects = []
object_spawn_timer = 0

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
fail = 0
attemp = 1
won = False

paused = False

rects = [] 

def read_record():
    try:
        with open("record.txt", "r") as file:
            return int(file.readline())
    except FileNotFoundError:
        return 0

def write_record(record):
    with open("record.txt", "w") as file:
        file.write(str(record))

record = read_record()        

def update_record(score):
    global record
    record = read_record()
    if score > record:
        record = score
        write_record(record)        

while True:
    pygame.time.delay(5)
    screen.blit(background_image, (0, 0))
    score_text = font.render(f"Score: {score} High Score: {record}", True, (236, 39, 39))
    screen.blit(score_text, (10, 10))
    screen.blit(pause, pause_Rect) 
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_record(score)
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_Rect.collidepoint(event.pos):
                paused = not paused

    if not paused: 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            for obj in objects: 
                obj_rect = smoke.get_rect(topleft=(obj[0], obj[1])) 
                if obj_rect.collidepoint(event.pos): 
                    objects.remove(obj) 
                    score += 1 
                    speed += 0.1
                    object_spawn_timer = max(object_spawn_timer - 10, 10) 
                    s.play()    
                                
    if (fail < 16 and won == False):
        if not paused:    
            if object_spawn_timer <= 0:
                objects.append([random.randint(0, screen_width - object_width - 100), screen_height])
                object_spawn_timer = 100 

            for obj in objects:
                screen.blit(smoke, (obj[0], obj[1])) 
                obj_rect = smoke.get_rect(topleft=(obj[0], obj[1])) 
                rects.append(obj_rect) 
                obj[1] -= speed

                if obj[1] <= 0:       
                    fail += 1
                    objects.remove(obj)             

            if fail > 3:
                if attemp == 1:
                    background_image = pygame.image.load("background\sky2.jpg")
                    f.play()             
                    attemp += 1

            if fail > 6:
                if attemp == 2:
                    background_image = pygame.image.load("background\sky3.jpg")
                    f.play()
                    attemp += 1

            if fail > 15:
                if attemp == 3:
                    background_image = pygame.image.load("background\end.jpg")
                    e.play()
                    objects.clear() 
                    pygame.mixer.music.stop() 
                    attemp += 1

            if score > 69:
                if won == False:
                    background_image = pygame.image.load("background\win.jpg") 
                    w.play()
                    objects.clear() 
                    pygame.mixer.music.stop() 
                    won = True         

        object_spawn_timer -= 1

        update_record(score)

    if paused:
        pause_text = font.render("Paused", True, (236, 39, 39))
        screen.blit(pause_text, (screen_width//2 - 50, screen_height//2 - 10))

        screen.blit(ds_logo, ds_Rect)

        screen.blit(kod_logo, kod_Rect)

        screen.blit(restart, restart_Rect) 


        if event.type == pygame.MOUSEBUTTONDOWN:
            if ds_Rect.collidepoint(event.pos):
                 webbrowser.open("https://discord.gg/kodland")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if kod_Rect.collidepoint(event.pos):
                 webbrowser.open("https://www.kodland.org/ru") 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_Rect.collidepoint(event.pos):
                 background_image = pygame.image.load("background\sky1.jpg")
                 objects.clear()         
                 pygame.mixer.music.play(-1)
                 won = False
                 fail = 0
                 attemp = 1
                 score = 0
                 object_spawn_timer = 0
                 speed = 1
                 object_spawn_timer = 0
                 paused = False
    

    pygame.display.update()   
    clock.tick(120)