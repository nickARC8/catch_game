import pygame
from random import randint, choice
from pygame import mixer
pygame.init()
# დროის კონტროლი (რამდენჯერ გაეშვას წამში თამაშის ციკლი)
clock = pygame.time.Clock()
fps = 120 #frame per second

mixer.music.load("images/zombie_music.mp3")
mixer.music.play(-1)
success = mixer.Sound("images/success.wav")


#ეკრანის შექმნაimages
width = 700
height = 500
screen = pygame.display.set_mode((width, height))
#წარწერის შეცვა ეკრანზე
pygame.display.set_caption("Labyrinth")
#ეკრანზე აიქონის შეცვლა
pygame.display.set_icon(pygame.image.load("images/cyborg.png"))
#ფონის სურათის შემოტანა
background = pygame.image.load("images/background.jpg")
#ფონის სურათის ზომის ცვლილება
background = pygame.transform.scale(background, (width, height))

#საგანძურის შექმნა
treasure_image = pygame.image.load("images/treasure.png")
treasure_image = pygame.transform.scale(treasure_image, (50, 50))
treasure_rect = treasure_image.get_rect(centerx=width - 70, centery=height - 70)


#მოთამაშის მარჯვენა სურათის შემოტანა
player_image = pygame.image.load("images/hero.png")

class Obj:
    # კონსტრუქტორს გადავცემთ მოთამაშის სურათს და ლოკაციას
    def __init__(self, x, y, image_right):
        # გადაცემულ სურათს ვუცვლით ზომებს
        self.image_right = pygame.transform.scale(image_right, (50, 50))
        # გადაცემულ სურათს ვაბრუნებთ სარკისებურად (მარცხნივ მოძრაობისთვის)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        # ვქმნით სურათის ზომის მართკუთხედს და გადავცემთ ცენტრალურ კოორდინატებს
        self.rect = self.image_right.get_rect(centerx=x, centery=y)
        # მიმართულების ცვლადი
        self.direction = "right"

    # მოთამაშის დახატვის ფუნქცია
    def draw(self, surface):
        # ხატავს გადაცემულ ზედაპირზე იმ სურათს რომელ მხარესაც აქვს აღებული მიმართულება
        if self.direction == "right":
            surface.blit(self.image_right, self.rect)
        else:
            surface.blit(self.image_left, self.rect)



#მოთამაშის კლასის შექმნა
class Player(Obj):
    # კონსტრუქტორს გადავცემთ მოთამაშის სურათს და ლოკაციას
    def __init__(self, x, y, image_right):
        super().__init__(x, y, image_right)
        # ჰორიზონტალური და ვერტიკალური სიჩქარეები
        self.x_speed = 0
        self.y_speed = 0
        self.mask = pygame.mask.from_surface(self.image_right)

    #მოძრაობის ფუნქციონალი
    def movement(self):
        # კვადრატის ცენტრალურ კოორდინატებს ემატებათ სიჩქარეები
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        #მიმართულების რედაქტირების ფუნქციონალი
        if self.x_speed > 0:
            self.direction = "right"
        elif self.x_speed < 0:
            self.direction = "left"
        #ჩვენი მოთამაშე არ გავიდეს ეკრანის საზღვრებიდან (მარჯვენა და მარცხენა საზღვარი)
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width
        # ჩვენი მოთამაშე არ გავიდეს ეკრანის საზღვრებიდან (ზედა და ქვედა საზღვარი)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

