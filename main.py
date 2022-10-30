import pygame
from random import *
import time
from pygame.locals import *
import os
vec = pygame.math.Vector2

SCREEN_SIZE = 400
FPS = 100

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), HWSURFACE | DOUBLEBUF)
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
pygame.font.init()
screen.set_alpha(None)
pygame.mixer.init(44100, -16, 2, 64)

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# empty function for testing purposes
def fun():
    pass

icon = pygame.image.load(find_file("icon.ico", os.getcwd()))
pygame.display.set_icon(icon)
bg_music = pygame.mixer.music.load(find_file("background.wav", os.getcwd()))
pygame.mixer.music.set_volume(0.1)
dt = clock.tick(FPS)

info = [
    "       *click anywhere to exit*",
    "",
    "space shooter was created by",
    "andrew wang(danub)",
    "do not distribute without",
    "permission!",
    "",
    "",
    "                how to play",
    "",
    "press the arrow keys to move",
    "press the space bar to shoot",
    "take down as many enemies as",
    "you can!",
    "there are 3 gamemodes",
    "easy, medium, and hard",
    "choose one and start your",
    "adventure!",
    ""
]

# Load pics
bg = pygame.image.load(find_file("background.png", os.getcwd()))
# Lasers
lazers = {"blue": pygame.image.load(find_file("laser blue.png", os.getcwd())).convert_alpha(),
          "green": pygame.image.load(find_file("laser green.png", os.getcwd())).convert_alpha(),
          "red": pygame.image.load(find_file("laser red.png", os.getcwd())).convert_alpha(),
          "bomber": pygame.image.load(find_file("bomber bomb.png", os.getcwd())).convert_alpha()}
playerL = pygame.image.load(find_file("player laser.png", os.getcwd())).convert_alpha()
# Ships
ships = {"blue": pygame.image.load(find_file("ship blue.png", os.getcwd())).convert_alpha(),
         "green": pygame.image.load(find_file("ship green.png", os.getcwd())).convert_alpha(),
         "red": pygame.image.load(find_file("ship red.png", os.getcwd())).convert_alpha(),
         "bomber": pygame.image.load(find_file("bomber.png", os.getcwd())).convert_alpha()}
playerS = pygame.image.load(find_file("player ship.png", os.getcwd())).convert_alpha()
# Powerups
health_powerup = pygame.image.load(find_file("health powerup.png", os.getcwd())).convert_alpha()
double_shot_powerup = pygame.image.load(find_file("double shot powerup.png", os.getcwd())).convert_alpha()
triple_shot_powerup = pygame.image.load(find_file("triple shot powerup.png", os.getcwd())).convert_alpha()
# Other
dotdotdot = pygame.image.load(find_file("dotdotdot.png", os.getcwd())).convert_alpha()
no_pic = pygame.image.load(find_file("no.png", os.getcwd())).convert_alpha()
music_pic = pygame.image.load(find_file("music.png", os.getcwd())).convert_alpha()
sound_pic = pygame.image.load(find_file("sound.png", os.getcwd())).convert_alpha()
particles_pic = pygame.image.load(find_file("particles.png", os.getcwd())).convert_alpha()
go_back_pic = pygame.image.load(find_file("go back.png", os.getcwd())).convert_alpha()

# Load sounds
laser1_sound = pygame.mixer.Sound(find_file("laser1.wav", os.getcwd()))
laser1_sound.set_volume(0.1)
laser2_sound = pygame.mixer.Sound(find_file("laser2.wav", os.getcwd()))
laser2_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(find_file("explosion.wav", os.getcwd()))
explosion_sound.set_volume(0.1)
button_press_sound = pygame.mixer.Sound(find_file("button press.wav", os.getcwd()))
button_press_sound.set_volume(0.1)
button_hover_sound = pygame.mixer.Sound(find_file("button hover.wav", os.getcwd()))
button_hover_sound.set_volume(0.025)


