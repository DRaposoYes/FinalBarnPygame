import pygame
import sys
import math
import random
from pygame.locals import *

pygame.init()

#screen info
FPS = 60
WIDTH, HEIGHT = 1920, 1080

# make game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FinalBarn")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (110, 93, 58)
GREEN = (0, 255, 0)

# Player Info
PLAYER_SPEED = 5
PLAYER_HEALTH = 100  

# Barn Info
BARN_HEALTH = 1000  

#currency
resources = 0

#weapons and upgrades
DAMAGE = 1
PBULLET_SPEED = 10
#cooldowns
pistolAttackCooldown = 0
mp40AttackCooldown = 0
awmAttackCooldown = 0
ak47AttackCooldown = 0
shotgunAttackCooldown = 0
tankAttackCooldown = 0


Shot = False

#weapon menu
pistol_img = pygame.image.load('sprites/weapons/pistol.png').convert_alpha() #1
shotgun_img = pygame.image.load('sprites/weapons/shotgun.png').convert_alpha() #2
mp40_img = pygame.image.load('sprites/weapons/mp40.png').convert_alpha() #3
awm_img = pygame.image.load('sprites/weapons/awm.png').convert_alpha() #4
ak47_img = pygame.image.load('sprites/weapons/ak47.png').convert_alpha() #5
tec9_img = pygame.image.load('sprites/weapons/panzer.png').convert_alpha() #6
tank_img = pygame.image.load('sprites/weapons/tank.png').convert_alpha() #7
cyborg_img = pygame.image.load('sprites/weapons/cyborg.png').convert_alpha() #8
godmode_img = pygame.image.load('sprites/weapons/godmode.png').convert_alpha() #9

pistol_rect = pistol_img.get_rect()
shotgun_rect = shotgun_img.get_rect()
mp40_rect = mp40_img.get_rect()
awm_rect = awm_img.get_rect()
ak47_rect = ak47_img.get_rect()
tec9_rect = tec9_img.get_rect()
tank_rect = tank_img.get_rect()
cyborg_rect = cyborg_img.get_rect()
godmode_rect = godmode_img.get_rect()

pistol_rect.x = 700
pistol_rect.y = 450

shotgun_rect.x = 770
shotgun_rect.y = 450

mp40_rect.x = 840
mp40_rect.y = 450


awm_rect.x = 700
awm_rect.y = 520

ak47_rect.x = 770
ak47_rect.y = 520

tec9_rect.x = 840
tec9_rect.y = 520


tank_rect.x = 700
tank_rect.y = 590

cyborg_rect.x = 770
cyborg_rect.y = 590

godmode_rect.x = 840
godmode_rect.y = 590

#Weapons unlocked set

pistolLock = False
shotgunLock = True
mp40Lock = True
awmLock = True
ak47Lock = True
tec9Lock = True
tankLock = True
cyborgLock = True
godmodeLock = True

#Weapons prices

pistolPrice = 0
shotgunPrice = 30
mp40Price = 200
awmPrice = 400
ak47Price = 800
tec9Price = 1000
tankPrice = 5000
cyborgPrice = 10000
godmodePrice = 50000

#Weapon selected

pistol1 = True
shotgun1 = False
mp401 = False
awm1 = False
ak471 = False
tec91 = False
tank1 = False
cyborg1 = False
godmode1 = False

#ALIEN info
ALIEN_SPEED = 2
ALIEN_DAMAGE = 5
NUM_ALIENS = 5
AlienAttackCooldown = 0
AlienBarnAttackCooldown = 0
ALIEN_SPAWN_MARGIN = 500  # Margin for enemy spawn outside the screen
NUM_ALIENS_PER_WAVE = 3
ALIEN_HEALTH = 2


# Barn render Info
BARN_HEALTH = 1000
barn_img = pygame.image.load('sprites/barn.png').convert_alpha()
barn_rect = barn_img.get_rect()
barn_rect.center = (WIDTH // 2, HEIGHT // 2)  
barnIsHit = False

#explotion render info boom
boom_img = pygame.image.load('sprites/boom.png').convert_alpha()
boom_rect = boom_img.get_rect()

# Player character render info
player_img = pygame.image.load('sprites/handgun.png').convert_alpha()
player_rect = player_img.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)
isPlayerFlipped = False
playerIsHit = False

