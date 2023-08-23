from cmu_112_graphics import *
import random, math, copy

def main():
    runApp(width=600, height=800)

# helper functions 

# from hw. 1
def distance(x1, y1, x2, y2):
    xDist = x2 - x1
    yDist = y2 - y1
    return (xDist ** 2 + yDist ** 2) ** 0.5

# https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

#fish class and subclasses

class Fish():
    def __init__(self, depth, xPos, app):
        self.depth = depth
        self.spawnedDepth = depth + app.spawnDepth
        self.xPos = xPos
        self.swimCounter = 0

    def __eq__(self, other):
        return (isinstance(other, Fish) and (self.name == other.name))

    def __hash__(self):
        return hash(self.name)

    #if the fish is moving to the right draw the fish facing the right
    def drawFish(self, canvas):
        if self.speed >= 0 and not isinstance(self, Bomb):
            canvas.create_image(self.xPos+self.size[0]/2, 
                                self.depth+self.size[1]/2, 
            image = ImageTk.PhotoImage(self.imageRight[self.swimCounter//10]))
    #if moving left, face left
        elif not isinstance(self, Bomb):
            canvas.create_image(self.xPos+self.size[0]/2, 
                                self.depth+self.size[1]/2, 
            image = ImageTk.PhotoImage(self.imageLeft[self.swimCounter//10]))
 #bomb is only 1 image so we can't index into the drawing list like other fish
        else:
            canvas.create_image(self.xPos+self.size[0]/2, 
                                self.depth+self.size[1]/2, 
                image = ImageTk.PhotoImage(self.imageLeft[0]))

    def drawFishOnHook(self, app, canvas):
        self.swimCounter += 1
        if self.swimCounter == 30:
            self.swimCounter = 0
        canvas.create_image(app.hook.hookPos[0], 
                            app.hook.hookPos[1]+self.size[0]/2,
            image = ImageTk.PhotoImage(self.reelingImage[self.swimCounter//10]))

    def moveFish(self, app):
        # every 10 times the fish is moved the animation resets
        self.swimCounter += 1
        if self.swimCounter == 30:
            self.swimCounter = 0
        self.xPos += self.speed
        self.depth -= app.dropSpeed
        self.avoidHook(app)
        # if at the edge, reverse the velocity
        if self.xPos >= app.width+self.size[0]:
            self.speed = -self.speed
        elif self.xPos <= -self.size[0]:
            self.speed = -self.speed

    def avoidHook(self, app):
        if isinstance(self, Bomb):
            return 
        if app.width < self.xPos < 0:
            return
        # if the fish can see the hook it will swim away from it if it's behind
        # the hook else it will slow down to avoid the hook
        if (distance(self.xPos+self.size[0], self.depth+self.size[1], 
            app.hook.hookPos[0], app.hook.hookPos[1]) < self.visionDistance):
            if self.xPos > app.hook.hookPos[0] and self.speed > 0:
                self.speed =  max(self.speedRange)
            elif self.xPos > app.hook.hookPos[0] and self.speed <= 0:
                self.speed = -min(self.speedRange)
            elif app.hook.hookPos[0] > self.xPos and self.speed > 0:
                self.speed = min(self.speedRange)
            elif app.hook.hookPos[0] > self.xPos and self.speed <= 0:
                self.speed = -max(self.speedRange)

    def getScore(self):
        return self.scoreValue

class YellowTang(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (1.8*difficultyMultiplier, 3.2*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 500
        self.rarity = 40
        self.minDepth = 0
        self.size = (57,30)
        self.color = "Yellow"
        self.scoreValue = math.ceil(100*difficultyMultiplier)
        self.imageRight = app.yellowTangRightAll
        self.imageLeft = app.yellowTangLeftAll
        self.reelingImage = app.yellowTangReelingAll
        self.weight = 7
        self.name = 'Yellow Tang'
        self.rarityLevel = 'Common'

class Bass(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (2.4*difficultyMultiplier, 3.8*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 700
        self.rarity = 34
        self.minDepth = 50
        self.size = (75,30)
        self.color = "blue"
        self.scoreValue = math.ceil(300*difficultyMultiplier)
        self.imageRight = app.bassRightAll
        self.imageLeft = app.bassLeftAll
        self.reelingImage = app.bassReelingAll
        self.weight = 10
        self.name = 'Bass'
        self.rarityLevel = 'Uncommon'

class MolaMola(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (2.7*difficultyMultiplier, 4.1*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 700
        self.rarity = 30 
        self.minDepth = 100
        self.size = (70,30)
        self.color = "gray"
        self.scoreValue = math.ceil(400 * difficultyMultiplier)
        self.imageRight = app.molaMolaRightAll
        self.imageLeft = app.molaMolaLeftAll
        self.reelingImage = app.molaMolaReelingAll
        self.weight = 15
        self.name = 'Mola Mola'
        self.rarityLevel = 'Uncommon'

class Tuna(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (3.3*difficultyMultiplier, 4.7*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 900
        self.rarity = 20
        self.minDepth = 750
        self.size = (70,50)
        self.color = "dodger blue"
        self.scoreValue = math.ceil(500 * difficultyMultiplier)
        self.imageRight = app.tunaRightAll
        self.imageLeft = app.tunaLeftAll
        self.reelingImage = app.tunaReelingAll
        self.weight = 13
        self.name = 'Tuna'
        self.rarityLevel = 'Rare'

class Bomb(Fish): 
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speed = 0
        self.rarity = 25
        self.minDepth = 150
        self.size = (50,50)
        self.color = 'black'
        self.imageRight = app.bombDrawing
        self.imageLeft = app.bombDrawing

class Sturgeon(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (6.3*difficultyMultiplier, 7.7*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 1000
        self.rarity = 15
        self.minDepth = 1600
        self.size = (80,20)
        self.color = "green"
        self.scoreValue = math.ceil(1000 * difficultyMultiplier)
        self.imageRight = app.sturgeonRightAll
        self.imageLeft = app.sturgeonLeftAll
        self.reelingImage = app.sturgeonReelingAll
        self.weight = 9
        self.name = 'Sturgeon'
        self.rarityLevel = 'Legendary'

class Angelfish(Fish):
    def __init__(self, depth, xPos, difficultyMultiplier, app):
        super().__init__(depth, xPos, app)
        self.speedRange = (8.3*difficultyMultiplier, 9.7*difficultyMultiplier)
        self.speed = random.uniform(self.speedRange[0], self.speedRange[1])
        self.visionDistance = 1000
        self.rarity = 12
        self.minDepth = 2000
        self.size = (40,15)
        self.color = "white"
        self.scoreValue = math.ceil(5000 * difficultyMultiplier)
        self.imageRight = app.angelfishRightAll
        self.imageLeft = app.angelfishLeftAll
        self.reelingImage = app.angelfishReelingAll
        self.weight = 5
        self.name = 'Angelfish'
        self.rarityLevel = 'Mythic'

#button class

class Button():
    def __init__(self, x0, y0, x1, y1, color, text, fill, finalCall):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.text = text
        self.fill = fill
        self.finalCall = finalCall
    
    def isPressed(self, x, y):
        if (x >= self.x0 and y >= self.y0 and
            x <= self.x1 and y <= self.y1):
            return True
        else:
            return False

    def drawButton(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1,
                                fill = self.color)
        canvas.create_text((self.x0+self.x1)/2, (self.y0+self.y1)/2,
                                text = self.text, fill = self.fill, 
                                font = 'FreeMono')

#helper funtions for tkinter

def getFishAssets(app, bonusFish, bonusScore):
    app.spawnDepth = 0
    app.allFish = [YellowTang, Bass, MolaMola,
                     Bomb, Tuna, Sturgeon, Angelfish]
    app.allCatchables = [YellowTang, Bass, MolaMola, Tuna, Sturgeon, Angelfish]
    if bonusFish == None:
        app.bonusFish = [set(), []]
        app.bonusScore = 0
        while len(app.bonusFish[0]) < 3:
            fish = app.allCatchables[random.randint(0,5)]
            app.bonusFish[0].add(fish)
            app.bonusFish[1].append(fish)
        for fish in app.bonusFish[0]:
            app.bonusScore += fish(0,0,1,app).getScore()
    else: 
        app.bonusFish = bonusFish
        app.bonusScore = bonusScore    
    app.fish = []
    app.fishTime = 39

def getHookAssets(app):
    app.dropSpeed = 2
    allHooks = [EasyHook, MediumHook, HardHook]
    app.hook = allHooks[app.difficulty](app, [153, app.height/2], 
                                        16-6*app.difficulty)
    app.caught = []
    app.depth = app.height/2
    app.isExplosion = False
    app.explosionTime = 0
    app.explosionSize = 1

def getStartScreenAssets(app):
    app.startScreen = StartScreen(app)
    app.waterShift = 0

def getScoreBoardAssets(app):
    app.leaderBoard = ScoreBoard(app)
    app.getName = False
    app.scoreBoardFish = [
            Sturgeon(app.height/2, random.randint(0,app.width), 1, app), 
            Tuna(app.height/10, random.randint(0,app.width), 1, app),
            Angelfish(app.height*3/5, random.randint(0,app.width), 1, app)]

def getAllImages(app):
    #all fish images from 
    #https://forums.rpgmakerweb.com/index.php?threads/whtdragons-animals-and-running-horses-now-with-more-dragons.53552/
    getYellowTangImages(app)
    getBassImages(app)
    getMolaMolaImages(app)
    getTunaImages(app)
    #bomb image from 
    #https://www.giantbomb.com/minesweeper/3030-4032/images/
    #application to remove backgorund and make transparent
    #https://express.adobe.com/tools/remove-background? 
    #explosion image from
    #http://pixelartmaker.com/art/370776acb20eed7 
    getBombImages(app)
    getSturgeonImages(app)
    getAngelfishImages(app)
    #boat image from 
    #https://sproutson.tumblr.com/post/143297511017/some-pixels-of-the-boys-and-their-boat
    app.boatImage = app.loadImage('Boat.png')

#for all getFish functions, import the sprite sheet, crop all images for swiming
#animations and add them to list and scale them as needed

def getYellowTangImages(app):
    app.yellowTangSprite = app.loadImage('YellowTang.png')
    yellowTangRight1 = app.yellowTangSprite.crop(( 0,198,32,222))
    yellowTangRight2 = app.yellowTangSprite.crop((32,198,64,222))
    yellowTangRight3 = app.yellowTangSprite.crop((64,198,96,222))
    app.yellowTangRightAll =[yellowTangRight1,yellowTangRight2,yellowTangRight3]
    yellowTangReeling1 = app.yellowTangSprite.crop(( 0,223,32,255))
    yellowTangReeling2 = app.yellowTangSprite.crop((32,223,64,255))
    yellowTangReeling3 = app.yellowTangSprite.crop((64,223,96,255))
    app.yellowTangReelingAll = [yellowTangReeling1,yellowTangReeling2,
                                                    yellowTangReeling3]
    for i in range(len(app.yellowTangRightAll)):
        app.yellowTangRightAll[i] = app.scaleImage(app.yellowTangRightAll[i], 2)
    for i in range(len(app.yellowTangReelingAll)): 
        app.yellowTangReelingAll[i] = (
                            app.scaleImage(app.yellowTangReelingAll[i], 2))
    app.yellowTangLeftAll = []
    for i in range(len(app.yellowTangRightAll)):
        app.yellowTangLeftAll.append(
                    app.yellowTangRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))

def getBassImages(app):
    app.bassSprite = app.loadImage('Bass.png')
    bassRight1 = app.bassSprite.crop((285,311,333,332))
    bassRight2 = app.bassSprite.crop((333,311,381,332))
    bassRight3 = app.bassSprite.crop((381,311,429,332))
    app.bassRightAll = [bassRight1, bassRight2, bassRight3]
    bassReeling1 = app.bassSprite.crop((285,338,333,377))
    bassReeling2 = app.bassSprite.crop((333,338,381,377))
    bassReeling3 = app.bassSprite.crop((381,338,429,377))
    app.bassReelingAll = [bassReeling1, bassReeling2, bassReeling3]
    for i in range(len(app.bassRightAll)):
        app.bassRightAll[i] = app.scaleImage(app.bassRightAll[i], 2)
    for i in range(len(app.bassReelingAll)):
        app.bassReelingAll[i] = app.scaleImage(app.bassReelingAll[i], 2)
    app.bassLeftAll = []
    for i in range(len(app.bassRightAll)):
        app.bassLeftAll.append(
                        app.bassRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))

def getMolaMolaImages(app):
    app.molaMolaSprite = app.loadImage('MolaMola.png')
    molaMolaRight1 = app.molaMolaSprite.crop((156,201,208,279))
    molaMolaRight2 = app.molaMolaSprite.crop((208,201,260,279))
    molaMolaRight3 = app.molaMolaSprite.crop((260,201,312,279))
    app.molaMolaRightAll = [molaMolaRight1, molaMolaRight2, molaMolaRight3]
    molaMolaReeling1 = app.molaMolaSprite.crop((156,292,208,356))
    molaMolaReeling2 = app.molaMolaSprite.crop((208,292,260,356))
    molaMolaReeling3 = app.molaMolaSprite.crop((260,292,312,356))
    app.molaMolaReelingAll = [molaMolaReeling1, molaMolaReeling2, 
                            molaMolaReeling3]
    for i in range(len(app.molaMolaRightAll)):
        app.molaMolaRightAll[i] = app.scaleImage(app.molaMolaRightAll[i], 1.3)
    for i in range(len(app.molaMolaReelingAll)):
        app.molaMolaReelingAll[i] = app.scaleImage(
                                            app.molaMolaReelingAll[i], 1.3)
    app.molaMolaLeftAll = []
    for i in range(len(app.molaMolaRightAll)):
        app.molaMolaLeftAll.append(
                    app.molaMolaRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))
    
def getTunaImages(app):
    app.tunaSprite = app.loadImage('Tuna.png')
    tunaRight1 = app.tunaSprite.crop(( 0,70,32,100))
    tunaRight2 = app.tunaSprite.crop((32,70,64,100))
    tunaRight3 = app.tunaSprite.crop((64,70,96,100))
    app.tunaRightAll = [tunaRight1, tunaRight2, tunaRight3]
    tunaReeling1 = app.tunaSprite.crop(( 0,105,32,122))
    tunaReeling2 = app.tunaSprite.crop((32,105,64,122))
    tunaReeling3 = app.tunaSprite.crop((64,105,96,122))
    app.tunaReelingAll = [tunaReeling1, tunaReeling2, tunaReeling3]
    for i in range(len(app.tunaRightAll)):
        app.tunaRightAll[i] = app.scaleImage(app.tunaRightAll[i], 4)
    for i in range(len(app.tunaReelingAll)):
        app.tunaReelingAll[i] = app.scaleImage(app.tunaReelingAll[i], 4)
    app.tunaLeftAll = []
    for i in range(len(app.tunaRightAll)):
        app.tunaLeftAll.append(
                        app.tunaRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))

def getBombImages(app):
    app.bombDrawing = app.loadImage('mineTransparent.png')
    app.bombDrawing = [app.scaleImage(app.bombDrawing, 1/7)]
    app.explosionImage = app.loadImage('Explosion.png')

def getSturgeonImages(app):
    app.sturgeonSprite = app.loadImage('Sturgeon.png')
    sturgeonRight1 = app.sturgeonSprite.crop((864,220,960,265))
    sturgeonRight2 = app.sturgeonSprite.crop((960,220,1056,265))
    sturgeonRight3 = app.sturgeonSprite.crop((1056,220,1152,265))
    app.sturgeonRightAll = [sturgeonRight1, sturgeonRight2, sturgeonRight3]
    sturgeonReeling1 = app.sturgeonSprite.crop((864,294,960,373))
    sturgeonReeling2 = app.sturgeonSprite.crop((960,294,1056,373))
    sturgeonReeling3 = app.sturgeonSprite.crop((1056,294,1152,373))
    app.sturgeonReelingAll = [sturgeonReeling1, 
                            sturgeonReeling2, sturgeonReeling3]
    for i in range(len(app.sturgeonRightAll)):
        app.sturgeonRightAll[i] = app.scaleImage(app.sturgeonRightAll[i], 1)
    for i in range(len(app.sturgeonReelingAll)):
        app.sturgeonReelingAll[i] = app.scaleImage(app.sturgeonReelingAll[i], 1)
    app.sturgeonLeftAll = []
    for i in range(len(app.sturgeonRightAll)):
        app.sturgeonLeftAll.append(
                    app.sturgeonRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))

def getAngelfishImages(app):
    app.angelfishSprite = app.loadImage('Angelfish.png')
    angelfishRight1 = app.angelfishSprite.crop((288,290,336,325))
    angelfishRight2 = app.angelfishSprite.crop((336,290,384,325))
    angelfishRight3 = app.angelfishSprite.crop((384,290,432,325))
    app.angelfishRightAll = [angelfishRight1, angelfishRight2, angelfishRight3]
    angelfishReeling1 = app.angelfishSprite.crop((288,338,336,363))
    angelfishReeling2 = app.angelfishSprite.crop((336,338,384,363))
    angelfishReeling3 = app.angelfishSprite.crop((384,338,432,363))
    app.angelfishReelingAll = [angelfishReeling1, angelfishReeling2, 
                            angelfishReeling3]
    for i in range(len(app.angelfishRightAll)):
        app.angelfishRightAll[i] = app.scaleImage(app.angelfishRightAll[i], 2)
    for i in range(len(app.angelfishReelingAll)):
        app.angelfishReelingAll[i] = app.scaleImage(
                                                app.angelfishReelingAll[i], 2)
    app.angelfishLeftAll = []
    for i in range(len(app.angelfishRightAll)):
        app.angelfishLeftAll.append(
                    app.angelfishRightAll[i].transpose(Image.FLIP_LEFT_RIGHT))

def createFish(app):
    if app.dropSpeed < 0:
        return 
    difficultyMultiplier = 0.75 + app.difficulty*.25
    canSpawn = 0
    # if the depth is deep enough, for the fish, the fish is "spawnable"
    for fish in range(len(app.allFish)):
        if app.spawnDepth > app.allFish[fish](0,0,1,app).minDepth:
            canSpawn += 1
    totalRange, spawnables = raritySpawnHelper(app, canSpawn)
    spawned = random.randint(0, totalRange)
    #pick a random number to determine which fish is spawned
    app.fish.append(spawnables[spawned-1]
    (random.randint(app.height,2*app.height), random.randint(0,app.width),
     difficultyMultiplier,app))

def raritySpawnHelper(app, canSpawn):
    totalRange = 0
    spawnables = []
    #makes a list containing fish and adds to it based on how rare each fish is
    for fish in range(canSpawn):
        totalRange += app.allFish[fish](0,0,1,app).rarity
        rarity = app.allFish[fish](0,0,1,app).rarity
        spawnables += [app.allFish[fish]] * rarity
    return totalRange, spawnables

def drawExplosion(app, canvas, bomb):
    canvas.create_image(bomb.xPos+25, bomb.depth+25,
                    image = ImageTk.PhotoImage(app.explosionImage))

def drawInfoPage(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='saddle brown')
    canvas.create_text(app.width/4,app.height/8,
                        text = 'Known Fish:', fill = 'gray74')
    difficultyMultiplier = 0.75 + app.difficulty*.25
    yellowTang = YellowTang(0,0,difficultyMultiplier,app)
    bass = Bass(0,0,difficultyMultiplier,app)
    molaMola = MolaMola(0,0,difficultyMultiplier,app)
    tuna = Tuna(0,0,difficultyMultiplier,app)
    sturgeon = Sturgeon(0,0,difficultyMultiplier,app)
    angelfish = Angelfish(0,0,difficultyMultiplier,app)
    fish = [yellowTang, bass, molaMola, tuna, sturgeon, angelfish]
    for i in range(len(fish)):
        canvas.create_image(app.width/6, app.height/4+100*i,
                        image = ImageTk.PhotoImage(fish[i].imageRight[1]))
        canvas.create_text(app.width/2.5, app.height/4+100*i,
                        text = 
f'''    Name: {fish[i].name}
    Minimum Depth: {(fish[i].minDepth+app.height//2)//17} meters
    Weight: {fish[i].weight} pounds
    Score Value: {fish[i].scoreValue}
    Rarity: {fish[i].rarityLevel}''', fill = 'gray74')
    canvas.create_text(app.width*3/4,app.height/2+40,
                        text = 'Watch Out For Mines', fill = 'gray74')
    canvas.create_image(app.width*3/4,app.height/2+100,
                        image = ImageTk.PhotoImage(app.bombDrawing[0]))
    canvas.create_text(app.width*3/4,app.height/8,
                        text = 'How to Play:', fill = 'gray74')
    canvas.create_text(app.width*3/4,app.height/3,
                        text = 
'''Move your mouse cursor to control
the hook. Avoid obsticles and catch 
as many fish as possible before time
runs out. If you have caught 5 fish
you will recast your line and start
again. Be careful because the more 
fish you have on your hook the slower
you can reel the line. Hitting a mine 
will reset all of your progress! If 
you catch all of the fish from the 
special order, you will be rewarded 
with a bonus score. 

       Good luck, and have fun!
''', fill = 'gray74')

def drawScoreAndTimer(app, canvas):
    canvas.create_text(app.width/2, 50, text = f'{app.score} points')
    canvas.create_text(app.width/2, 75, 
                    text = f'{int(app.gameTimer//29.4)} seconds left')
    canvas.create_text(app.width/2, 100, 
                        text = f'{int(app.spawnDepth//17)} meters')

######## IMPORTANT ######## If the game is laggy increase step
def drawSineWave(x0, y0, x1, y1, amplitude, shift, color, canvas, step=1):
    #loop through width of the rectangle given and draw trapizoids to represent
    #the wave
    for i in range(x0, x1, step):
        canvas.create_polygon(i, math.sin(i*math.pi/180+shift)*
                    amplitude+y0, i+step, 
                    math.sin((i+step)*math.pi/180+shift)*amplitude+y0, 
                    i+step, y1, i, y1, fill=color)

def drawNameGetter(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'gray2')
    canvas.create_text(app.width/2, app.height/4, text = 'Enter Your Name',
                    font = 'FreeMono', fill = 'white')
    canvas.create_line(app.width/4, app.height*2/3, 
                    app.width*3/4, app.height*2/3, fill = 'white')
    canvas.create_text(app.width/2, app.height*2/3-25, text = app.name, 
                    font = 'FreeMono', fill = 'white')

def getTheName(app, event):
    if event.key == ('Return' or 'Enter'): 
        app.getName = False
    elif event.key == 'Space':
        app.name += ' '
    elif event.key == ('BackSpace' or 'Backspace'): 
        app.name = app.name[0:-1]
    else:
        app.name += event.key

def gameIsOver(app):
    app.leaders = app.leaderBoard.getScoreLeaders(app, app.leaders)
    app.dropSpeed = 0
    for fish in app.scoreBoardFish:
        if fish.speed > 0:
            fish.speed = 4
        else: fish.speed = -4
        fish.moveFish(app)

def moveAllFish(app):
    #loop through all spawned fish 
    for fish in range(len(app.fish)):
        if app.hook.checkCollision(app.fish[fish]):
            #if we hit a bomb, we will move the explosion
            if isinstance(app.fish[fish], Bomb):
                if app.explosionTime % 8 == 0:
                    app.explosionSize += .1
                    app.explosionImage = app.scaleImage(app.explosionImage, 
                                                    app.explosionSize)
                app.explodedBomb = app.fish[fish]
                app.isExplosion = True
                app.explosionTime += 1
                app.dropSpeed = 0
                if app.explosionTime == 40:
                    app.bonusFish[0] = set(app.bonusFish[1])
                    app.bonusScore = 0
                    # reset progress on the special order
                    for fish in app.bonusFish[0]:
                        app.bonusScore += fish(0,0,1,app).getScore()
                    appStarted(app, 0, app.gameTimer, True, False, app.leaders,
                        app.attempt, app.difficulty, 
                        app.bonusFish, app.bonusScore)
                return 
            #remove the fish from the list of caught fish and add it to the list
            # of caught fish
            currCaught = app.fish.pop(fish)
            app.caught.append(currCaught) 
            app.dropSpeed = -10
            for fish in app.caught:
                app.dropSpeed += 0.1*fish.weight
            return
        app.fish[fish].moveFish(app)

def updateScore(app):
    scoreCounter = 0
    for fish in app.caught:
        scoreCounter += fish.getScore()
    app.score = scoreCounter + app.startScore

def isNewHighScore(app):
    if app.gameTimer == 0:
        if app.leaders == None and app.score >= 100:
            app.getName = True
            app.name = ''
        elif app.leaders == None:
            app.getName = False
        elif app.score >= app.leaders[-1][0]:
            app.getName = True
            app.name = ''
        for fish in app.caught:
            if type(fish) in app.bonusFish[0]:
                app.bonusFish[0].remove(type(fish))
        if len(app.bonusFish[0]) == 0:
            app.score += app.bonusScore
            app.bonusScore = 0
        app.gameOver = True

def checkGameOver(app):
    if len(app.caught) == 5:
        for fish in app.caught:
            if type(fish) in app.bonusFish[0]:
                app.bonusFish[0].remove(type(fish))
        if len(app.bonusFish[0]) == 0:
            app.score += app.bonusScore
            app.bonusScore = 0
        appStarted(app, app.score, app.gameTimer, True, False, app.leaders, 
                app.attempt, app.difficulty, app.bonusFish, app.bonusScore)
        return
    if app.startTime < 0 and app.spawnDepth < 0:
        for fish in app.caught:
            if type(fish) in app.bonusFish[0]:
                app.bonusFish[0].remove(type(fish))
        if len(app.bonusFish[0]) == 0:
            app.score += app.bonusScore
            app.bonusScore = 0
        appStarted(app, app.score, app.gameTimer, True, False, app.leaders, 
                app.attempt, app.difficulty, app.bonusFish, app.bonusScore)
        return 

#score board class

class ScoreBoard():
    def __init__(self,app):
        self.restartButton = Button(0,app.height*9.25/10,
                                    app.width, app.height, 
                                    'grey14', 'Click Here To Restart', 
                                    'white', appStarted)

    def getScoreLeaders(self, app, currLeader):
        if app.getName:
            return
        if currLeader == None:
            # Kimo is the greatest fisher in all of Hawaii
            # go to @yellowtangbangahs on ig for more info 
            currLeader=[
                    [10000, 'Kimo Higgins', None], [7500, 'Kimo Higgins', None], 
                    [5000, 'Kimo Higgins', None],  [1000, 'Kimo Higgins', None],
                    [100, 'Kimo Higgins', None]]
        for score in range(len(currLeader)):
            if app.score >= currLeader[score][0]:
                if [app.score, app.name, app.attempt] in currLeader:
                    continue
                currLeader.insert(score, [app.score, app.name, app.attempt])
                currLeader.pop()
                break
        return currLeader

    def getButtonPresses(self, app, event):
        if self.restartButton.isPressed(event.x, event.y):
            self.restartButton.finalCall(app, 0, 2645, False, False, 
                                    app.leaders, app.attempt+1)
        
    def drawScoreBoard(self, app, canvas, currLeader):
        goodBlue = rgbString(29, 38, 120)
        darkSand = rgbString(33, 33, 21)
        if currLeader == None:
            return
        canvas.create_rectangle(0,0, app.width, app.height, fill = goodBlue)
        drawSineWave(0, app.height*9/10, app.width, 
                    app.height, app.height/50, 0, darkSand, canvas)
        canvas.create_image(200, 300, 
                            image = ImageTk.PhotoImage(app.bombDrawing[0]))
        canvas.create_image(50, 600, 
                            image = ImageTk.PhotoImage(app.bombDrawing[0]))
        canvas.create_image(450, 200, 
                            image = ImageTk.PhotoImage(app.bombDrawing[0]))
        canvas.create_image(500, 700, 
                            image = ImageTk.PhotoImage(app.bombDrawing[0]))
        canvas.create_image(300, 30, 
                            image = ImageTk.PhotoImage(app.bombDrawing[0]))
        for fish in app.scoreBoardFish:
            fish.drawFish(canvas)
        canvas.create_text(app.width/2, app.height/4, 
                        text = 'High Scores:', font="FreeMono 18 bold", 
                        fill='white')
        scoreMargins = 75
        marginCounter = 1
        for player in currLeader:
            marginCounter += 1
            canvas.create_text(app.width/2, 
                    app.height/4+marginCounter*scoreMargins,
                    text = f'{player[1]}: {player[0]}', 
                    font = 'FreeMono', fill = 'white')
        self.restartButton.drawButton(canvas)

#start screen class

class StartScreen():
    def __init__(self, app):
        self.startButton = Button(app.width/8, app.height/8, 
                                app.width*7/8, app.height/4,'PeachPuff4',
                                'Start', 'black', appStarted)
        self.difficultyButton = Button(app.width/8, app.height/4+5,
                                app.width*3/8-5, app.height/2.5,'DarkSeaGreen4',
                                f'Difficulty:\n\n Medium', 'black', appStarted)
        self.leadersButton = Button(app.width*3/8+5, app.height/4+5, 
                                app.width*5/8-5, app.height/2.5, 'MistyRose3',
                                'High Scores', 'black', appStarted)
        self.infoButton = Button(app.width*5/8+5, app.height/4+5,
                                app.width*7/8, app.height/2.5, 'khaki2',
                                'Game Information', 'black', appStarted)
        self.infoBackButton = Button(app.width/2+50,app.height*3/4,
                                app.width-50,app.height-50, 'salmon1',
                                'Press Here To Go Back', 'black', appStarted)
        self.isInfoPage = False
        self.difficultyStrings = ['Difficulty:\n\n   Easy',
                                  'Difficulty:\n\n Medium',
                                  'Difficulty:\n\n   Hard']
    
    def drawStartScreen(self, app, canvas):
        if self.isInfoPage:
            drawInfoPage(app, canvas)
            self.infoBackButton.drawButton(canvas)
            return
        canvas.create_rectangle(0,0,app.width,app.height, fill = "CadetBlue2")
        drawSineWave(0, app.height*3/4, app.width, app.height, 7, 
                    app.waterShift, 'DeepSkyBlue2', canvas)
        canvas.create_image(app.width/2, 
                    4*math.sin(app.waterShift)+app.height*4.5/7,
                    image = ImageTk.PhotoImage(app.boatImage))
        canvas.create_line(153,605,153,app.height)
        self.startButton.drawButton(canvas)
        self.difficultyButton.drawButton(canvas)
        self.leadersButton.drawButton(canvas)
        self.infoButton.drawButton(canvas)
        canvas.create_text(app.width/2, app.height/20,
                            text = '112 Fishing Simulator', 
                            font="FreeMono 30 bold")
        canvas.create_polygon(app.width*4/9-90, app.height*3/5-40, 
                            app.width*4/9, app.height*3/5,
                            app.width*4/9-40, app.height*3/5-90,
                            fill = 'white', outline = 'black')
        canvas.create_oval(app.width/16, app.height*4/9, 
                        app.width*4/9, app.height*3/5, fill = 'white')
        specialFishStr = ''
        for fish in app.bonusFish[0]:
            specialFishStr += fish(0,0,1,app).name +'\n'
        canvas.create_text((app.width/16+app.width*4/9)/2, 
                        (app.height*4/9+app.height*3/5)/2, 
                        text = f'Special Order:\n{specialFishStr}')
        

    def checkButtonPresses(self, app, event):
        if not self.isInfoPage:
            if self.startButton.isPressed(event.x, event.y):
                self.startButton.finalCall(app, 0, 2645, True, False, app.leaders, 
                                    app.attempt+1, app.difficulty, 
                                    app.bonusFish, app.bonusScore)
            elif self.difficultyButton.isPressed(event.x, event.y):
                app.difficulty += 1
                if app.difficulty == 3:
                    app.difficulty = 0
                self.difficultyButton.text= (
                self.difficultyStrings[app.difficulty])
            elif self.leadersButton.isPressed(event.x, event.y):
                self.leadersButton.finalCall(app, app.score, 0, True, True, 
                                    app.leaders, app.attempt+1)
            elif self.infoButton.isPressed(event.x, event.y):
                self.isInfoPage = True
        else:
            if self.infoBackButton.isPressed(event.x, event.y):
                self.isInfoPage = False

#hook class

class Hook():
    def __init__(self, app, hookPos, delaySpeed):
        self.hookPos = hookPos
        self.targetPos = copy.copy(hookPos)
        self.delaySpeed = delaySpeed
        self.boatHeight = app.height/8

    def drawHookLine(self, app, canvas, caught=None):
        if app.startTime > 0 or app.spawnDepth < 240:
            canvas.create_rectangle(0,0,app.width,app.height, fill = "CadetBlue2")
            drawSineWave(0, self.boatHeight+85.7, app.width, app.height, 7, 
                    app.waterShift, 'DeepSkyBlue2', canvas)
            canvas.create_image(app.width/2, 
                    4*math.sin(app.waterShift)+self.boatHeight,
                    image = ImageTk.PhotoImage(app.boatImage))
            canvas.create_line(153,self.boatHeight+80,153,app.height/2)
            canvas.create_arc(153-5, self.hookPos[1], 
                            153+5, self.hookPos[1]+10,
                            style = 'arc', extent = -270,
                            outline = self.color)
            for fish in caught:
                fish.depth = self.hookPos[1]
                fish.xPos = self.hookPos[0]
                fish.drawFishOnHook(app, canvas)
            return 
        canvas.create_line(self.hookPos[0], 0, self.hookPos[0], 
                            self.hookPos[1])
        canvas.create_arc(self.hookPos[0]-5, self.hookPos[1], 
                            self.hookPos[0]+5, self.hookPos[1]+10,
                            style = 'arc', extent = -270,
                            outline = self.color)
        for fish in caught:
            fish.depth = self.hookPos[1]
            fish.xPos = self.hookPos[0]
            fish.drawFishOnHook(app, canvas)

    def moveHookLine(self, app):
        if app.startTime > 0 or app.spawnDepth < 340: 
            self.targetPos[0] = 153
            if app.spawnDepth < 340 and app.dropSpeed < 0:
                self.delaySpeed = 25
        if self.hookPos[0] > self.targetPos[0]:
            self.hookPos[0] -= self.delaySpeed
            if self.hookPos[0] < self.targetPos[0]:
                self.hookPos[0] = self.targetPos[0]
        if self.hookPos[0] < self.targetPos[0]:
            self.hookPos[0] += self.delaySpeed
            if self.hookPos[0] > self.targetPos[0]:
                self.hookPos[0] = self.targetPos[0]

    def checkCollision(self, other):
        xCol = (self.hookPos[0] >= other.xPos and 
                self.hookPos[0] <= other.xPos+other.size[0])
        yCol = (self.hookPos[1] >= other.depth and 
                self.hookPos[1] <= other.depth+other.size[1])
        if xCol and yCol:
            return True
        else:
            return False

class EasyHook(Hook):
    def __init__(self, app, hookPos, delaySpeed):
        super().__init__(app, hookPos, delaySpeed)
        self.color = 'dark green'
        
class MediumHook(Hook):
    def __init__(self, app, hookPos, delaySpeed):
        super().__init__(app, hookPos, delaySpeed)
        self.color = 'black'

class HardHook(Hook):
    def __init__(self, app, hookPos, delaySpeed):
        super().__init__(app, hookPos, delaySpeed)
        self.color = 'maroon'

#tkinter funtions

def appStarted(app, score=0, gameTime=2645, gameStart=False, gameOver=False,
            leaders=None, attempt=0, difficulty=1, bonusFish=None,
            bonusScore=0):
    app.timerDelay = 17
    app.startScore = score
    app.score = score
    app.gameTimer = gameTime
    app.gameOver = gameOver
    app.gameStarted = gameStart
    app.startTime = 120
    app.leaders = leaders
    app.attempt = attempt
    app.difficulty = difficulty
    getHookAssets(app)
    getAllImages(app)
    getStartScreenAssets(app)
    getFishAssets(app, bonusFish, bonusScore)
    getScoreBoardAssets(app)

def timerFired(app):
    app.waterShift += math.pi/25
    if app.waterShift == 2*math.pi:
        app.waterShift = 0
    if app.getName:
        return
    if not app.gameStarted:
        return
    if app.gameOver:
        gameIsOver(app)
        return
    app.startTime -= 1
    app.hook.boatHeight -= app.dropSpeed
    updateScore(app)
    app.spawnDepth += app.dropSpeed
    app.fishTime += 1
    if app.fishTime == 40:
        app.fishTime = 0
        createFish(app)
    app.gameTimer -= 1
    isNewHighScore(app)
    if not app.isExplosion:
        app.hook.moveHookLine(app)
    checkGameOver(app)
    moveAllFish(app)

def mouseMoved(app, event):
    if not app.gameStarted:
        return
    if app.gameOver:
        return
    app.hook.targetPos[0] = event.x

def mouseDragged(app, event):
    if not app.gameStarted:
        return
    if app.gameOver:
        return
    app.hook.targetPos[0] = event.x

def mousePressed(app, event):
    if not app.gameStarted:
        app.startScreen.checkButtonPresses(app, event)        
    if app.gameOver:
        app.leaderBoard.getButtonPresses(app, event)

def keyPressed(app, event):
    if app.getName:
        getTheName(app,event)
        return
    if app.gameStarted:
        if event.key == 'r':
            appStarted(app, 0, 2645, False, False, app.leaders, 
                    app.attempt+1)
    else:
        if event.key == 'r':
            app.startScreen.isInfoPage = False
    if app.gameOver:
        if event.key == 'r':
            appStarted(app, 0, 2645, False, False, app.leaders, 
                    app.attempt+1)

def redrawAll(app, canvas):
    if app.getName:
        drawNameGetter(app, canvas)
        return
    if not app.gameStarted:
        app.startScreen.drawStartScreen(app, canvas)
        return
    if app.gameOver:
        app.leaderBoard.drawScoreBoard(app, canvas, app.leaders)
        return 
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'DeepSkyBlue2')
    app.hook.drawHookLine(app, canvas, app.caught)
    if app.isExplosion:
        drawExplosion(app, canvas, app.explodedBomb)
    for fish in app.fish:
        if fish.spawnedDepth - app.height*2 < app.spawnDepth:
            fish.drawFish(canvas)
    drawScoreAndTimer(app, canvas)

if __name__ == '__main__':
    main()
