from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import PIL.Image as Image

class myGraph():
	def __init__(self):
		self.wallPts()
		self.bindTexture()
		self.light()
	def wallPts(self):
		self.pts = [[-0.5,-0.5,0],[0.5,-0.5,0],[0.5,0.5,0],[-0.5,0.5,0], \
						[-0.5,-0.5,-0.3],[0.5,-0.5,-0.3],[0.5,0.5,-0.3],[-0.5,0.5,-0.3]]
		#self.lines = [[0,1],[0,2],[1,3],[2,3],[0,4],[1,5],[2,6],[3,7],[1,5],[4,5],[4,6],[5,7],[6,7]]
		self.faces = [[0,1,2,3],[2,6,7,3],[0,3,7,4]]#,[4,5,6,7],[0,1,5,4],[1,2,6,5]]
		self.cor = [[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0]]
	def drawWall(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()

		self.readTextures("./resources/wall.jpg")
		glMatrixMode(GL_MODELVIEW)
		glRotatef(30.0,0.0,1.0,0.0)
		glRotatef(30.0,1.0,0.0,0.0)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures)
		glEnable(GL_TEXTURE_GEN_S)
		glEnable(GL_TEXTURE_GEN_T)
		#glEnable(GL_TEXTURE_GEN_R)
		glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
		glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
		#glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
		
		"""glColor3f(1.0,0.0,0.0)
		glBegin(GL_LINES)
		for [i,j] in self.lines:
			glVertex3fv(self.pts[i])
			glVertex3fv(self.pts[j])
		glEnd()"""
		glutSolidSphere(1,50,50)
		glDisable(GL_TEXTURE_2D)

		glPopMatrix()
		glFlush()
	def drawCube(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()

		glMatrixMode(GL_MODELVIEW)
		glRotatef(15.0,0.0,1.0,0.0)
		glRotatef(30.0,1.0,0.0,0.0)

		glBegin(GL_QUADS)
		glNormal3f(0.0,0.0,1.0)
		for pt in self.faces[0]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glNormal3f(0.0,1.0,0.0)
		for pt in self.faces[1]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glNormal3f(-1.0,0.0,0.0)
		for pt in self.faces[2]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glEnd()

		glPopMatrix()
		glFlush()
	def light(self):
		light_position = [-0.8, 0.8, 1.1, 1.0]
		mat_diffuse = [1.0, 1.0, 1.0, 1.0]
		glShadeModel ( GL_SMOOTH )
		#glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
		glLightfv (GL_LIGHT0, GL_DIFFUSE, [1.0,1.0,1.0,1.0])
		glLightfv ( GL_LIGHT0, GL_POSITION, light_position)
		glEnable (GL_LIGHTING)
		glEnable (GL_LIGHT0)
		glEnable (GL_DEPTH_TEST)
		glDisable(GL_COLOR_MATERIAL)
	def bindTexture(self):
		self.readTextures("./resources/wall.jpg")
		glEnable(GL_TEXTURE_2D)
		#glEnable(GL_TEXTURE_GEN_S)
		#glEnable(GL_TEXTURE_GEN_T)
		glBindTexture(GL_TEXTURE_2D, self.textures)
	def readTextures(self, filename):
		img = Image.open(filename)
		img = np.asarray(img, dtype=np.uint8)
		self.textures = glGenTextures(1)
		#glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glBindTexture(GL_TEXTURE_2D, self.textures)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		#glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		#glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[0], img.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
		return self.textures

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(400,400)
	glutCreateWindow("realisticGraph")
	g = myGraph()
	glutDisplayFunc(g.drawCube)
	glutMainLoop()

if __name__ == "__main__":
	main()