# Player health
player_health = PLAYER_HEALTH

# Font for displaying player health
font = pygame.font.Font(None, 40)

# Bullet
bullets = []

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = PBULLET_SPEED
        self.angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.rect = pygame.Rect(x, y, 5, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)


# Load enemy image
alien_img = pygame.image.load('sprites/alienflip.png').convert_alpha()
alien_img = pygame.transform.scale(alien_img, (40, 40))

# Alien class
class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = ALIEN_SPEED
        self.health = ALIEN_HEALTH

    def update(self, player_rect, barn_rect):
        # Calculate the angle towards the barn
        if(self.health == 2):
            angle = math.atan2(barn_rect.centery - self.y, barn_rect.centerx - self.x)
        else:
            angle = math.atan2(player_rect.centery - self.y, player_rect.centerx - self.x)
        # Calculate the angle towards the player
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(alien_img, self.rect)        

# Create a list of enemies
aliens = []


# Wave management initial
current_wave = 1
wave_spawn_timer = 0
wave_delay_timer = 0
aliens_to_spawn = NUM_ALIENS_PER_WAVE
WAVE_DELAY_SECONDS = 3


#texture info
ground = pygame.image.load('sprites/ground.png').convert()


# Game loop
clock = pygame.time.Clock()
running = True

#running game & check for shooting & check what gun is used & bullet management / shooting management for enemies
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
#pistol bullet function   
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if pistol1 == True and pistolAttackCooldown == 15:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
                pistolAttackCooldown = 0
#shotgun bullet function        
            if shotgun1 == True and shotgunAttackCooldown == 30:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x + random.randint(-75, 0), target_y + random.randint(-75, 0))
                bullets.append(bullet)

                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)   

                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x + random.randint(0, 75), target_y + random.randint(0, 75))
                bullets.append(bullet)
                shotgunAttackCooldown = 0
#awp bullet function
            if awm1 == True and awmAttackCooldown == 60:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
                awmAttackCooldown = 0
#tec9 bullet function 
            if tec91 == True:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
#tank bullet function 
            if tank1 == True and tankAttackCooldown == 60:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
                tankAttackCooldown = 0
#godmode bullet function 
            if godmode1 == True:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
               

#handle automatic weapons bullets
#mp40 bullet function 
    if pygame.mouse.get_pressed()[0]:
        if mp401 == True:           
            if mp40AttackCooldown == 10:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
                mp40AttackCooldown = 0   
            else:
                mp40AttackCooldown += 1
#ak47 bullet function 
        if ak471 == True:           
            if ak47AttackCooldown == 5:
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet)
                ak47AttackCooldown = 0   
            else:
                ak47AttackCooldown += 1      
#cyborg bullet function     
        if cyborg1 == True:         
                target_x, target_y = pygame.mouse.get_pos()
                bullet = Bullet(player_rect.centerx, player_rect.centery, target_x, target_y)
                bullets.append(bullet) 


##movement and controlls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= PLAYER_SPEED
        isPlayerFlipped = True
    if keys[pygame.K_d]:
        player_rect.x += PLAYER_SPEED
        isPlayerFlipped = False
    if keys[pygame.K_w]:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player_rect.y += PLAYER_SPEED

#switch weapons
    if keys[pygame.K_1]:
        pistol1 = True
        shotgun1 = False
        mp401 = False
        awm1 = False
        ak471 = False
        tec91 = False
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_2]:
        pistol1 = False
        shotgun1 = True
        mp401 = False
        awm1 = False
        ak471 = False
        tec91 = False
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_3]:
        pistol1 = False
        shotgun1 = False
        mp401 = True
        awm1 = False
        ak471 = False
        tec91 = False
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_4]:
        pistol1 = False
        shotgun1 = False
        mp401 = False
        awm1 = True
        ak471 = False
        tec91 = False
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_5]:
        pistol1 = False
        shotgun1 = False
        mp401 = False
        awm1 = False
        ak471 = True
        tec91 = False
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_6]:
        pistol1 = False
        shotgun1 = False
        mp401 = False
        awm1 = False
        ak471 = False
        tec91 = True
        tank1 = False
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_7]:
        pistol1 = False
        shotgun1 = False
        mp401 = False
        awm1 = False
        ak471 = False
        tec91 = False
        tank1 = True
        cyborg1 = False
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

    if keys[pygame.K_8]:
        pistol1 = False
        shotgun1 = False
        mp401 = False
        awm1 = False
        ak471 = False
        tec91 = False
        tank1 = False
        cyborg1 = True
        godmode1 = False

        player_img = pygame.image.load('sprites/handgun.png').convert_alpha()

