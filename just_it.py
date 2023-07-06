#ფაიგეიმის შემოტანა
import pygame
from random import *
from time import *
#ფაიგეიმის ინიციაცია
pygame.init()

#ვქმნით "საათს" თამაშის სიხშირის დასადგენად
clock = pygame.time.Clock()
fps = 40

#ცვლადები
enemy_number = 5
shooting_delay = 1.05



#ეკრანის ზომები (ბექგრაუნდის სურათის ზომების ნახევარი)
width = int(1920 / 2)
height = int(1403 / 2)
# ეკრანის შექმნა
screen = pygame.display.set_mode((width, height))

#ვცვლით ეკრანის აიქონს
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
#ვცვლით ეკრანის წარწერას
pygame.display.set_caption("Space Invaders!")

#შემოგვაქვს ბექგრაუნდის სურათი
background = pygame.image.load("images/galaxy.jpg").convert_alpha()
#ბექგრაუნდის სურათის ზომების ცვლილება, მორგება ეკრანის ზომებზე
background = pygame.transform.scale(background, (width, height))

# რაკეტის ზომების განსაზღვრა
player_width = 1302 / 15
player_height = 1920 / 15
# მოთამაშის სურათის შემოტანა
player_image = pygame.image.load("images/rocket.png").convert_alpha()
#მოთამაშის სურათის შემცირება ზომაში
player_image = pygame.transform.scale(player_image, (player_width, player_height))

#მოთამაშის კლასის შექმნა
class Player:
    def __init__(self, image):
        # გადაცემული სურათის შენახვა ცვლადში
        self.image = image
        #სურათის ზომის კვადრატის შექმნა და მისი განთავსება სასურველ კოორდინატებზე
        self.rect = self.image.get_rect(centerx=width / 2, centery=height - 100)
        # სიჩქარის ცვლადის შექმნა
        self.x_speed = 0
        self.bullet_list = []

    #დახატვის და მოძრაობის ფუნქცია
    def draw(self):
        # ტყვიების დახატვის ფუნქციონალი
        for bul in self.bullet_list:
            bul.draw()
        # ვხატავთ სურათს ეკრანზე მოთამაშის კვადრატში
        screen.blit(self.image, self.rect)
        # მოთამაშის კვადრატის ცენტრალურ კოორდინატებს ვცვლით სიჩქარის მიხედვით
        self.rect.centerx += self.x_speed

        # არ გავიდეს ეკრანის გარეთ
        if self.rect.left < 0 and self.x_speed < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width


        # ცარიელი ხომ არ არის ჩვენი ტყვიების სია
        if len(self.bullet_list) != 0:
            # ტყვია ხომ არ გაცდა საზღვარს
            if self.bullet_list[0].rect.bottom < 0:
                self.bullet_list.pop(0)






#უცხოპლანეტელების კლასი
class Alien:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(50, width - 50)
        self.rect.centery = randint(-400, -100)
        self.speed = randint(1, 4)

    def draw(self):
        global escaped_enemy
        screen.blit(self.image, self.rect)
        self.rect.centery += self.speed
        #თუ მოწინააღმდეგე გაცდა ეკრანის ქვედა საზღვარს, ახლიდან ჩამოვიდეს ზემოდან
        if self.rect.top > height:
            self.rect.centerx = randint(50, width - 50)
            self.rect.centery = randint(-400, -100)
            self.speed = randint(1, 4)
            escaped_enemy += 1
    # როგორ გამოიყურებოდეს ობიექტი ამოპრინტერებისას
    def __repr__(self):
        return "Alien Object"


class Bullet:
    #გადავცემთ სურათს და რაკეტის ლოკაციას რომ ტყვიაც იმ ადგილიდან გაისროლოს
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.speed = -4

    def draw(self):
        screen.blit(self.image, self.rect)
        self.rect.centery += self.speed


alien_image = pygame.image.load("ufo.png").convert_alpha()
#უცხოპლანეტელის სურათის ზომების რედაქტირება
new_width = 1280 / 10
new_height = 649 / 10
alien_image = pygame.transform.scale(alien_image, (new_width, new_height))

bullet_image = pygame.image.load("bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (640 // 20, 1280 // 20))
# მოთამაშის ობიექტს ვქმნით კლასიდან და გადავცემთ სურათს
player = Player(player_image)

#უცხოპლანეტელების ობიექტების სია
enemy_list = []
for i in range(enemy_number):
    enemy = Alien(alien_image)
    enemy_list.append(enemy)


creation_time = 0

# განადგურებული და გაქცეული მოწინააღმდეგეების დათვის ცვლადები
crushed_enemy = 0
escaped_enemy = 0

#ფონტების შექმნა
result_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 90)

#ბეჭვდის ფუნქცია
def write(font, color, text, x, y):
    render_text = font.render(text, True, color)
    text_rect = render_text.get_rect(centerx=x, centery=y)
    screen.blit(render_text, text_rect)


run = True
while run:

    # თამაში ხომ არ დასრულდა?
    if escaped_enemy >= 10:
        run = False


    clock.tick(fps)
    screen.blit(background, (0, 0))
    player.draw()


    for alien in enemy_list:
        #მოწინააღმდეგის დახატვა
        alien.draw()
        #ტყვია ხომ არ მოხდა
        for bul in player.bullet_list:
            if alien.rect.colliderect(bul.rect):
                # მოწინააღმდეგის თავიდან გენერირება
                alien.rect.centerx = randint(50, width - 50)
                alien.rect.centery = randint(-400, -100)
                alien.speed = randint(1, 4)
                # ტყვიის წაშლა
                player.bullet_list.remove(bul)
                crushed_enemy = crushed_enemy + 1

    #დავწეროთ განადგურებული მოწინააღმდეგის რაოდენობა
    crushed_text = f"Crushed: {crushed_enemy}"
    write(result_font, (100, 200, 100), crushed_text, 100, height - 100)
    # დავწეროთ გაქცეული მოწინააღმდეგის რაოდენობა
    escaped_text = f"Escaped: {escaped_enemy}"
    write(result_font, (200, 100, 100), escaped_text, 100, height - 50)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x_speed = 7
            if event.key == pygame.K_LEFT:
                player.x_speed = -7
            #ტყვიის გასროლის ფუნქციონალი
            if event.key == pygame.K_SPACE:
                new_bullet = time()
                if new_bullet - creation_time > shooting_delay:
                    bullet = Bullet(bullet_image, player.rect.centerx, player.rect.centery)
                    player.bullet_list.append(bullet)
                    creation_time = time()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_speed = 0

    pygame.display.update()


write(game_over_font, (255, 255, 255), "Game Over!", width / 2, height / 2)
pygame.display.update()
pygame.time.wait(3000)

pygame.quit()