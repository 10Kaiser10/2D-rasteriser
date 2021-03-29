'''mapping every point to draw'''
import numpy as np
import cv2
import math
import time

'''defintion of resolution of canvas'''
res_X = 1000
res_Y = 1000

'''creating the canvas as a numpy array full of zeros'''
canvas = np.zeros((res_X, res_Y))

'''an empty list that is used later to store every object to be drawn'''
objectslist = []



'''funtion that takes a point, origin and angle as input and rotates the point wrt to the origin by given angle, then returns rotated point'''
def rotate(p, angle, origin):
    dx = p.x - origin.x
    dy = p.y - origin.y

    xd = dx * math.cos(angle) - dy * math.sin(angle) + origin.x
    yd = dx * math.sin(angle) + dy * math.cos(angle) + origin.y

    return point(xd,yd)



'''point class, just a way to store the x and y coordinates of a point'''
class point:
    def __init__(self, i, j):
        self.x = i  
        self.y = j



'''rectangle class, stores info about rectangles, has draw funtion to display the rectangle'''
class rectangle:
    def __init__(self, centx, centy, l, b, rot=0, w=0, vx=0, vy=0):
        self.center = point(centx, centy)
        self.length = l
        self.breadth = b
        self.rotation = rot
        self.angVel = w
        self.speedX = vx
        self.speedY = vy
        objectslist.append(self)


    '''draw takes the time elapsed between frames to find new position, then draws the object on canvas'''
    def draw(self,dt):
        self.rotation = self.rotation + dt * self.angVel
        self.center.x = self.center.x + self.speedX * dt
        self.center.y = self.center.y + self.speedY * dt

        for i in range(int(self.center.x - (self.length // 2)), int(self.center.x + (self.length // 2))):
            for j in range(int(self.center.y - (self.breadth // 2)), int(self.center.y + (self.breadth // 2))):
                p = rotate(point(i,j), self.rotation, self.center)
                canvas.itemset((int(p.x), int(p.y)), 0.99)




'''
play funtion, takes a list of objects and displays them, runs a loop to display each frame
deltatime is used to diplay the time for each frame, which is sent to draw funtion to calculate new position
'''
def play(oblist):
    deltatime = 0                         
    ctime = time.time()

    while (1):
        canvas.fill(0)

        print(deltatime)
        deltatime = time.time() - ctime
        ctime = time.time()
        
        for o in oblist:
            o.draw(deltatime)

        cv2.imshow('image', canvas) 
        cv2.waitKey(1)    




r1 = rectangle(250, 250, 100, 200,vx = 50 ,vy=20,w=3.14/2)
r2 = rectangle(100, 100, 20, 50, w=-3.14 / 8)
play(objectslist)







    


