#ფაიგეიმის შემოტანა
import pygame
from pygame import mixer
pygame.init()

#წამში რამდენჯერ გაეშვას თამაში
clock = pygame.time.Clock()
fps = 60

#ეკრანის შექმნა
width = 700
height = 500
screen = pygame.display.set_mode((width, height))

#თამაშის სახელის შეცვლა დუსფლეიზე
pygame.display.set_caption("Catch Game")
#აიქონის ატვირთვა
icon = pygame.image.load("images/sprite1.png")
#დისფლეიზე აიქონის შეცვლა
pygame.display.set_icon(icon)

#ფონის შექმნა
background = pygame.image.load("images/background.png")
#ფონის ზომის შეცვლა
background = pygame.transform.scale(background, (width, height))


#player1
player1_right = pygame.image.load("images/sprite1.png")
player1_right = pygame.transform.scale(player1_right, (50, 50))
player1_left = pygame.transform.flip(player1_right, True, False)
rect1 = player1_right.get_rect()
rect1.x = 100
rect1.y = 400
speed1_horizontal = 0
speed1_vertical = 0

#player2
player2_right = pygame.image.load("images/sprite2.png")
player2_right = pygame.transform.scale(player2_right, (50, 50))
player2_left = pygame.transform.flip(player2_right, True, False)
rect2 = player2_right.get_rect()
rect2.x = 300
rect2.y = 400
speed2_horizontal = 0
speed2_vertical = 0


sprite1 = player1_right
sprite2 = player2_right

font = pygame.font.Font(None, 90)
def game_over(font):
    text = "Game Over"
    text_render = font.render(text, True, (200, 0, 0))
    text_rect = text_render.get_rect()
    text_rect.centerx = int(width/2)
    text_rect.centery = int(height/2)
    screen.blit(text_render, text_rect)

#მთავარი თამაშის ციკლი
run = True
while run:
    clock.tick(fps)
    #ფონის დაკვრა ეკრანზე
    screen.blit(background, (0, 0))


    rect1.x += speed1_horizontal
    rect2.x += speed2_horizontal

    rect1.y += speed1_vertical
    rect2.y += speed2_vertical

    #პირველი მოთამაშის ეკრანზე გამოჩენა
    screen.blit(sprite1, rect1)
    # მეორე მოთამაშის ეკრანზე გამოჩენა
    screen.blit(sprite2, rect2)

    #თამაშის გათიშვის ფუნქციონალი
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #კლავიშს თუ დავაჭირეთ
        if event.type == pygame.KEYDOWN:
            #რომელ კლავიშს დავაჭირეთ player1
            if event.key == pygame.K_RIGHT:
                speed1_horizontal = 5
            if event.key == pygame.K_LEFT:
                speed1_horizontal = -5
            #ვერტიკალური მოძრაობა
            if event.key == pygame.K_UP:
                speed1_vertical = -5
            if event.key == pygame.K_DOWN:
                speed1_vertical = 5

            # რომელ კლავიშს დავაჭირეთ player2
            if event.key == pygame.K_d:
                speed2_horizontal = 5
            if event.key == pygame.K_a:
                speed2_horizontal = -5

            # მეორე სპრაიტის ვერტიკალური მოძრაობა
            if event.key == pygame.K_w:
                speed2_vertical = -5
            if event.key == pygame.K_s:
                speed2_vertical = 5

        #კლავიშს თუ ავუშვით
        if event.type == pygame.KEYUP:
            #მარჯჯვნივ ან მარცხნივ წასვლის ღილაკს ხოარ ავუშვით player1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                speed1_horizontal = 0
            # მარჯჯვნივ ან მარცხნივ წასვლის ღილაკს ხოარ ავუშვით player2
            if event.key == pygame.K_d or event.key == pygame.K_a:
                speed2_horizontal = 0

            # ზემოთ ან ქვემოთ წასვლის ღილაკს ხოარ ავუშვით player1
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                speed1_vertical = 0

            # ზემოთ ან ქვემოთ წასვლის ღილაკს ხოარ ავუშვით player1
            if event.key == pygame.K_w or event.key == pygame.K_s:
                speed2_vertical = 0

    #პირველი მოთამაშის მარცხენა საზღვარი
    if rect1.x < 0:
        rect1.x = 0
    #მარჯვენა საზღვარი
    if rect1.x > width - 50:
        rect1.x = width - 50

    # პირველი მოთამაშის ზედა საზღვარი
    if rect1.y < height - 150:
        rect1.y = height - 150
    # ქვედა საზღვარი
    if rect1.y > height - 50:
        rect1.y = height - 50

    # მეორე მოთამაშის მარცხენა საზღვარი
    if rect2.x < 0:
        rect2.x = 0
    # მარჯვენა საზღვარი
    if rect2.x > width - 50:
        rect2.x = width - 50

    # მეორე მოთამაშის ზედა საზღვარი
    if rect2.y < height - 150:
        rect2.y = height - 150
    # ქვედა საზღვარი
    if rect2.y > height - 50:
        rect2.y = height - 50

    #1 სპრაიტის მიმართულების კონტროლი
    if speed1_horizontal == 5:
        sprite1 = player1_right
    if speed1_horizontal == -5:
        sprite1 = player1_left
    # 2 სპრაიტის მიმართულების კონტროლი
    if speed2_horizontal == 5:
        sprite2 = player2_right
    if speed2_horizontal == -5:
        sprite2 = player2_left


    #დაჭერის ფუნქციონალი
    if rect1.collidepoint(rect2.centerx, rect2.centery):
        break

    pygame.display.update()

game_over(font)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()