class Player(pygame.sprite.Sprite):  # Player class
    def __init__(self):
        self.group = all_sprites
        pygame.sprite.Sprite.__init__(self, self.group)
        self.image = playerS
        self.rect = self.image.get_rect()
        self.pos = vec(200, 360)
        self.vel = 0.2
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.width = 40
        self.height = 40
        self.max_health = 100
        self.health = self.max_health
        self.score = 0
        self.shoot_state = 1
        self.elapsed_time = 0
        self.time_limit = 0
        self.current_powerup = "none"
        self.strength = 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos.x -= self.vel * dt
        if keys[pygame.K_RIGHT]:
            self.pos.x += self.vel * dt
        if keys[pygame.K_UP]:
            self.pos.y -= self.vel * dt
        if keys[pygame.K_DOWN]:
            self.pos.y += self.vel * dt

        # Wall collisions
        if self.pos.x > SCREEN_SIZE - self.width / 2:
            self.pos.x = SCREEN_SIZE - self.width / 2
        if self.pos.x < self.width / 2:
            self.pos.x = self.width / 2
        if self.pos.y > SCREEN_SIZE - self.width / 2 - 20:
            self.pos.y = SCREEN_SIZE - self.width / 2 - 20
        if self.pos.y < 250:
            self.pos.y = 250
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.show_health()
        if self.health >= 100:
            self.health = 100
        self.mask = pygame.mask.from_surface(self.image)

        if self.shoot_state > 3:
            self.shoot_state = 3

        try:
            self.elapsed_time = time.time() - self.start_time
            if self.elapsed_time > self.time_limit:
                self.shoot_state = 1
                self.time_limit = 0
                self.current_powerup = "none"
        except:
            pass

        self.show_powerup()

    def fire(self):
        if self.shoot_state == 1:
            bullet = Bullet(0, 0)
        elif self.shoot_state == 2:
            bullet = Bullet(-7, 20)
            bullet = Bullet(7, 20)
        elif self.shoot_state == 3:
            bullet = Bullet(0, 0)
            bullet = Bullet(-17, 20)
            bullet = Bullet(17, 20)
        if sound_on:
            if randint(0, 1) == 0:
                laser1_sound.play()
            else:
                laser2_sound.play()

    def show_health(self):  # Player health
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.rect.x, self.rect.bottom+5, int(self.max_health*0.4), 3))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.rect.x, self.rect.bottom+5, int(self.health*0.4), 3))

    def show_powerup(self):
        if self.current_powerup == "none":
            self.elapsed_time = 0

        if self.time_limit != 0:
            font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 13)
            text = font.render(self.current_powerup, True, (255, 255, 255))
            screen.blit(text, (420, 130))
            pygame.draw.rect(screen, (100, 100, 100), (525, 130, 51, 10))
            pygame.draw.rect(screen, (200, 200, 0),
                             (526, 131, int(50 - self.elapsed_time * 50 / self.time_limit), 8))


class Bullet(pygame.sprite.Sprite):  # Bullet
    def __init__(self, x, y):
        self.group = all_sprites, bullets
        pygame.sprite.Sprite.__init__(self, self.group)
        self.image = playerL
        self.rect = self.image.get_rect()
        self.width = 5
        self.height = 15
        self.rect.center = (int(player.pos.x + x), int(player.pos.y + y))
        self.rect.y -= 15

    def update(self):
        self.rect.y -= 0.25 * dt
        # Out of screen
        if self.rect.bottom < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)

    def die(self):
        if particles_on:
            for _ in range(8):
                explosion = Explosion(self)
        self.kill()


