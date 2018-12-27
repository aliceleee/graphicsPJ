import cocos
from cocos.director import director
import datetime
import random
import librosa
import pygame

class FrontEnd(cocos.cocosnode.CocosNode):
    def __init__(self,width = 720,height = 720,fullScreen = False,musicFile = './resources/The Brandenburg Consort-Orchestral Suite No. 3 in D Major, BWV. 1068 - II. Air on the G String.mp3'):
        director.init(width = width ,height =  height,fullscreen = fullScreen)
        super(FrontEnd,self).__init__()
        self.director = director
        self.layer = cocos.layer.Layer()
        self.layer.anchor = (0,0)
        self.layer.position = (0,0)
        self.scene = cocos.scene.Scene(self.layer)

        self.circles = []
        self.datas = []
        self.nowPos = 0
        self.totalTime = 2.0
        self.passedTime = 0.0

        pygame.mixer.init()
        self.track = pygame.mixer.music.load(musicFile)
        y, sr = librosa.load(musicFile)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        self.totalTime = 1.0 + max(0,180 - tempo) / 60.0
        print(tempo)
        print(self.totalTime)
        self.datas = librosa.frames_to_time(beat_frames, sr=sr)

    def startSchedule(self):
        print('start')
        self.passedTime = 0
        #self.oldTime = datetime.datetime.now()
        self.schedule(self.updateCallback,self)
        pygame.mixer.music.play()
        self.resume_scheduler()

    def stopSchedule(self):
        self.unschedule(self.updateCallback)

    def showScene(self):
        self.director.run(self.scene)

    def updateCallback(dt, *args,**kwargs):
        self = args[1]
        delta = args[0]
        self.passedTime += delta
        removeList = []
        for item in self.circles:
            f = item.update(delta,self.totalTime)
            if f:
                removeList.append(item)
        for item in removeList:
            self.layer.remove(item)
            self.circles.remove(item)

        if self.passedTime >= self.datas[self.nowPos]:
            print('beat ' + str(self.nowPos))
            newCircle = Circle()
            self.layer.add(newCircle)
            self.circles.append(newCircle)
            self.nowPos += 1
        

class Circle(cocos.sprite.Sprite):
    def __init__(self):
        super(Circle,self).__init__('resources/Circle.png')
        self.anchor = (0.5,0.5)
        self.position = 360,360
        self.startscale = 0.1
        self.scale = self.startscale
        self.max = 1.7
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.colorClamp = 10

    def update(self,dt,totalTime):
        delta = dt / totalTime * (self.max - self.startscale)
        self.scale += delta
        if self.scale >= self.max:
            return True
        self.color = (
            max(0,min(255,self.color[0] + random.randint(-self.colorClamp,self.colorClamp))),
            max(0,min(255,self.color[1] + random.randint(-self.colorClamp,self.colorClamp))),
            max(0,min(255,self.color[2] + random.randint(-self.colorClamp,self.colorClamp))),
        )
        return False

if __name__ == '__main__':
    FE = FrontEnd()
    FE.startSchedule()
    FE.showScene()