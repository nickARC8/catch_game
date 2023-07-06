#ფაიგეიმის შემოტანა
import pygame
#ფაიგეიმის ინიციაცია
pygame.init()

#ეკრანის ზომები (ბექგრაუნდის სურათის ზომების ნახევარი)
width = 1920 / 2
height = 1403 / 2
# ეკრანის შექმნა
screen = pygame.display.set_mode((width, height))

#ვცვლით ეკრანის აიქონს
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
#ვცვლით ეკრანის წარწერას
pygame.display.set_caption("Space Invaders!")

#შემოგვაქვს ბექგრაუნდის სურათი
background = pygame.image.load("images/galaxy.jpg")
#ბექგრაუნდის სურათის ზომების ცვლილება, მორგება ეკრანის ზომებზე
background = pygame.transform.scale(background, (width, height))

# რაკეტის ზომების განსაზღვრა
player_width = 1302 / 15
player_height = 1920 / 15
# მოთამაშის სურათის შემოტანა
player_image = pygame.image.load("images/rocket.png")
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

    #დახატვის და მოძრაობის ფუნქცია
    def draw(self):
        # ვხატავთ სურათს ეკრანზე მოთამაშის კვადრატში
        screen.blit(self.image, self.rect)
        # მოთამაშის კვადრატის ცენტრალურ კოორდინატებს ვცვლით სიჩქარის მიხედვით
        self.rect.centerx += self.x_speed

        # არ გავიდეს ეკრანის გარეთ
        if self.rect.left < 0 and self.x_speed < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width




# მოთამაშის ობიექტს ვქმნით კლასიდან და გადავცემთ სურათს
player = Player(player_image)




run = True
while run:
    screen.blit(background, (0, 0))
    player.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x_speed = 0.8
            if event.key == pygame.K_LEFT:
                player.x_speed = -0.8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_speed = 0

    pygame.display.update()