class Enemy(pygame.sprite.Sprite):  # Enemies multiple types
    def __init__(self, type, start_pos):
        self.group = all_sprites, enemies
        pygame.sprite.Sprite.__init__(self, self.group)
        self.type = type
        try:
            self.image = ships[self.type]
        except:
            self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0.045)
        self.pos = vec(start_pos, -40)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.rand_moving = False
        self.ctr = 100
        if self.type == "red":
            self.max_health = 60
            self.health = 60
            self.point = 5
            self.width = 25
            self.height = 15
        elif self.type == "green":
            self.max_health = 40
            self.health = 40
            self.point = 3
            self.width = 25
            self.height = 15
        elif self.type == "blue":
            self.max_health = 20
            self.health = 20
            self.point = 2
            self.width = 15
            self.height = 15
        elif self.type == "bomber":
            self.max_health = 100
            self.health = 150
            self.point = 12
            self.width = 25
            self.height = 25
            self.vel = vec(0, 0.03)

    def update(self):
        self.pos += self.vel * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Fire bullet event
        if randint(0, int(400/difficulty)) == 0 and self.type != "bomber":
            self.fire()
        if randint(0, 330+(4-difficulty)*20) == 0 and self.type == "bomber":
            self.fire()

        if self.pos.y > 430:
            player.score -= 10
            self.kill()

        # Random move event
        if randint(0, int(150/difficulty*2)) == 0:
            self.random_move()
        if self.rand_moving == True:
            self.ctr -= 1
        if self.ctr == 0:
            self.ctr = 100
            self.rand_moving = False
            self.vel.x = 0

        if self.pos.x >= 390 - self.width // 2:
            self.pos.x = 390 - self.width // 2
        if self.pos.x <= 10 + self.width // 2:
            self.pos.x = 10 + self.width // 2

        # Test for death
        if self.health <= 0:
            self.die()

        self.show_health()
        self.mask = pygame.mask.from_surface(self.image)

    def fire(self):
        bullet = Enemy_bullet(self)

    def random_move(self):
        self.rand_moving = True
        temp_vel = randint(-20, 20) / 100/5*3
        while temp_vel == 0:
            temp_vel = randint(-20, 20) / 100/5*3
        self.vel.x = temp_vel

    def show_health(self):
        if self.type == "blue":
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.rect.x, self.rect.y-5, int(self.max_health*0.8), 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.rect.x, self.rect.y-5, int(self.health*0.8), 2))
        elif self.type == "green":
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.rect.x, self.rect.y-5, int(self.max_health*0.6), 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.rect.x, self.rect.y-5, int(self.health*0.6), 2))
        elif self.type == "red":
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.rect.x, self.rect.y-5, int(self.max_health*0.4), 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.rect.x, self.rect.y-5, int(self.health*0.4), 2))
        elif self.type == "bomber":
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.rect.x, self.rect.y-10, int(self.max_health/4), 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.rect.x, self.rect.y-10, int(self.health/6), 2))

    def die(self):
        if sound_on:
            explosion_sound.play()
        if particles_on:
            for _ in range(40):
                explosion = Explosion(self)
        if randint(0, 12) == 0:  # 12
            powerup = Powerup(self, "health")
        elif randint(0, 12) == 0 and (self.type == "red" or self.type == "green"):  # 12
            powerup = Powerup(self, "double_shot")
        elif randint(0, 9) == 0 and self.type == "red":  # 9
            powerup = Powerup(self, "triple_shot")
        elif randint(0, 6) == 0 and self.type == "bomber":  # 6
            powerup = Powerup(self, "triple_shot")
        player.score += self.point
        self.kill()


class Enemy_bullet(pygame.sprite.Sprite):  # Enemy's bullet
    def __init__(self, master):
        self.group = all_sprites, enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.group)
        self.master = master
        self.type = master.type
        self.image = lazers[self.type]
        self.rect = self.image.get_rect()
        self.width = 5
        self.height = 15
        self.vel = vec(0, 0.18)
        self.rect.center = (int(self.master.pos.x), int(self.master.pos.y))
        self.rect.y += 5
        if self.type == "red":
            self.strength = 6
            self.explosion_size = 8
        elif self.type == "green":
            self.strength = 4
            self.explosion_size = 8
        elif self.type == "blue":
            self.strength = 2
            self.explosion_size = 8
        elif self.type == "bomber":
            self.strength = 12
            self.vel = vec(0, 0.108)
            self.explosion_size = 70
            self.max_health = 40
            self.health = self.max_health

    def update(self):
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        if self.rect.y > 400:
            self.kill()
        if self.type == "bomber":
            try:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (self.rect.x, self.rect.y - 10, self.max_health * 0.5, 2))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (self.rect.x, self.rect.y - 10, self.health * 0.5, 2))
            except:
                pass
        try:
            if (self.type == "bomber" and self.rect.y > 350) or self.health <= 0:
                self.die()
        except:
            pass
        self.mask = pygame.mask.from_surface(self.image)

    def die(self):
        player.score += 2
        if self.type == "bomber":
            for _ in range(self.explosion_size):
                explosion = Explosion(self, time=60, slow_down=20)
        if particles_on and self.type != "bomber":
                for _ in range(self.explosion_size):
                    explosion = Explosion(self)
        self.kill()


class Explosion(pygame.sprite.Sprite):  # All explosions work with this
    def __init__(self, master, time=38, slow_down=0):
        self.group = all_sprites, explosions
        pygame.sprite.Sprite.__init__(self, self.group)
        self.master = master
        self.image = pygame.Surface((5, 5))
        self.color = self.master.image.get_at(
            (randint(0, self.master.width-1), randint(0, self.master.height-1)))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.pos = self.master.rect.center
        self.vel = vec(randint(-3, 3), randint(-3, 3))
        self.vel = self.vel/10*0.5
        self.rect.center = self.pos
        self.survive_time = 0
        self.time = time
        self.slow_down = slow_down

    def update(self):
        self.pos += self.vel * dt
        self.vel *= randint(70 + self.slow_down, 100) / 100
        self.survive_time += 1
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.survive_time > randint(self.time - 25, self.time + 25):
            self.kill()
        if self.rect.right >= 400:
            self.rect.right = 400
        try:
            if self.master.type == "bomber":
                if pygame.sprite.collide_rect(player, self):
                    player.health -= 0.2
                    self.kill()
        except:
            pass


