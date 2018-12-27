from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
import numpy as np
import PIL.Image as Image

class interaction():
    def __init__(self):
        self.pts = [[-0.5,-0.5,0],[0.5,-0.5,0],[0.5,0.5,0],[-0.5,0.5,0]]
        self.colors = [[1.0,1.0,1.0],[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]
        self.coloridx = 0

    def drawObject(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        color = self.colors[self.coloridx]
        glColor(color[0],color[1],color[2])
        glBegin(GL_QUADS)
        for pt in self.pts:
            glVertex3fv(pt)
        glEnd()

        glFlush()
    def mouseDown(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.pressed = 1
            self.cx = x
            self.cy = y
            #print("mouse down, start corordinate: ",x,y)
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            if self.pressed:
                self.pressed = 0
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            self.coloridx = (self.coloridx+1) % 4
            glutPostRedisplay()
    def motion(self, x,y):
        if self.pressed:
            #print("motion corordinate: ", x, y)
            deltax = x - self.cx
            deltay = y - self.cy
            self.cx = x
            self.cy = y
            #print("move delta: ", deltax, deltay)
            glTranslatef(deltax/500, -deltay/500, 0.0)
            glutPostRedisplay()
    def keyboard(self, key, x, y):
        print("in keyboard callback")
        if key == GLUT_KEY_UP:
            print("get key, but no scaled")
            glScaled(1.1,1.1,1.0)
        if key == GLUT_KEY_DOWN:
            glScaled(0.9,0.9,1.0)
        glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500,500)
    glutCreateWindow("test")
    interactionWin = interaction()
    glutDisplayFunc(interactionWin.drawObject)
    glutMouseFunc(interactionWin.mouseDown)
    glutMotionFunc(interactionWin.motion)
    glutSpecialFunc(interactionWin.keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()