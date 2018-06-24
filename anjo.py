from pygame import *
import random, sys

class Flake(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface( (11,11) )
        self.rect = self.image.get_rect()
        draw.line(self.image,Color("white"),(5,0),(5,10))
        draw.line(self.image,Color("white"),(0,2),(10,8))
        draw.line(self.image,Color("white"),(0,8),(10,2))
        self.vy = 1
        flakes.add(self)
    def update(self):
        self.rect.y += self.vy
        self.rect.x = (self.rect.x+self.vx)%width
        if self.rect.y > height-50:
            flakes.remove(self)
        if angel.lives>0 and self.rect.colliderect(angel.rect):
            angel.lives -= 1
            startLevel()

class Angel(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface( (11,17) )
        self.rect = self.image.get_rect()
        poly = ((0,1),(2,4),(8,4),(10,1),(10,8),(7,10),(10,16),(0,16),(3,10),(0,8))
        draw.polygon(self.image,Color("yellow"),poly)
        draw.circle(self.image,Color("yellow"),(5,2),2)
        self.lives = 2
    def update(self):
        tasten = key.get_pressed()
        if tasten[K_UP]:
            self.rect.y -=  3
        if tasten[K_DOWN] and self.rect.bottom<height:
            self.rect.y += 3
        if tasten[K_LEFT] and self.rect.x>0:
            self.rect.x -= 3
        if tasten[K_RIGHT] and self.rect.right<width:
            self.rect.x += 3
        if (tasten[K_l]and self.rect.bottom<height) or self.rect.top<25:
            startLevel(min(level+1,len(vxRanges)))

flakes = sprite.RenderPlain()
init()
width = 800
height = 600
window = display.set_mode((width, height))
display.set_caption("Anjo")
screen = display.get_surface()
fnt = font.Font(None, 24)


def write(s,x,y,center=0):
    text = fnt.render(s,True,Color("white"))
    screen.blit(text,(x-center*text.get_width()/2,y))

def welcone(s,x,y,center=0):
    text = fnt.render(s,True,Color("purple"))
    screen.blit(text,(x-center*text.get_width()/2,y))

vxRanges = ((0,0),(0,0),(-1,1),(1,2),(0,0),(-1,1),(-1,1),(-2,2),(-2,2),(-2,2),(-2,2),(-3,3),(0,0))
vyRanges = ((1,1),(1,2),(1,2),(1,2),(1,3),(1,2),(1,2),(1,2),(1,2),(1,3),(1,3),(1,3),(0,0))
freqs = (0.1,0.1,0.1,0.1,0.2,0.2,0.25,0.25,0.3,0.3,0.4,0.4,0)
clock = time.Clock()
angel = Angel()

def updateFlakes():
    if random.random()<freqs[level-1]:
        f = Flake()
        f.rect.x = random.randint(0,3*width)
        f.rect.bottom = 0
        f.vx = random.randint(*vxRanges[level-1])
        f.vy = random.randint(*vyRanges[level-1])
    flakes.update()

def startLevel(lvl=0):
    global level
    angel.rect.x = width/2
    angel.rect.bottom = height
    if lvl:
        level = lvl
        for i in range(800):
            updateFlakes()

startLevel(1)
while True:
    for ev in event.get():
        if ev.type == constants.QUIT:
            exit(0)
    screen.fill((0,0,0))
    write("Vidas: %d"%angel.lives,width-120,20)
    if level<len(vxRanges):
        write("Nível: %d/%d"%(level,len(vxRanges)-1),width-120,40)
        updateFlakes()
        flakes.draw(screen)
    else:
        write("Parbéns, você venceu!",width/2,height/2-10,1)
    if angel.lives>0:
        angel.update()
        screen.blit(angel.image,angel.rect.topleft)
    else:
        write("Fim de Jogo",width/2,height/2-10,1)
        write("Comece um novo jogo com 'n'.", width/2,height/2+40,1)
    if key.get_pressed()[K_n]:
        angel.lives = 2
        startLevel(1)
    if level==1 and angel.lives==2 and angel.rect.bottom==height:
        welcone("Use as setas para voar. Evite flocos de neve.", width/2,height/2,1)
    display.flip()
    clock.tick(40)
