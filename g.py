# Import packages
import pygame
from pygame.locals import *
import math
import random

# Initialize the game
exitcode = 1
def game():
    pygame.init()
    width, height = 640, 480
    screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    keys = [False, False, False, False]
    playerpos=[50,400]
    acc=[0,0]
    arrows=[]
    badtimer=100
    badtimer1=0
    badguys=[[640,100]]
    healthvalue=194
    score = 0
    running = 1
    exitcode = 0
    pygame.mixer.init()

    # Load assets

    player = pygame.image.load("resources/images/dude2.png")
    grass = pygame.image.load("resources/images/tileSand1.png")

    arrow = pygame.image.load("resources/images/bullet.png")
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    badguyimg=badguyimg1
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    gameover = pygame.image.load("resources/images/gameover.png")
    youwin = pygame.image.load("resources/images/youwin.png")
    # 3.1 - Load audio
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    # keep looping through
    while running:
        badtimer-=1
        # clear the screen before drawing it again
        screen.fill(0)
        # draw the player on the screen
        for x in range(width/grass.get_width()+1):
            for y in range(height/grass.get_height()+1):
                screen.blit(grass,(x*100,y*100))

        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1)
        # 6.2 - Draw arrows
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                arrows.pop(index)
            index+=1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
        # Draw badgers
        if badtimer==0:
            badguys.append([random.randint(200,640), random.randint(50,430)])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
        index=0
        for badguy in badguys:
            if badguy[0]<-64:
                badguys.pop(index)
            badguy[0]-=7
            # Attack player
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if (badrect.left <= playerpos[0]+50 and badrect.left >= playerpos[0]-50 and badrect.top <= playerpos[1]+50 and badrect.top >= playerpos[1]-50):
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.pop(index)
            # Check for collisions
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    try:
                        badguys.pop(index)
                    except:
                        pass
                    arrows.pop(index1)
                    score+=1
                index1+=1
            # Next bad guy
            index+=1
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
        # Show Score
        font = pygame.font.Font(None, 24)
        scoretext = font.render(str(score), True, (0,0,0))
        textRect = scoretext.get_rect()
        textRect.topright=[635,5]
        screen.blit(scoretext, textRect)
        # Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
        # update the screen
        pygame.display.flip()
        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True
                elif event.key==K_q:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position=pygame.mouse.get_pos()
                acc[1]+=1
                arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])

        # 9 - Move player
        if keys[0]:
            playerpos[1]-=5
        elif keys[2]:
            playerpos[1]+=5
        if keys[1]:
            playerpos[0]-=5
        elif keys[3]:
            playerpos[0]+=5

        if healthvalue<=0:
            running=0
            exitcode=0

    # Win/lose display
    if exitcode==0:
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Score: "+str(score), True, (255,0,0))
        mesg = font.render("Press SPACEBAR to play again", True, (255,0,0));
        textRect = text.get_rect()
        mesgRect = mesg.get_rect()
        textRect.centerx = screen.get_rect().centerx
        mesgRect.centerx = screen.get_rect().centerx
        mesgRect.centery = screen.get_rect().centerx+30
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (0,0))
        screen.blit(text, textRect)
        screen.blit(mesg, mesgRect)
game()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                game()
    pygame.display.flip()
