import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random  import randint
from math import sqrt,cos,sin,acos,pi,floor

    
def main():

    def erreur():
        glColor(.1,.1,.05)
        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface:
                glVertex(add(verticies[vertex]+(0,0,0),1000))
        glEnd()

    TX,TY,TZ=6,15,6
    #TX,TY,TZ=5,5,5
    
    PRECISION=2
    plateau=[[[-1]*TZ for i in range(TY)]for j in range(TX)]


    verticies = (
        (-.5, -.5, -.5),
        (.5, -.5, -.5),
        (.5, .5, -.5),
        (-.5, .5, -.5),
        (-.5, -.5, .5),
        (.5, -.5, .5),
        (.5, .5, .5),
        (-.5, .5, .5)
        )

    edges = (
        (0,1),
        (0,3),
        (0,4),
        (1,2),
        (1,5),
        (2,3),
        (2,6),
        (3,7),
        (4,5),
        (4,7),
        (5,6),
        (6,7)
            )

    surfaces = [ (0, 1, 2, 3), 
                (4,5,6,7),  
                (0,4,7,3), 
                (1,5,6,2),  
                (0,1,5,4), 
                (3,2,6,7) ] 
        
    colors = (
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (1,1,0),
        (0,1,1),
        (1,1,1),
        (1,0,1))

    def point_rotation(u,v,rotation):
        if u==v==0:return 0,0
        d=sqrt(u**2+v**2)
        if v!=abs(v):d*=-1
        angle=acos(u/d)
        return cos(angle+rotation)*d,sin(angle+rotation)*d

    class brique:
        L_formes=[(4,((0,0,0),(1,0,0),(2,0,0),(3,0,0))),
                  (2,((0,0,0),(0,1,0),(1,0,0),(1,1,0))),
                  (3,((0,0,0),(1,0,0),(1,1,0),(2,0,0))),
                  (3,((0,0,0),(1,0,0),(2,0,0),(2,1,0))),
                  (3,((0,0,0),(1,0,0),(1,1,0),(2,1,0))),
                  (2,((0,0,0),(1,0,0),(1,1,0),(1,0,1))),
                  (2,((0,0,0),(1,0,0),(1,1,0),(0,0,1)))]
                  
        
        def __init__(self):
            self.brique= randint(0,6)
            self.taille=brique.L_formes[self.brique][0]
            self.forme=[[[0]*self.taille for i in range(self.taille)]for j in range(self.taille)]

            for x,y,z in brique.L_formes[self.brique][1]:
                self.forme[x][y][z]=1
                
            self.x=randint(0,TX-self.taille)
            self.y=1
            self.z=randint(0,TZ-self.taille)
            self.vie=True

            if not self.update():
                print("fin")
                self.vie=False

            #print(self.__str__())

        def rotation(self,axe,angle=pi/2):
            tmp=self.forme
            self.forme=[[[0]*self.taille for i in range(self.taille)]for j in range(self.taille)] 
            for x,Lx in enumerate(tmp):
                for y,Ly in enumerate(Lx):
                    for z,el in enumerate(Ly):
                        if el:
                            T=self.taille/2-.5
                            nx,ny,nz=x-T,y-T,z-T
                            if axe==0:nx,ny=point_rotation(nx,ny,angle)
                            elif axe==1:nz,ny=point_rotation(nz,ny,angle)
                            else: nx,nz=point_rotation(nx,nz,angle)

                            self.forme[round(nx+T)][round(ny+T)][round(nz+T)]=1
            #print(self.__str__())
            
                            
        def __str__(self):
            for xL in self.forme:
                for yL in xL:
                    print(''.join(map(str,yL)))
                print()
            return ''
        
        def update(self):#aucune collision
            for x,xL in enumerate(self.forme):
                for y,yL in enumerate(xL):
                    for z,el in enumerate(yL):
                        if el:
                            if not (0<=x+self.x <TX and 0<=y+self.y <TY and 0<=z+self.z <TZ):
                                #print('taille')
                                #print(x+self.x,y+self.y,z+self.z)
                                return False
                            if  plateau[x+self.x][y+self.y][z+self.z]!=-1:
                                #print(self.brique)
                                return False

            return True
        def afficher(self):
            for x,xL in enumerate(a.forme):
                    for y,yL in enumerate(xL):
                        for z,el in enumerate(yL):
                            if el:
                                Cube((x+a.x-TX/2,y-TY/2+a.y,z-TZ/2+a.z),self.brique)

        
    def drawText(position, text):                                                

                                                           
        font = pygame.font.Font(None, 64)                                          
        textSurface = font.render(text, True, (255,255,255,255),                   
                                  (0,0,0,255))                                     
        textData = pygame.image.tostring(textSurface, "RGBA", True)                
        glRasterPos3d(*position)                                                
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),         
                        GL_RGBA, GL_UNSIGNED_BYTE, textData)
        
    def add(arg,mul=1):
        res=list(arg[:3])
        for i in range(3):
            res[i]+=arg[3+i]
            res[i]*=mul
        return res

    def Cube(pos,couleur):
        glBegin(GL_QUADS)
        glColor(colors[couleur])
        for surface in surfaces:
            for vertex in surface:
                glVertex(add(verticies[vertex]+pos))
        glEnd()

        glColor(.5,.6,.5)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex(add(verticies[vertex]+pos))
        glEnd()
        


    pygame.init()
    if not pygame.joystick.get_count():
        print('No joystick')
        return
    stick=pygame.joystick.Joystick(0)
    stick.init()
    display = (1920,1080)

    screen =pygame.display.set_mode(display, DOUBLEBUF|HWSURFACE|OPENGL|FULLSCREEN)
    pygame.mouse.set_visible(False)

    gluPerspective(70, (display[0]/display[1]), 0.5, 1000.0)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0.0,0,-max(TX,TY)*3/2.5)
    glRotatef(180,1,0,0)

    affich_cadriage=True
    Y_rotation=0
    X_rotation=0
    acceleration=False
    score=0
    notevent=False
    text_position=(-20,-10,0)

    a=brique()


    while True:

        
        for i in range(10):
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN and event.button < 3:
                    notevent=1-notevent
                    continue

                if event.type == pygame.QUIT:
                     pygame.quit()
                     return
                if event.type == JOYBUTTONDOWN :
                    if event.button <3:
                        pygame.quit()
                        return
                    elif event.button==3:
                        affich_cadriage=1-affich_cadriage
                    elif event.button==7:
                        acceleration=1-acceleration
                    elif 3<event.button<7:
                        a.rotation(event.button-4)
                        if not a.update():
                            erreur()
                            a.rotation(event.button-4,-pi/2)
                    else:
                        #if event.button==11:pygame.image.save(screen, str(a.brique)+".jpeg")
                        pygame.quit()
                        return                   


            Text_X,Text_Y,Text_Z=text_position

            
            x,y=stick.get_axis(1),stick.get_axis(0)

            if abs(x)<.2:x=0
            if abs(y)<.2:y=0

            Y_rotation+=y*PRECISION
            glRotatef(y*PRECISION,0,1, 0)
            Text_X,Text_Z=point_rotation(Text_X,Text_Z,y*PRECISION*pi/180)
            X_rotation+=x*PRECISION

                
            if X_rotation<-30:
                X_rotation=-30
                x=0
            if X_rotation>90:
                X_rotation=90
                x=0
                
            glRotatef(x*PRECISION, cos(Y_rotation*pi/180), 0,sin(Y_rotation*pi/180))
            Text_Y,Text_Z=point_rotation(Text_Y,Text_Z,-x*PRECISION*cos(Y_rotation*pi/180)*pi/180)
            Text_X,Text_Y=point_rotation(Text_X,Text_Y,-x*PRECISION*sin(Y_rotation*pi/180)*pi/180)

            text_position=(Text_X,Text_Y,Text_Z)
            

            

            glColor(1,1,1)
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex(verticies[vertex][0]*TX-.5,
                            verticies[vertex][1]*TY-.5,verticies[vertex][2]*TZ-.5)
                            
            glEnd()

            
            if affich_cadriage:
                glColor(.3,.3,.3)
                glBegin(GL_LINES)
                for x in range(TX+1):
                    for y in range(TY+1):
                        glVertex(x-TX/2-.5,y-TY/2-.5, TZ/2-.5)
                        glVertex(x-TX/2-.5,y-TY/2-.5,-TZ/2-.5)

                for x in range(TX+1):
                    for z in range(TZ+1):
                        glVertex(x-TX/2-.5, TY/2-.5,z-TZ/2-.5)
                        glVertex(x-TX/2-.5,-TY/2-.5,z-TZ/2-.5)

                for y in range(TY+1):
                    for z in range(TZ+1):
                        glVertex( TX/2-.5,y-TY/2-.5,z-TZ/2-.5)
                        glVertex(-TX/2-.5,y-TY/2-.5,z-TZ/2-.5)
                        
                        
                glEnd()
            
            drawText(text_position, "score : {}".format(score) )
                
            for x,xL in enumerate(plateau):
                for y,yL in enumerate(xL):
                    for z,el in enumerate(yL):
                        if el!=-1:
                            Cube((x-TX/2,y-TY/2,z-TZ/2),el)


            x,z=point_rotation(stick.get_axis(2),-stick.get_axis(3),Y_rotation/180*pi)

            if i%2==0:
                if x<-.3: x=-1
                elif x>.3: x= 1
                else:x=0
                
                if z<- .3:z=-1
                elif z>.3: z= 1
                else:z=0

                a.x+=x
                if not a.update():
                    erreur()
                    a.x-=x
                
                a.z+=z
                if not a.update():
                    erreur()
                    a.z-=z

                

            a.afficher()
            pygame.display.flip()
            pygame.time.wait(40)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            if notevent or not(i==4 or acceleration ) :continue

            
            a.y+=1
            if not a.update():
                acceleration=False
                for x,xL in enumerate(a.forme):
                    for y,yL in enumerate(xL):
                        for z,el in enumerate(yL):
                            if el:
                                plateau[x+a.x][y+a.y-1][z+a.z]=a.brique

            
                a.__init__()
                if not a.vie:
                    a.afficher()
                    pygame.display.flip()
                    pygame.quit()
                    return

                L_destruction=[]
                for y in range(TY):
                    for x in range(TX):
                        for z in range(TZ):
                            if plateau[x][y][z]==-1:
                                break
                        else:
                            L_destruction+=[(x,y,z) for z in range(TZ)]

                    for z in range(TZ):
                        for x in range(TX):
                            if plateau[x][y][z]==-1:
                                break
                        else:
                            L_destruction+=[(x,y,z) for x in range(TX)]
                            
                if len(L_destruction):
                    score+=(len(L_destruction)//TX)**2*TX
                    print(score)
                    avant=(-1,-1,-1)
                    L_destruction.sort()
                    for x,y,z in L_destruction:
                        if (x,y,z)==avant:continue
                        avant=(x,y,z)
                        for y in range(y,0,-1):
                            plateau[x][y][z]=plateau[x][y-1][z]
                        plateau[x][0][z]=-1
main()
