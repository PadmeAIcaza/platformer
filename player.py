import pygame

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3
        
    def __init__(self, x, y, width, height, sprites):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0
        self.SPRITES = sprites
          
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count = 0
        
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0
            
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        
    def hit_head(self):
        self.count = 0
        self.y_vel += -1
        
    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.x_vel != 0:
            sprite_sheet = 'run'
            
        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count//self.ANIMATION_DELAY)%len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))