class Powerup(pygame.sprite.Sprite):  # Powerups multiple types
    def __init__(self, master, type):
        self.group = all_sprites, powerups
        pygame.sprite.Sprite.__init__(self, self.group)
        self.master = master
        self.type = type
        if self.type == "health":
            self.image = health_powerup
        if self.type == "double_shot":
            self.image = double_shot_powerup
        if self.type == "triple_shot":
            self.image = triple_shot_powerup
        self.rect = self.image.get_rect()
        self.pos = self.master.pos
        self.rect.center = (int(self.master.pos.x), int(self.master.pos.y))
        self.vel = vec(0, 1)

    def update(self):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.pos.y > 430:
            self.die()
        self.mask = pygame.mask.from_surface(self.image)

    def use(self):
        if self.type == "health":
            player.health += 10
        if self.type == "double_shot":
            player.shoot_state = 2
            if player.time_limit != 0 and not player.time_limit >= 45:
                player.time_limit = player.time_limit - player.elapsed_time + 15
            elif player.time_limit >= 45 and player.elapsed_time <= 15:
                player.elapsed_time = 0
            elif player.elapsed_time > 15:
                player.time_limit = player.time_limit - player.elapsed_time + 15
            else:
                player.time_limit = 15
            player.start_time = time.time()
        if self.type == "triple_shot":
            player.shoot_state = 3
            if player.time_limit != 0 and not player.time_limit >= 30:
                player.time_limit = player.time_limit - player.elapsed_time + 10
            elif player.time_limit >= 30 and player.elapsed_time <= 10:
                player.elapsed_time = 0
            elif player.elapsed_time > 10:
                player.time_limit = player.time_limit - player.elapsed_time + 10
            else:
                player.time_limit = 10
            player.start_time = time.time()

    def die(self):
        self.kill()