## update bullet
    for bullet in bullets:
        bullet.update()


## Weapon Management, check what weapon player has and do damage ACORDINGLY
    for alien in aliens:
        for bullet in bullets:
            if alien.rect.colliderect(bullet.rect):
                #pistol
                if pistol1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE
 
                #shotgun
                if shotgun1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 1

                #mp40
                if mp401 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 2

                #awm
                if awm1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 50

                #ak47
                if ak471 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 8

                #tec9
                if tec91 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 1

                #tank
                if tank1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 250
                #cyborg
                if cyborg1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 1

                #godmode
                if godmode1 == True:
                    bullets.remove(bullet)
                    alien.health -= DAMAGE + 400

        if(alien.health <= 0):
            aliens.remove(alien)
            resources += 1




















## Check for enemy-barn collision
    for alien in aliens:
        if barn_rect.colliderect(alien.rect):
            if barnIsHit == False:
                BARN_HEALTH -= ALIEN_DAMAGE
                resources -= 1
                AlienBarnAttackCooldown = 0
                barnIsHit = True

##cooldown for attack so BARN doesnt insta die
    if AlienBarnAttackCooldown == 60:
        barnIsHit = False
    else:
        AlienBarnAttackCooldown += 1
        
#weapon coolcowns
##awm cooldown
    if awmAttackCooldown == 60:
        Shot = False
    else:
        awmAttackCooldown += 1


    if shotgunAttackCooldown == 30:
        Shot = False
    else:
        shotgunAttackCooldown += 1


    if pistolAttackCooldown == 15:
        Shot = False
    else:
        pistolAttackCooldown += 1

    if tankAttackCooldown == 60:
        Shot = False
    else:
        tankAttackCooldown += 1                           

## Check for enemy-player collision
    for alien in aliens:
        if player_rect.colliderect(alien.rect):
            if playerIsHit == False:
                player_health -= ALIEN_DAMAGE
                AlienAttackCooldown = 0
                playerIsHit = True

##cooldown for attack so PLAYER doesnt insta die
    if AlienAttackCooldown == 60:
        playerIsHit = False
    else:
        AlienAttackCooldown += 1


## Update enemies
    for alien in aliens:
        alien.update(player_rect, barn_rect)


##Render ground  surface      
    for y in range(0,1080,32):
        for x in range(0,1920,32):
            screen.blit(ground,(x,y))
    
## Render Barn
    screen.blit(barn_img,barn_rect)

##Check for flipped player
    if(isPlayerFlipped):
        flipped_image = pygame.transform.flip(player_img, True, False)
        screen.blit(flipped_image, player_rect)
    else:
        screen.blit(player_img, player_rect)



## Draw the bullet
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet.rect)

    # Draw enemies
    for alien in aliens:
        alien.draw()

## Show player health
    health_text = font.render(f"Health: {player_health}", True, RED)
    screen.blit(health_text, (10, 10))
    

## Show barn health
    barn_text = font.render(f"Barn Health: {BARN_HEALTH}", True, BROWN)
    screen.blit(barn_text, (1600, 10))

## Show resources text
    rs_text = font.render(f"resources: {resources}", True, GREEN)
    screen.blit(rs_text, (10, 1050))    

## Show wave
    wave_text = font.render(f"wave: {current_wave}", True, BLUE)
    screen.blit(wave_text, (810, 10))


