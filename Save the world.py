import pygame, time, random, sys
from pygame.locals import *

DISPLAYHEIGHT, DISPLAYWIDTH = 600,1000
RESOLUTION = (DISPLAYWIDTH, DISPLAYHEIGHT)

# define colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
LAWNGREEN = (124,252,0)
CHARTREUSE = (127,255,0)
LIMEGREEN = (50,205,50)
GOOGLERED = (219, 50, 54)

BGCOLOR = BLACK #Background color

def main():
    global DISPLAYSURF, FPSCLOCK, IMAGESDICT, BASICFONT, MIDFONT, LARGEFONT,\
    FPS, HEALTH, HIGHSCORE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    FPS = 60
    HIGHSCORE = 0
    
    DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Save The World! - A Game by GangofFour")
    
    BASICFONT = pygame.font.Font("freesansbold.ttf",22)
    MIDFONT   = pygame.font.Font("freesansbold.ttf",40)
    LARGEFONT = pygame.font.Font("freesansbold.ttf",100)

    IMAGESDICT = {'bgimage': pygame.image.load('images/bgi.jpg'),
                  'flames' : pygame.image.load('images/flame.png'),
                  'ship'   : pygame.image.load("images/ship.png"),
                  'meteor' : pygame.image.load("images/meteor.png"),
                  'health' : pygame.image.load("images/healthimg.png")}
                  
    
    while True:    
        startScreen()
        game_loop()

def startScreen():
    FIREBALLCOUNT = 7 # number of fireballs displayed on start screen
    FIREBALLVELOCITY = 2 # speed of fireball displayed on start screen

    bgimage = IMAGESDICT['bgimage']
    bgimage = pygame.transform.scale(bgimage,RESOLUTION) # fit image to screen
    
    INSTRUCTIONS  = ["Press ESC to quit at any time",
                     "Press SPACE to pause",
                     "Press ENTER key to continue...",
                     "Tip : Dodge the meteors to increase score"]
    