class Button(pygame.sprite.Sprite):  # Customizable buttons
    def __init__(self, pos, size, color, other_color, text, font, text_color, function, picture=pygame.Surface((0, 0)), hover_sound=button_hover_sound, click_sound=button_press_sound):
        self.group = buttons
        pygame.sprite.Sprite.__init__(self, self.group)
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = size[0]
        self.height = size[1]
        self.default_color = color
        self.color = color
        self.hover_color = other_color
        self.text = text
        self.function = function
        self.first_hover = True
        self.first_click = True
        self.font = font
        self.text_color = text_color
        self.blit_text = self.font.render(self.text, True, self.text_color)
        self.text_width = self.blit_text.get_width()
        self.text_height = self.blit_text.get_height()
        self.first_hover = True
        self.first_click = True
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        self.picture = picture
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self, mouse_pos, mouse_state, mouse_released):
        self.mouse_pos = mouse_pos
        self.mouse_state = mouse_state
        self.mouse_released = mouse_released
        self.image.fill(self.color)
        if self.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
            if self.first_hover:
                self.hover_sound.play()
                self.first_hover = False
            if self.mouse_state == 1:
                if self.mouse_released == None:
                    if self.first_click:
                        self.click_sound.play()
                        self.function()
                        self.first_click = False
                else:
                    if self.first_click:
                        self.click_sound.play()
                        self.first_click = False
                    if self.mouse_released:
                        self.function()
                self.image.fill(self.color)
            else:
                self.first_click = True  
                self.image.fill(self.hover_color)
        else:
            self.first_hover = True

    def draw_text(self):
        screen.blit(self.blit_text, 
        (self.x + (self.width - self.text_width) // 2, self.y + (self.height - self.text_height) // 2))
        screen.blit(self.picture, (self.x + (self.width - self.picture.get_width()) // 2, 
        self.y + (self.height - self.picture.get_height()) // 2))


# Text animation
def gradual_text(text, font, size, pos, color, speed, btw=0.62):
    ctr = 0
    for ch in text:
        text = font.render(ch, True, color)
        if ch == "m":
            screen.blit(text, (pos[0] + ctr * size * (btw - 0.017), pos[1]))
        elif ch == 'a':
            screen.blit(
                text, (int(pos[0] + ctr * size * (btw - 0.005)), pos[1]))
        elif ch == "i":
            screen.blit(text, (int(pos[0] + ctr * size * (btw + 0.2)), pos[1]))
        elif ch == "1":
            screen.blit(text, (pos[0] + ctr * size * (btw + 0.02), pos[1]))
        else:
            screen.blit(text, (int(pos[0] + ctr * size * btw), pos[1]))

        ctr += 1
        pygame.time.delay(speed)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


# start screen background
def draw_bg():
    pygame.display.flip()
    # player ship
    temp = pygame.transform.scale(playerS, (100, 100))
    temp = pygame.transform.rotate(temp, 25)
    screen.blit(temp, (245, 245))
    pygame.time.delay(100)
    pygame.display.flip()
    # player lazer
    temp = pygame.Surface((10, 30), pygame.SRCALPHA)
    temp.fill((225, 188, 41))
    temp = pygame.transform.rotate(temp, 25)
    screen.blit(temp, (266, 220))
    pygame.time.delay(100)
    pygame.display.flip()
    # red ship
    temp = pygame.transform.scale(ships["red"], (50, 30))
    screen.blit(temp, (210, 160))
    pygame.time.delay(100)
    pygame.display.flip()
    # blue ship
    temp = pygame.transform.scale(ships["blue"], (30, 30))
    screen.blit(temp, (340, 210))
    pygame.time.delay(100)
    pygame.display.flip()
    # green ship
    temp = pygame.transform.scale(ships["green"], (50, 30))
    screen.blit(temp, (320, 30))
    pygame.time.delay(100)
    pygame.display.flip()
    # blue ship 2
    temp = pygame.transform.scale(ships["blue"], (30, 30))
    screen.blit(temp, (35, 120))


def draw_start_screen():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    screen.fill((0, 0, 0))
    gradual_text("SPaCe", title_font, 60, (35, 25),
                (255, 255, 255), 50, btw=0.68)
    gradual_text("SHooTeR", title_font, 60, (90, 95),
                (255, 255, 255), 50, btw=0.68)
    text = score_font.render("score: {}".format(score), True, (255, 255, 255))
    screen.blit(text, (35, 200))

    if difficulty == 1:
        text = score_font.render("highscore: {}".format(highscore1), True, (255, 255, 255))
    if difficulty == 2:
        text = score_font.render("highscore: {}".format(highscore2), True, (255, 255, 255))
    if difficulty == 3:
        text = score_font.render("highscore: {}".format(highscore3), True, (255, 255, 255))
    screen.blit(text, (35, 220))

    if difficulty == 1:
        text = diff_font.render("difficulty: easy", True, (255, 255, 255))
    if difficulty == 2:
        text = diff_font.render("difficulty: medium", True, (255, 255, 255))
    if difficulty == 3:
        text = diff_font.render("difficulty: hard", True, (255, 255, 255))
    screen.blit(text, (35, 263))
    
    draw_bg()
    pygame.display.flip()


def game():  # Game loop
    global running
    running = True
    game_screen_width = 400
    global force_quit
    global paused
    global dt
    global music_on

    if music_on:
        pygame.mixer.music.play(-1)
    buttons.empty()

    # functions for buttons
    def pause_game():
        global paused
        global new_start_time
        new_start_time = time.time()
        try:
            player.start_time += new_elapsed_time
        except:
            pass
        paused = not paused

        font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 60)
        small_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 25)
        text = font.render("Paused", True, (255, 255, 255))
        screen.blit(text, (70, 150))

        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def go_to_main_menu():
        global running
        global paused
        paused = False
        running = False

    # Buttons
    pause_button = Button((460, 295), (80, 30), (0, 180, 0), (0, 255, 0), "pause", 
    pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 18), (0, 0, 0), pause_game)
    main_menu_button = Button((435, 340), (130, 30), (180, 180, 0), (255, 255, 0), "main menu", 
    pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 18), (0, 0, 0), go_to_main_menu)

    # Draw permanent stuff on screen
    def draw():
        screen.fill((0, 0, 170))
        screen.blit(bg, (0, 0))
        pygame.draw.line(screen, (0, 0, 255), (401, 0), (401, 400), 4)
        pygame.draw.line(screen, (0, 0, 255), (400, 1), (600, 1), 4)
        pygame.draw.line(screen, (0, 0, 255), (597, 0), (597, 400), 4)
        pygame.draw.line(screen, (0, 0, 255), (400, 397), (600, 397), 4)

        # Draw scores
        font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 20)
        font2 = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 15)
        scoreTXT = font.render("score : {}".format(
            player.score), True, (255, 255, 255))
        screen.blit(scoreTXT, (420, 25))

        if difficulty == 1:
            highscoreTXT = font.render("highscore : {}".format(highscore1), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : easy", True, (255, 255, 255))
        if difficulty == 2:
            highscoreTXT = font.render("highscore : {}".format(highscore2), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : medium", True, (255, 255, 255))
        if difficulty == 3:
            highscoreTXT = font.render("highscore : {}".format(highscore3), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : hard", True, (255, 255, 255))
        screen.blit(highscoreTXT, (420, 70))
        screen.blit(diffTXT, (420, 100))

        all_sprites.update()
        all_sprites.draw(screen)

        # Draw buttons
        buttons.update(m_pos, m_state, None)
        buttons.draw(screen)
        for button in buttons:
            button.draw_text()

        pygame.display.flip()

    while running:
        if game_screen_width < 600:
            game_screen_width += 5
            screen = pygame.display.set_mode((game_screen_width, SCREEN_SIZE))

        dt = clock.tick(FPS)
        pygame.display.set_caption("Space Shooter | " + str(len(all_sprites.sprites())) + " | " + str(int(clock.get_fps())))

        # Get button pressed
        m_state = pygame.mouse.get_pressed()[0]
        m_pos = pygame.mouse.get_pos()
        # Pause loop
        while paused:
            m_state = pygame.mouse.get_pressed()[0]
            m_pos = pygame.mouse.get_pos()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            buttons.update(m_pos, m_state, None)
            buttons.draw(screen)
            for button in buttons:
                button.draw_text()

            current_time = time.time()
            new_elapsed_time = current_time - new_start_time
            pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # Player fire bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire()

        # Spawn enemies
        if randint(0, 70 + (4 - difficulty) * 20) == 0:
            new_enemy = Enemy(
                choice(["red", "green", "green", "blue", "blue", "blue"]), randint(20, 380))

        if randint(0, 800 + (4 - difficulty) * 215) == 0:
            new_enemy = Enemy("bomber", randint(20, 380))

        # Collisions
        if pygame.sprite.groupcollide(bullets, enemies, False, False):
            hits = pygame.sprite.groupcollide(bullets, enemies, False, False)
            for hit in hits:
                hit.die()
            hits = hits.values()
            for hit in hits:
                for h in hit:
                    h.health -= player.strength

        if pygame.sprite.spritecollideany(player, enemies, False):
            hits = pygame.sprite.spritecollide(
                player, enemies, False, pygame.sprite.collide_mask)
            for hit in hits:
                player.health -= 15
                hit.die()

        if pygame.sprite.spritecollideany(player, enemy_bullets, False):
            hits = pygame.sprite.spritecollide(
                player, enemy_bullets, False, pygame.sprite.collide_mask)
            for hit in hits:
                player.health -= hit.strength
                hit.die()

        if pygame.sprite.groupcollide(enemy_bullets, bullets, False, False):
            hits = pygame.sprite.groupcollide(
                enemy_bullets, bullets, False, True)
            for hit in hits:
                if hit.type != "bomber":
                    hit.die()
                else:
                    hit.health -= player.strength

        if pygame.sprite.spritecollideany(player, powerups, False):
            hits = pygame.sprite.spritecollide(
                player, powerups, False, pygame.sprite.collide_mask)
            for hit in hits:
                if hit.type != "health":
                    player.current_powerup = hit.type
                hit.use()
                hit.die()

        if player.health <= 0:
            running = False
            player_death()

        if player.score <= 0:
            player.score = 0

        draw()


def start():  # Start screen
    pygame.mixer.music.fadeout(5)
    draw_start_screen()

    global waiting

    start_screen_buttons()

    waiting = True
    while waiting:
        m_pos = pygame.mouse.get_pos()
        m_state = pygame.mouse.get_pressed()[0]
        m_released = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONUP:
                m_released = 1

        buttons.update(m_pos, m_state, m_released)
        buttons.draw(screen)
        for button in buttons:
            button.draw_text()
        pygame.display.flip()


def player_death():  # End screen
    for i in range(200):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.fill((0, 0, 170))
        screen.blit(bg, (0, 0))
        pygame.draw.line(screen, (0, 0, 255), (401, 0), (401, 400), 4)
        pygame.draw.line(screen, (0, 0, 255), (400, 1), (600, 1), 4)
        pygame.draw.line(screen, (0, 0, 255), (597, 0), (597, 400), 4)
        pygame.draw.line(screen, (0, 0, 255), (400, 397), (600, 397), 4)

        # Draw scores
        font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 20)
        font2 = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 15)
        scoreTXT = font.render("score : {}".format(
            player.score), True, (255, 255, 255))
        screen.blit(scoreTXT, (420, 25))

        if difficulty == 1:
            highscoreTXT = font.render("highscore : {}".format(highscore1), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : easy", True, (255, 255, 255))
        if difficulty == 2:
            highscoreTXT = font.render("highscore : {}".format(highscore2), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : medium", True, (255, 255, 255))
        if difficulty == 3:
            highscoreTXT = font.render("highscore : {}".format(highscore3), True, (255, 255, 255))
            diffTXT = font2.render("difficulty : hard", True, (255, 255, 255))
        screen.blit(highscoreTXT, (420, 70))
        screen.blit(diffTXT, (420, 100))

        font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 50)
        text = font.render("You DieD!", True, (255, 255, 255))
        screen.blit(text, (80, 150))
        
        Explosion(player, time=100, slow_down=15)
        explosions.update()
        explosions.draw(screen)

        pygame.mixer.music.fadeout(5)

        pygame.display.flip()


def update_difficulty(diff=1):
    global difficulty
    difficulty = diff

    pygame.draw.rect(screen, (0, 0, 0), (35, 263, 150, 10))
    if diff == 1:
        text = diff_font.render("difficulty: easy", True, (255, 255, 255))
    if diff == 2:
        text = diff_font.render("difficulty: medium", True, (255, 255, 255))
    if diff == 3:
        text = diff_font.render("difficulty: hard", True, (255, 255, 255))
    screen.blit(text, (35, 263))

    pygame.draw.rect(screen, (0, 0, 0), (35, 220, 180, 12))
    if diff == 1:
        text = score_font.render("highscore: {}".format(highscore1), True, (255, 255, 255))
    if diff == 2:
        text = score_font.render("highscore: {}".format(highscore2), True, (255, 255, 255))
    if diff == 3:
        text = score_font.render("highscore: {}".format(highscore3), True, (255, 255, 255))
    screen.blit(text, (35, 220))


def start_screen_buttons():  # Create buttons
    buttons.empty()

    easy_button = Button((35, 280), (50, 30), (0, 150, 0), (0, 230, 0), 
    "easy", button_font, (255, 255, 255), lambda: update_difficulty(1))
    medium_button = Button((95, 280), (50, 30), (170, 170, 0), (240, 240, 0), 
    "medi", button_font, (255, 255, 255), lambda: update_difficulty(2))
    hard_button = Button((155, 280), (50, 30), (180, 0, 0), (255, 0, 0), 
    "hard", button_font, (255, 255, 255), lambda: update_difficulty(3))
    start_button = Button((35, 322), (110, 50), (0, 0, 180), (0, 0, 255), 
    "start", text_font, (255, 255, 255), end_start_screen)
    more_button = Button((155, 322), (30, 50), (225, 120, 30), (255, 170, 20), 
    "", button_font, (255, 255, 255), more_functions, picture=dotdotdot)


def end_start_screen():
    global waiting
    waiting = False


def more_functions_go_back():
    global tmp
    tmp = False


def show_info():
    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 195, 11), (30, 30, 340, 340))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONUP:
                return 0

        count = 0
        for line in info:
            text = score_font.render(line, True, (0, 0, 0))
            screen.blit(text, (50, 50+count*16))
            count += 1

        pygame.display.flip()


