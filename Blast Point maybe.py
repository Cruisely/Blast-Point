import pygame, random

pygame.init()


WIDTH = 600
HEIGHT = 800


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blast Point")


clock = pygame.time.Clock()
FPS = 60


SCROLL_THRESH = 200
GRAVITY = 0.7
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0


Grey = 240, 240, 240
Dark_Grey = 100, 100, 100
Light_Grey = 200, 200, 200
Blue = 0, 144, 255


logo = pygame.image.load('data/images/logo.png')
pygame.display.set_icon(logo)

bg_image = pygame.image.load('data/images/bg.png').convert_alpha()
rocketship = pygame.image.load('data/images/Rocketship.png').convert_alpha()
moon = pygame.image.load('data/images/moon.png').convert_alpha()


def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll))
	screen.blit(bg_image, (0, -800 + bg_scroll))

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

        if self.rect.bottom + dy > HEIGHT:
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
		self.image = pygame.transform.scale(moon, (400, 400))
		self.width = 200
		self.height = 200
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
        

	def update(self, scroll):
            self.rect.y += scroll


rocketship = Rocketship(WIDTH // 2, HEIGHT - 150) 

platform_group = pygame.sprite.Group()

run = True
while run:

    clock.tick(FPS)

    scroll = rocketship.move()

    bg_scroll += scroll
    if bg_scroll >= 600:
        bg_scroll = 0
    draw_bg(bg_scroll)

    if len(platform_group) < MAX_PLATFORMS:
        platform = Platform(WIDTH // 2 - 100, HEIGHT - 50, 400)
        platform_group.add(platform)

    platform_group.update(scroll)

    platform_group.draw(screen)
    rocketship.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.QUIT()