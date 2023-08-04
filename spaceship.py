import random

import pygame

WIDTH = 720
HEIGHT = 480

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def checking_intersecrion_of_bullet_and_enemy(bullet_head, enemy_basement):
    x_bullet_head = bullet_head[0]
    y_bullet_head = bullet_head[1]

    x1_enemy_basement = enemy_basement[0]
    y1_enemy_basement = enemy_basement[1]
    x2_enemy_basement = enemy_basement[2]
    y2_enemy_basement = enemy_basement[3]

    if x1_enemy_basement <= x_bullet_head <= x2_enemy_basement and y1_enemy_basement >= y_bullet_head:
        return True

def you_win():
    font = pygame.font.Font(None, 72)
    text = font.render("You win!", True, 'green')
    place = text.get_rect(center=(200, 150))
    screen.blit(text, place)

def you_lose():
    font = pygame.font.Font(None, 72)
    text = font.render("You lose!", True, 'red')
    place = text.get_rect(center=(200, 150))
    screen.blit(text, place)

def main():
    global space_ship, bullets_for_enemies, bullets_for_spaceship
    space_ship = Spaceship()
    bullets_for_enemies = []
    bullets_for_spaceship = []
    clock = pygame.time.Clock()

    enemies = [Enemy(x, 20) for x in range(20, 700, 30)]
    running = True
    game_loosed = False
    """z value is for shooting. It does not allow to shot too often.
        It increases each iteration and gets 0 if the shot has been done"""
    z = 0
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            space_ship.move('left')
        if keys[pygame.K_d]:
            space_ship.move('right')
        if keys[pygame.K_SPACE]:
            if z > 10:
                space_ship.fire()
                z = 0
        screen.fill('black')
        space_ship.draw()
        if len(enemies) == 0:
            you_win()
        if game_loosed is True:
            you_lose()
        for enemy in enemies:
            enemy.draw()
            enemy.fire()
        #  get each of bullet in list of bullets
        for bullet_spaceship in bullets_for_spaceship:

            #  move the bullet
            bullet_spaceship.move()

            #  getting coordinates of the head of the bullet
            bullet_head = bullet_spaceship.get_coordinates_head()

            #  getting coordinates of the enemy basement and the index of the basement in enemies list
            coordinates_of_the_enemies = [[enemy.get_coordinates(), enemies.index(enemy)] for enemy in enemies]

            #  if there is an intersection between coordinates of the enemy basement and bullet head,
            #  the enemy will be deleted from the list of enemies
            for enemy_basement_coord, ind in coordinates_of_the_enemies:
                if checking_intersecrion_of_bullet_and_enemy(bullet_head, enemy_basement_coord) is True:
                    enemies.pop(ind)

        for bullet_enemy in bullets_for_enemies:
            bullet_enemy.move()

            #  deleting the bullet from the list of bullets if it gets the end of the screen border
            if bullet_enemy.get_head_of_the_bullet() >= HEIGHT:
                bullet_index = bullets_for_enemies.index(bullet_enemy)
                bullets_for_enemies.pop(bullet_index)

            """checking if the bullet hits our space_ship"""
            if bullet_enemy.check_hitting_with_spaceship() is True:
                space_ship.hitted()
                game_loosed = True
        pygame.display.flip()
        clock.tick(60)
        z += 1