##weapon buy menu Management (Show Price)
    if barn_rect.colliderect(player_rect):

        screen.blit(pistol_img, pistol_rect)
        screen.blit(shotgun_img, shotgun_rect)
        screen.blit(mp40_img, mp40_rect)
        screen.blit(awm_img, awm_rect)
        screen.blit(ak47_img, ak47_rect)
        screen.blit(tec9_img, tec9_rect)
        screen.blit(tank_img, tank_rect)
        screen.blit(cyborg_img, cyborg_rect)
        screen.blit(godmode_img, godmode_rect)

        if pistol_rect.collidepoint(pygame.mouse.get_pos()):
            pistolPrice_text = font.render(f"{pistolPrice}", True, GREEN)
            screen.blit(pistolPrice_text, pistol_rect)

        if shotgun_rect.collidepoint(pygame.mouse.get_pos()):
            shotgunPrice_text = font.render(f"{shotgunPrice}", True, GREEN)
            screen.blit(shotgunPrice_text, shotgun_rect)

        if mp40_rect.collidepoint(pygame.mouse.get_pos()):
            mp40Price_text = font.render(f"{mp40Price}", True, GREEN)
            screen.blit(mp40Price_text, mp40_rect)

        if awm_rect.collidepoint(pygame.mouse.get_pos()):
            awmPrice_text = font.render(f"{awmPrice}", True, GREEN)
            screen.blit(awmPrice_text, awm_rect)

        if ak47_rect.collidepoint(pygame.mouse.get_pos()):
            ak47Price_text = font.render(f"{ak47Price}", True, GREEN)
            screen.blit(ak47Price_text, ak47_rect)

        if tec9_rect.collidepoint(pygame.mouse.get_pos()):
            tec9Price_text = font.render(f"{tec9Price}", True, GREEN)
            screen.blit(tec9Price_text, tec9_rect)

        if tank_rect.collidepoint(pygame.mouse.get_pos()):
            tankPrice_text = font.render(f"{tankPrice}", True, GREEN)
            screen.blit(tankPrice_text, tank_rect)

        if cyborg_rect.collidepoint(pygame.mouse.get_pos()):
            cyborgPrice_text = font.render(f"{cyborgPrice}", True, GREEN)
            screen.blit(cyborgPrice_text, cyborg_rect)

        if godmode_rect.collidepoint(pygame.mouse.get_pos()):
            godmodePrice_text = font.render(f"{godmodePrice}", True, GREEN)
            screen.blit(godmodePrice_text, godmode_rect)








##weapon buy menu Management (functional)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                # Check if the click occurred within the image bounds
                if pistol_rect.collidepoint(event.pos):
                    yes = True
                if shotgun_rect.collidepoint(event.pos):
                    shotgunLock = False                
                if mp40_rect.collidepoint(event.pos):
                    mp40Lock = False
                if awm_rect.collidepoint(event.pos):
                    awmLock = False
                if ak47_rect.collidepoint(event.pos):
                    ak47Lock = False
                if tec9_rect.collidepoint(event.pos):
                    tec9Lock = False
                if tank_rect.collidepoint(event.pos):
                    tankLock = False
                if cyborg_rect.collidepoint(event.pos):
                    cyborgLock = False
                if godmode_rect.collidepoint(event.pos):
                    godmodeLock = False


## Check if ded
    if player_health <= 0:
        running = False
    pygame.display.flip()

## Wave management in game
    if aliens_to_spawn  >= len(aliens) and wave_delay_timer <= 0:
            if aliens_to_spawn > 0:
                if len(aliens) <= 10:
                    x = random.randint(-ALIEN_SPAWN_MARGIN, WIDTH + ALIEN_SPAWN_MARGIN)
                    y = random.randint(-ALIEN_SPAWN_MARGIN, HEIGHT + ALIEN_SPAWN_MARGIN)
                    aliens.append(Alien(x, y))
                    aliens_to_spawn -= 1
                    wave_spawn_timer = 0
            else:
                wave_delay_timer = WAVE_DELAY_SECONDS
                current_wave += 1
                aliens_to_spawn = NUM_ALIENS_PER_WAVE * current_wave

    if wave_delay_timer > 0:
        wave_delay_timer -= 1 / FPS




## Cap the frame rate
    clock.tick(FPS)

# Game overw
game_over_text = font.render("Game Over", True, RED)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
pygame.display.flip()
pygame.time.delay(2)  # Display "Game Over" for 2 seconds before quitting

# Quit the game
pygame.quit()
sys.exit()