def more_functions():
    buttons.empty()

    global tmp
    tmp = True

    # create buttons
    settings_button = Button((50, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
    "settings", more_buttons_font, (0, 0, 0), settings)
    info_button = Button((210, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
    "info", more_buttons_font, (0, 0, 0), show_info)
    go_back_button = Button((170, 265), (60, 70), (255, 195, 11), (220, 180, 30), 
    "", text_font, (0, 0, 0), more_functions_go_back, go_back_pic)

    while True:
        screen.fill((0, 0, 0))
        m_pos = pygame.mouse.get_pos()
        m_state = pygame.mouse.get_pressed()[0]
        m_released = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # restart start screen
                    draw_start_screen()
                    start_screen_buttons()
                    return 0
            if event.type == MOUSEBUTTONUP:
                m_released = 1

        if not tmp:
            tmp = True
            draw_start_screen()
            start_screen_buttons()
            return 0

        pygame.draw.rect(screen, (255, 195, 11), (30, 30, 340, 340))

        buttons.update(m_pos, m_state, m_released)
        buttons.draw(screen)
        for button in buttons:
            button.draw_text()

        pygame.display.flip()


def settings():
    global music_on
    global sound_on
    global tmp

    buttons.empty()

    def show_music():
        global music_on
        music_on = not music_on
        # save
        with open(find_file("settings.txt", os.getcwd()), "w") as f:
            f.truncate()
            f.write(str(music_on)+"\n")
            f.write(str(sound_on)+"\n")
            f.write(str(particles_on))

    def show_sound():
        global sound_on
        sound_on = not sound_on
        # save
        with open(find_file("settings.txt", os.getcwd()), "w") as f:
            f.truncate()
            f.write(str(music_on)+"\n")
            f.write(str(sound_on)+"\n")
            f.write(str(particles_on))

    def decrease_particles():
        global particles_on
        particles_on = not particles_on
        # save
        with open(find_file("settings.txt", os.getcwd()), "w") as f:
            f.truncate()
            f.write(str(music_on)+"\n")
            f.write(str(sound_on)+"\n")
            f.write(str(particles_on))

    def go_back():
        global tmp
        tmp = False

    # create buttons
    music_button = Button((90, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
    "music", more_buttons_font, (0, 0, 0), show_music)
    sound_button = Button((90, 120), (140, 45), (150, 150, 150), (110, 110, 110), 
    "sound", more_buttons_font, (0, 0, 0), show_sound)
    decrease_particles_buttons = Button((90, 190), (140, 50), (150, 150, 150), (110, 110, 110), 
    "particles", more_buttons_font, (0, 0, 0), decrease_particles)
    go_back_button = Button((170, 275), (60, 70), (255, 195, 11), (220, 180, 30), 
    "", text_font, (0, 0, 0), go_back, go_back_pic)

    tmp = True
    while True:
        screen.fill((0, 0, 0))
        m_pos = pygame.mouse.get_pos()
        m_state = pygame.mouse.get_pressed()[0]
        m_released = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # recreate more_functions buttons
                    buttons.empty()
                    Button((50, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
                    "settings", more_buttons_font, (0, 0, 0), settings)
                    Button((210, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
                    "info", more_buttons_font, (0, 0, 0), show_info)
                    go_back_button = Button((170, 265), (60, 70), (255, 195, 11), (220, 180, 30), 
                    "", text_font, (0, 0, 0), more_functions_go_back, go_back_pic)
                    return 0
            # check whether mouse button is up
            if event.type == MOUSEBUTTONUP:
                m_released = 1

        if not tmp:
            tmp = True
            buttons.empty()
            Button((50, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
            "settings", more_buttons_font, (0, 0, 0), settings)
            Button((210, 50), (140, 45), (150, 150, 150), (110, 110, 110), 
            "info", more_buttons_font, (0, 0, 0), show_info)
            go_back_button = Button((170, 265), (60, 70), (255, 195, 11), (220, 180, 30), 
            "", text_font, (0, 0, 0), more_functions_go_back, go_back_pic)
            return 0

        # background
        pygame.draw.rect(screen, (255, 195, 11), (30, 30, 340, 340))

        screen.blit(music_pic, (255, 55))
        if not music_on:
            screen.blit(no_pic, (250, 50))
        screen.blit(sound_pic, (255, 125))
        if not sound_on:
            screen.blit(no_pic, (250, 120))
        screen.blit(particles_pic, (255, 195))
        if not particles_on:
            screen.blit(no_pic, (250, 190))

        buttons.update(m_pos, m_state, m_released)
        buttons.draw(screen)
        for button in buttons:
            button.draw_text()

        pygame.display.flip()


text_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 30)
title_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 60)
score_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 16)
diff_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 13)
button_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 15)
more_buttons_font = pygame.font.Font(find_file("SFOuterLimits.ttf", os.getcwd()), 24)

difficulty = 1
score = 0

# load settings
with open(find_file("settings.txt", os.getcwd()), "r") as f:
    music_on = f.readline()
    sound_on = f.readline()
    particles_on = f.readline()

    if music_on[0] == "T":
        music_on = True
    else:
        music_on = False
    if sound_on[0] == "T":
        sound_on = True
    else:
        sound_on = False
    if particles_on[0] == "T":
        particles_on = True
    else:
        particles_on = False

# load highscore
with open(find_file("highscore.txt", os.getcwd()), "r") as f:
    highscore1 = int(f.readline())
    highscore2 = int(f.readline())
    highscore3 = int(f.readline())

force_quit = False
paused = False
running = True
new_start_time = 0
waiting = True
tmp = True

playing = True
while playing:
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    player = Player()

    start()
    game()
    score = player.score
    if difficulty == 1 and score > highscore1:
        highscore1 = score
    if difficulty == 2 and score > highscore2:
        highscore2 = score
    if difficulty == 3 and score > highscore3:
        highscore3 = score

    # save highscore
    with open(find_file("highscore.txt", os.getcwd()), "w") as f:
        f.truncate()
        f.write(str(highscore1)+"\n")
        f.write(str(highscore2)+"\n")
        f.write(str(highscore3))

pygame.quit()
quit()