class Spaceship:
    def __init__(self):
        self.x = WIDTH/2  # base x point of the ship
        self.y = HEIGHT   # base y point
        self.killed = False

    def draw(self):
        if self.killed == True:
            return
        """coordinates of the basement of the spaceship (rectangle)"""
        self.x1 = self.x - 25
        self.y1 = self.y - 10
        self.x2 = 50
        self.y2 = 10

        """coordinates of the head of the spaceship (rectangle)"""
        self.x1_head = self.x - 5
        self.y1_head = self.y - 20
        self.x2_head = 10
        self.y2_head = 8

        """drawing basement"""
        pygame.draw.rect(screen, 'white', ((self.x1, self.y1), (self.x2, self.y2)))

        """drawing head"""
        pygame.draw.rect(screen, 'white', ((self.x1_head, self.y1_head), (self.x2_head, self.y2_head)))

    def hitted(self):
        self.killed = True

    def get_head_coods(self):
        """this function used by enemy-bullets to check if they hit the head of the spaceship"""
        return self.x1_head, self.y1_head, self.x2_head, self.y2_head

    def get_body_spaceship(self):
        """this function used by enemy-bullets to check if they hit the basement of the spaceship"""
        return self.x1, self.y1

    def move(self, direction):
        """make a move for the spaceship depending on the pressed key"""
        if direction == 'left':
            self.x += -5
        elif direction == 'right':
            self.x += 5
        Spaceship.checking_hitting_with_ends(self)

    def checking_hitting_with_ends(self):
        if self.x <= 25:
            self.x = 26
        if self.x >= 695:
            self.x = 694

    def fire(self):
        """fire when the space is pressed"""
        if self.killed == False:
            bullet = Bullet_spaceship(x=self.x1_head+2, y=self.y1_head)
            bullets_for_spaceship.append(bullet)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fire_or_not = []
        for i in range(300):
            if i == 50:
                self.fire_or_not.append(True)
            else:
                self.fire_or_not.append(False)

    def draw(self):
        self.head = (self.x+5, self.y+20)
        coordinates = (
            (self.x, self.y),  #  first coordinate
            self.head,
            (self.x + 10, self.y)
        )
        pygame.draw.polygon(screen, 'white', (coordinates))

    def fire(self):
        if random.choice(self.fire_or_not) is True:
            bullets_for_enemies.append(Bullet_enemy(self.head[0], self.head[1]))

    def get_coordinates(self):
        """function returns coordinates (only first point) of the enemy"""
        basement_coordinates_of_enemy = self.x, self.y, self.x+10, self.y
        return basement_coordinates_of_enemy

class Bullet_spaceship:
    """the bullet that spaceship creates"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= 5
        pygame.draw.rect(screen, 'red', ((self.x, self.y - 8), (5, 7)))
        pygame.draw.polygon(screen, 'red', ((self.x, self.y - 9), (self.x + 2, self.y - 20), (self.x + 4, self.y - 9)))

    def get_coordinates_head(self):
        head_coordinates = self.x+2, self.y-20
        return head_coordinates

class Bullet_enemy:
    """bullet of the enemy built on the top of the enemies head"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        coordinates = (
            (self.x-2, self.y+1),
            (self.x-2, self.y+4),
            (self.x, self.y+6),
            (self.x+2, self.y+4),
            (self.x+2, self.y+1)
        )
        pygame.draw.polygon(screen, 'red', coordinates)

    def get_head_of_the_bullet(self):
        return self.y+6

    def move(self):
        self.y += 1
        Bullet_enemy.draw(self)

    def check_hitting_with_spaceship(self):

        #  coordinates of the bullet
        bullets_head_coord_x = self.x
        bullets_head_coord_y = self.y + 6

        #  cooordinates of the head spaceship
        coordinates_of_spaceship_head = space_ship.get_head_coods()   #  x1, y1
        x1_head_space_ship = coordinates_of_spaceship_head[0]
        y1_head_space_ship = coordinates_of_spaceship_head[1]
        x2_head_space_ship = x1_head_space_ship + 10
        y2_head_space_ship = y1_head_space_ship + 8

        #  check if coordinates intersect
        if x1_head_space_ship <= bullets_head_coord_x <= x2_head_space_ship \
                and y1_head_space_ship <= bullets_head_coord_y <= y2_head_space_ship:
            return True

        #  cooordinates of the body spaceship
        coordinates_of_spaceship_body = space_ship.get_body_spaceship()  # x1, y1
        x1_body_space_ship = coordinates_of_spaceship_body[0]
        y1_body_space_ship = coordinates_of_spaceship_body[1]
        x2_body_space_ship = x1_body_space_ship + 50
        y2_body_space_ship = y1_body_space_ship + 10

        #  check if coordinates intersect
        if x1_body_space_ship <= bullets_head_coord_x <= x2_body_space_ship \
                and y1_body_space_ship <= bullets_head_coord_y <= y2_body_space_ship:
            return True



if __name__ == '__main__':
    main()