#    fontObj = pygame.font.Font("freesansbold.ttf",100)
    titleText = LARGEFONT.render("Save the World",True,GOOGLERED)
    titleRect = titleText.get_rect()
    topCoord = DISPLAYHEIGHT//2 - titleRect.height-50
    titleRect.top = topCoord
    titleRect.centerx = DISPLAYWIDTH//2
    topCoord+=titleRect.height + 20
    
    displayText = []
    displayTextPos = []
    
    for i in range(len(INSTRUCTIONS)):
        displayText.append(BASICFONT.render(INSTRUCTIONS[i],True,BLACK))
        displayTextPos.append(displayText[i].get_rect())
        displayTextPos[i].center = (DISPLAYWIDTH//2,topCoord)
        topCoord+=displayTextPos[i].height
        
    # theme music
    pygame.mixer.music.load('sounds/theme.mp3')
    pygame.mixer.music.play(-1,0.0)

#    smallFireballsSize = tuple([i//3 for i in IMAGESDICT['meteor'].get_size()])
    midFireballsSize = tuple([i//2 for i in IMAGESDICT['meteor'].get_size()])
    
    
    fireballs = create_fireballs(FIREBALLCOUNT,FIREBALLVELOCITY/2)
    fireballs2 = create_fireballs(FIREBALLCOUNT,FIREBALLVELOCITY/4)
    for i in range(FIREBALLCOUNT):
#        fireballs[i].image = pygame.transform.scale(fireballs[i].image,\
#                 midFireballsSize)
        fireballs2[i].image = pygame.transform.scale(fireballs2[i].image,\
                  midFireballsSize)
    
    
    while True: #Main loop for the start screen
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(bgimage,bgimage.get_rect())

        for i in range(FIREBALLCOUNT):
            fireballs[i].move()
            fireballs2[i].move()

            if fireballs[i].position_y >= DISPLAYHEIGHT:
                fireballs[i].update_position()
            if fireballs2[i].position_y >= DISPLAYHEIGHT:
                fireballs2[i].update_position()
            

            DISPLAYSURF.blit(fireballs[i].image, (fireballs[i].position_x, fireballs[i].position_y))
            DISPLAYSURF.blit(fireballs2[i].image, (fireballs2[i].position_x, fireballs2[i].position_y))

        DISPLAYSURF.blit(titleText,titleRect)

        for i in range(len(displayText)):
            DISPLAYSURF.blit(displayText[i],displayTextPos[i])

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RETURN:
                    pygame.mixer.music.stop()
                    return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def pauseGame():
    '''Pauses game and returns on pressing SPACE key '''
    
    pauseText = LARGEFONT.render("PAUSED",True,WHITE)

    textRect  = pauseText.get_rect()
    textRect.center = (DISPLAYWIDTH//2,DISPLAYHEIGHT//2)

    DISPLAYSURF.blit(pauseText,textRect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return
                
def DisplayFirewall():
    WallLeft  = IMAGESDICT['flames']
    WallRight = IMAGESDICT['flames']
    WallRight  = pygame.transform.flip(WallRight,1,0)
    
    LeftPos  = (0,50)
    RightPos = (DISPLAYWIDTH - WallRight.get_size()[0],50)

    DISPLAYSURF.blit(WallLeft,LeftPos)
    DISPLAYSURF.blit(WallRight,RightPos)
    
class plane:
    def __init__(self):
        self.image = IMAGESDICT['ship']
        self.width, self.height = self.image.get_size()
        
    def planeRender (self,x,y):
        DISPLAYSURF.blit(self.image,(x,y))

class fireball:
    def __init__(self,velocity):
        self.image = IMAGESDICT['meteor']
        self.width, self.height = self.image.get_size()
        self.position_y = -self.height
        self.position_x = random.randint(50, DISPLAYWIDTH - self.width - 50)
        self.velocity = velocity

    def update_position(self):
        """
        Updates the position of fireballs from downside of screen to top of screen
        """
        self.position_y = -random.randint(self.height - 10,self.height + 10)
        self.position_x = random.randint(50, DISPLAYWIDTH - self.width - 50)

    def move(self):
        """
        Moves the fireballs downwards
        """
        self.position_y += self.velocity

    def display(self):
        DISPLAYSURF.blit(self.image, (self.position_x, self.position_y))

def create_fireballs(count,velocity):
    """
    Returns a list of count fireballs
    """
    fireballs = []
    for i in range(count):
        fireballs.append(fireball(velocity))
        fireballs[i].position_y -= (i+1) * (DISPLAYHEIGHT // count)

    return fireballs

def TextRender(text,font,color,position):
    textSurf = font.render(text,True,color)
    textRect = textSurf.get_rect()
    textRect.center = position
    DISPLAYSURF.blit(textSurf,textRect)
    
# main game loop
# anything after the game has started is written inside this loop
def game_loop():
    global HIGHSCORE
    
    HEALTH = 3
    LEVELGRAD = 2 # speed of meteors changes by this amount when level increases 
    currentScore = 0

    FIREBALLCOUNT = 4
    FIREBALLVELOCITY = 5

    Healthimg = IMAGESDICT['health']
    
    jet = plane()
    
    MIDFONTHEIGHT = MIDFONT.get_height()

    xchange = 0
    crashSound = pygame.mixer.Sound('sounds/explodedeath.wav')
    CrashText = "YOU CRASHED!"
    
    while HEALTH > 0:
        pygame.mixer.music.load('sounds/game.mp3')
        pygame.mixer.music.set_volume(.7)
        pygame.mixer.music.play(-1,0.0)
                
        fireballs = create_fireballs(FIREBALLCOUNT,FIREBALLVELOCITY)
        game_level = 1
        JetSpeed = 8
        
        x = DISPLAYWIDTH/2 - jet.width/2
        y = DISPLAYHEIGHT - jet.height - 10

        isCrashed = False
        while not isCrashed:
            DISPLAYSURF.fill(BLACK)
            
            DisplayFirewall()
            # displays score , level , highscore
            TextRender('Score: ',MIDFONT,WHITE,(70,MIDFONTHEIGHT//2+5))
            # not combined with above line intentionally
            TextRender(str(currentScore),MIDFONT,WHITE,(170,MIDFONTHEIGHT//2+5)) 
            
            TextRender('Level:  ' + str(game_level),MIDFONT,WHITE,(DISPLAYWIDTH//2,MIDFONTHEIGHT//2+5))
            
            TextRender('Highscore: ',MIDFONT,WHITE,(DISPLAYWIDTH - 180,MIDFONTHEIGHT//2+5))
            TextRender(str(HIGHSCORE),MIDFONT,WHITE,(DISPLAYWIDTH - 30,MIDFONTHEIGHT//2+5))
            
            for i in range(HEALTH):
                DISPLAYSURF.blit(Healthimg,(200 + (i*45),(0)))
            
            for i in range(FIREBALLCOUNT): # renders fireballs
                fireballs[i].move()
    
                if fireballs[i].position_y >= DISPLAYHEIGHT:
                    fireballs[i].update_position()
                    currentScore +=1
                    if currentScore > HIGHSCORE:
                        HIGHSCORE = currentScore
                    if (currentScore) % 20 == 0:
                        game_level += 1
                        JetSpeed += 1
                        levelSound = pygame.mixer.Sound('sounds/healthup.wav')
                        levelSound.set_volume(1.0)
                        levelSound.play()
                        for i in range(4):
                            fireballs[i].velocity+= LEVELGRAD
                # Only display below score and health bar
                if fireballs[i].position_y > 40:
                    DISPLAYSURF.blit(fireballs[i].image, (fireballs[i].position_x, fireballs[i].position_y))
            jet.planeRender(x,y)
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        pauseGame()
                    elif event.key == K_ESCAPE:
                        terminate()
                    elif event.key == pygame.K_LEFT :
                        xchange = -JetSpeed
                    elif event.key == pygame.K_RIGHT:
                        xchange = JetSpeed
    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        xchange = 0
            x = x + xchange
            if x < 50 or x > DISPLAYWIDTH - jet.width - 50:
                isCrashed = True
            else:    
                for i in range(4):
                    if (fireballs[i].position_y + fireballs[i].height > y \
                        and fireballs[i].position_y < y + jet.height):
                            if not (x >= fireballs[i].position_x + fireballs[i].width \
                                    or x + jet.width <= fireballs[i].position_x ) :
                                isCrashed = True
            if isCrashed:
                pygame.mixer.music.stop()
                HEALTH -= 1
                crashSound.play()
                if HEALTH <= 0:
                    CrashText = "GAME OVER"
                    textSurf = LARGEFONT.render("Score: "+ str(currentScore),True,WHITE)
                    textRect = textSurf.get_rect()
                    textRect.center = ((DISPLAYWIDTH//2),(DISPLAYHEIGHT//2 + textRect.height))
                    DISPLAYSURF.blit(textSurf,textRect)
                
                textSurf = LARGEFONT.render(CrashText,True,WHITE)
                textRect = textSurf.get_rect()
                textRect.center = ((DISPLAYWIDTH//2),(DISPLAYHEIGHT//2))
                DISPLAYSURF.blit(textSurf,textRect)
    
                pygame.display.update()        
                time.sleep(2)
                
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
