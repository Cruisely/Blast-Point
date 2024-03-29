import pygame, random

pygame.init()


WIDTH = 400
HEIGHT = 600


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blast Bounce")


clock = pygame.time.Clock()
FPS = 60


SCROLL_THRESH = 200
GRAVITY = 0.7
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0


Grey = 240, 240, 240
Dark_Grey = 100, 100, 100
Light_Grey = 200, 200, 200
Blue = 0, 144, 255
bg_contrast = 18, 20, 38

font_small = pygame.font.SysFont('data/fonts/VCR_OSD_MONO_1.001.ttf', 20)
font_big = pygame.font.SysFont('data/fonts/VCR_OSD_MONO_1.001.ttf', 24)
font_large = pygame.font.SysFont('data/fonts/VCR_OSD_MONO_1.001.ttf', 48)

logo = pygame.image.load('data/images/logo.png')
pygame.display.set_icon(logo)

bg_image = pygame.image.load('data/images/bg.png').convert_alpha()
rocketship = pygame.image.load('data/images/Rocketship.png').convert_alpha()
ufo = pygame.image.load('data/images/ufo.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img =  font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll))
	screen.blit(bg_image, (0, -600 + bg_scroll))

class Rocketship():
    def __init__(self, x, y):
         self.image = pygame.transform.scale(rocketship, (35, 60))
         self.width = 20
         self.height = 50
         self.rect = pygame.Rect(0, 0, self.width, self.height)
         self.rect.center = (x, y)
         self.vel_y = 0

    def move(self):
        
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a]: # LEFT
            dx = -3
        if key[pygame.K_d]: # RIGHT
            dx = 3

        self.vel_y += GRAVITY
        dy += self.vel_y

        if key[pygame.K_LEFT]: # LEFT
            dx = -3
        if key[pygame.K_RIGHT]: # RIGHT
            dx = 3


        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right
            
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(self.image, (self.rect.x - 8, self.rect.y - 5))

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width ):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(ufo, (75, 75))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
            self.rect.y += scroll
            
            if self.rect.top > HEIGHT:
                self.kill()



rocketship = Rocketship(WIDTH // 2, HEIGHT - 150) 

platform_group = pygame.sprite.Group()

platform = Platform(WIDTH // 2 - 50, HEIGHT - 150, 75)
platform_group.add(platform)

run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        scroll = rocketship.move()

        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(75, 75)
            p_x = random.randint(0, WIDTH - p_w)
            p_y = platform.rect.y - random.randint(165, 165)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)

        platform_group.update(scroll)

        platform_group.draw(screen)
        rocketship.draw()

        
        if rocketship.rect.top > HEIGHT:
            game_over = True
    else:
        draw_text('GAME OVER!', font_large, Blue, 100, 200)
        draw_text('SCORE: '+ str(score), font_big, Light_Grey, 160, 250)
        draw_text('PRESS SPACE TO RESTART', font_big, Light_Grey, 80, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            scroll = 0
            rocketship.rect.center = (WIDTH // 2, HEIGHT - 150)
            platform_group.empty()
            platform = Platform(WIDTH // 2 - 50, HEIGHT - 150, 75)
            platform_group.add(platform)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.QUIT()