class Cyborg(Obj):
    def __init__(self, x, y, image_right):
        super().__init__(x, y, image_right)
        self.x_speed = 2
        self.y_speed = 0
        self.mask = pygame.mask.from_surface(self.image_right)

    def movement(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        #კონტროლები
        if self.rect.right == width:
            self.x_speed = -2
            self.direction = "left"

        if self.rect.left == width - 200 and self.x_speed == -2:
            self.x_speed = 0
            self.y_speed = 2

        if self.rect.bottom == height:
            self.y_speed = -2

        if self.rect.top == height - 200 and self.y_speed == -2:
            self.y_speed = 0
            self.x_speed = 2
            self.direction = "right"

#კედლის კლასის შექმნა
class Wall:
    #კედლის კლასს მართკუთხედის შესაქმნელად სჭირდება ოთხი მონაცემი (იქს კოორდინატი / იგრეკ კოორდინატი / სიგანე / სიმაღლე)
    def __init__(self, x, y, w, h):
        #იქმნება მართკუთხედი
        self.rect = pygame.Rect(x, y, w, h)

    #მართკუთხედის დახატვის ფუნქცია
    def draw(self):
        # საჭიროებს სამ მონაცემს: რაზე დახატოს / ფერი / დასახატი მართკუთხედი
        pygame.draw.rect(screen, (100, 200, 100), self.rect)

#კედლების ჩამონათვლისთვის განკუთვნილი ცარიელი ლისთი
all_walls = []
# მართკუთხედების შექმნა Wall კლასის მეშვეობით, შემთხვევით შერჩეულ ლოკაციაზე, შემთხვევით შერჩეული ზომებით
for i in range(13):
    x = randint(200, 500)
    y = randint(0, 400)
    w = choice([10, 120])
    if w == 10:
        h = 120
    else:
        h = 10
    #ვქმნით მართკუთხედს
    wall = Wall(x, y, w, h)
    #ვამოწმებთ კიბორგისკენ ძალიან ხომ არ აქვს მართკუთხედს გაშვერილი მარჯვენა კიდე
    if wall.rect.right > 450:
        pass
    # თუ არ აქვს, ვამატებთ ჩამონათვალში
    else:
        all_walls.append(wall)


cyborg_image_right = pygame.image.load("images/cyborg.png")
cyborg = Cyborg(width - 200 + 25, height - 200 + 25, cyborg_image_right)

#მოთამაშის კლასისგან ობიექტის შექმნა
player = Player(100, 400, player_image)

#წარწერის ცვლადი
text = ""

#მთავარი ციკლის კონტროლერი
run = True
#მთავარი ციკლი
while run:
    # დროის კონტროლი (რამდენჯერ გაეშვას წამში თამაშის ციკლი)
    clock.tick(fps)
    #ეკრანის დახატვა
    screen.blit(background, (0, 0))

    #საგანძურის დახატვა
    screen.blit(treasure_image, treasure_rect)

    #მოთამაშს დახატვა
    player.draw(screen)

    cyborg.draw(screen)
    #მოთამაშის მოძრაობა
    player.movement()
    cyborg.movement()

    #თითოული კედლისთვის ჩამონათვალში, ვხატავთ ამ კედელს და ვამოწმებთ მოთამაშე ხოარ ეჯახება...
    for wall in all_walls:
        wall.draw()
        if player.rect.colliderect(wall.rect):
            run = False
            text = "Looser!!!"

    #კლავიატურის და მაუსის კონტროლი
    for event in pygame.event.get():
        #როდის გაითიშოს პროგრამა
        if event.type == pygame.QUIT:
            run = False
        #რომელ კლავიშს დავაწექი და აკორექტირებს სჩქარეს
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x_speed = 1
            if event.key == pygame.K_LEFT:
                player.x_speed = -1

            if event.key == pygame.K_UP:
                player.y_speed = -1
            if event.key == pygame.K_DOWN:
                player.y_speed = 1
        # რომელ კლავიშს ავუში და აკორექტირებს სჩქარეს
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.x_speed = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.y_speed = 0


    #შეჯახების ფუნქციონალი
    if pygame.sprite.collide_mask(player, cyborg):
        run = False
        text = "Looser!!!"

    if player.rect.collidepoint((treasure_rect.centerx, treasure_rect.centery)):
        run = False
        text = "Treasure Is Yours!!!"
        success.play()
    #ეკრანის განახლება
    pygame.display.update()



#ფონტის შექმნა
font = pygame.font.Font(None, 60)
#ტექსტის ფინტით თეთრად რენდერირება
final_text = font.render(text, False, (255, 100, 100), (0, 0, 0))
#მართკუთხედის შექმნა ტექსტისთვის და ეკრანის ცენტრში განთავსება
final_text_rect = final_text.get_rect(centerx=width/2, centery=height/2)
#წარწერის გამოტანა
screen.blit(final_text, final_text_rect)
#ეკრანის განახლება
pygame.display.update()
#სამი წამით დაცდა თამაშის დასრულებამდე
pygame.time.wait(3000)

#ფაიგეიმის გათიშვა
pygame.quit()