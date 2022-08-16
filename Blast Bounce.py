import pygame, random

pygame.init()


WIDTH = 600
HEIGHT = 800


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blast Bounce")


clock = pygame.time.Clock()
FPS = 60


SCROLL_THRESH = 200
scroll = 0
GRAVITY = 0.7
MAX_PLATFORMS = 10


Grey = 240, 240, 240
Dark_Grey = 100, 100, 100
Light_Grey = 200, 200, 200
Blue = 0, 144, 255


logo = pygame.image.load('data/images/logo.png')
pygame.display.set_icon(logo)

bg_image = pygame.image.load('data/images/bg.png').convert_alpha()
rocketship = pygame.image.load('data/images/Rocketship.png').convert_alpha()
moon = pygame.image.load('data/images/moon.png').convert_alpha()


class Rocketship():
    def __init__(self, x, y):
         self.image = pygame.transform.scale(rocketship, (35, 60))
         self.width = 20
         self.height = 50
         self.rect = pygame.Rect(0, 0, self.width, self.height )
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
        if key[pygame.K_w]: # UP
            dy = -3

        self.vel_y += GRAVITY
        dy += self.vel_y

        if key[pygame.K_LEFT]: # LEFT
            dx = -3
        if key[pygame.K_RIGHT]: # RIGHT
            dx = 3 
        if key[pygame.K_UP]: # UP
            dy = -3

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
            scroll = -dy

        self.rect.x += dx
        self.rect.y += dy

        return scroll

    def draw(self):
        screen.blit(self.image, (self.rect.x - 8, self.rect.y - 5))
        pygame.draw.rect(screen, Grey, self.rect, 2)

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width ):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(moon, (75, 75))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


rocketship = Rocketship(WIDTH // 2, HEIGHT - 150) 

platform_group = pygame.sprite.Group()

for p in range(MAX_PLATFORMS):
	p_w = random.randint(40, 60)
	p_x = random.randint(0, WIDTH - p_w)
	p_y = p * random.randint(80, 120)
	platform = Platform(p_x, p_y, p_w)
	platform_group.add(platform)


run = True
while run:

    clock.tick(FPS)

    scroll = rocketship.move()

    screen.blit(bg_image, (0,0))

    pygame.draw.line(screen, Blue, (0, SCROLL_THRESH), (WIDTH, SCROLL_THRESH))
    
    platform_group.draw(screen) 
    rocketship.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.QUIT()