import pygame, random
pygame.init()
screen_width, screen_height = 700, 800
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D POLICE CAR GAME")

menu_font = pygame.font.SysFont("comicsans", 40, True)
score_font = pygame.font.SysFont("comicsans", 35, True)
death_font = pygame.font.SysFont("comicsans", 80, True)
list_cars, new_car_count, new_car_num, tick_num, score = [], 45, 0, 30, 0


class Background:
    def __init__(self, y):
        self.x = 0
        self.y = y
        self.pic = pygame.transform.scale(pygame.image.load('Resources/Road_bg.png'), (700, 1500))
        self.vel = 10


class Player:
    def __init__(self):
        self.x = 156
        self.y = 600
        self.vel = 10
        self.pic_options = [pygame.transform.scale(pygame.image.load("Resources/police-car-siren-blue.png"), (170, 200)), pygame.transform.scale(pygame.image.load("Resources/police-car-siren-red.png"), (170, 200)), pygame.transform.scale(pygame.image.load("Resources/police car.png"), (170, 200))]
        self.pic = 0
        self.left, self.right, self.turn_count = False, False, 1
        self.health = 100


class Obstacles:
    def __init__(self, y):
        self.y = y
        self.car_pic_options = [pygame.transform.scale(pygame.image.load("Resources/car1.png"), (70, 130)),
                       pygame.transform.scale(pygame.image.load("Resources/car2.png"), (70, 130)),
                       pygame.transform.scale(pygame.image.load("Resources/car3.png"), (70, 130)),
                       pygame.transform.scale(pygame.image.load("Resources/car4.png"), (70, 130)),
                       pygame.transform.scale(pygame.image.load("Resources/car5.png"), (70, 130))]
        self.pic = random.choice(self.car_pic_options)

        self.x_coord_options = [210, 317, 423]
        self.x = random.choice(self.x_coord_options)


def add_car():
    new_car = Obstacles(-150)
    list_cars.append(new_car)




bg1, bg2 = Background(0), Background(-1500)
player = Player()

# --------------------------------------- MENU --------------------------------------- #
text_info1 = menu_font.render('PRESS ANY KEY TO START!', 1, (0, 0, 255))
text_info2 = score_font.render('Dodge the cars in the quickest time', 1, (0, 0, 255))
gameInit = 0
while gameInit == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            gameInit = 1

    win.blit(bg1.pic, (0, 0))
    win.blit(text_info1, (40, 150))
    win.blit(text_info2, (50, 200))
    pygame.display.update()



run = True
while run:
    pygame.time.delay(tick_num)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x >= 80:
        player.x -= player.vel
        player.left = True
    if keys[pygame.K_RIGHT] and player.x <= 450:
        player.x += player.vel
        player.right = True

    if not 100 <= player.x <= 430:
        player.health -= 1
        tick_num = 50
    else: tick_num = 30

    new_car_count += 1
    if new_car_count >= 30:
        add_car()
        new_car_count = random.choice(range(0, 5))

    for bg in [bg1, bg2]:
        win.blit(bg.pic, (bg.x, bg.y))
        bg.y += bg.vel
        if bg.y >= 1500:
            bg.y = -1500

    for car in list_cars:
        if car.y > (screen_height + 200):
            list_cars.remove(car)
        else:
            car.y += bg1.vel
            win.blit(car.pic, (car.x, car.y))

        if player.left:
            if car.y-110 <= (player.y + 40) <= car.y and (car.x - 70) <= (player.x + 50) <= (car.x + 50):
                run = False
            elif car.y <= (player.y + 40) <= (car.y + 115) and (car.x - 60) <= (player.x + 50) <= (car.x + 65):
                run = False
        elif player.right:
            if car.y-110 <= (player.y + 40) <= car.y and (car.x - 60) <= (player.x + 50) <= (car.x + 65):
                run = False
            elif car.y <= (player.y + 40) <= (car.y + 115) and (car.x - 70) <= (player.x + 50) <= (car.x + 50):
                run = False
        else:
            if car.y <= (player.y + 40) <= (car.y + 130) and (car.x - 75) <= (player.x + 50) <= (car.x + 70):
                run = False
        if player.health <= 0:
            run = False

    score += 1
    text1 = score_font.render("Tire wear: " + str(int(player.health//10)), 1, (100, 0, 255))
    text2 = score_font.render("Time: " + str(int(score // 20)), 1, (0, 0, 255))
    win.blit(text1, (515, 40))
    win.blit(text2, (515, 10))

    if player.left and not player.right:
        new_image = win.blit(pygame.transform.rotate(player.pic_options[int(player.pic//1)], 10), (player.x-20, player.y-10))
    elif player.right and not player.left:
        new_image = win.blit(pygame.transform.rotate(player.pic_options[int(player.pic//1)], 350), (player.x-10, player.y-10))
    else:
        win.blit(player.pic_options[int(player.pic//1)], (player.x, player.y))
    player.left, player.right = False, False
    if player.pic < 2.8:
        player.pic += 0.20
    else:
        player.pic = 0

    pygame.display.update()


text_info_death = death_font.render("YOU LOST!!", 1, (255, 0, 0))
win.blit(text_info_death, (40, 150))
pygame.display.update()
pygame.time.wait(4000)
pygame.quit()