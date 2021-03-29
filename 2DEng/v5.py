'''circle added'''
import numpy as np
import cv2
import math
import time
from math import sqrt

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

    return point(xd, yd)


def distance(p1, p2):
    dist = sqrt((p1.x - p2.x)** 2 + (p1.y - p2.y)** 2)
    return dist


'''point class, just a way to store the x and y coordinates of a point'''


class point:
    def __init__(self, i, j):
        self.x = i
        self.y = j


class linesegment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def onLine(self, p):
        fack = (int(self.p2.y) - int(self.p1.y)) * (int(p.x) - int(self.p1.x)) - (int(p.y) - int(self.p1.y)) * (int(self.p2.x) - int(self.p1.x))
        if fack == 0:
            return 0
        elif fack > 0:
            return 1
        elif fack < 0:
            return - 1

    def intersection(self, x):
        if (int(self.p1.x) - int(self.p2.x)) == 0:
            return - 1
            
        elif ((int(self.p2.x) <= x <= int(self.p1.x)) or (int(self.p2.x) >= x >= int(self.p1.x))):

            return (int(self.p2.y) - ((int(self.p2.y) - int(self.p1.y)) * (int(self.p2.x - x))) / (int(self.p2.x) - int(self.p1.x)))

        else:
            return -1


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

    def getcorners(self):
        self.corners = [rotate(point(self.center.x + (self.length) / 2, self.center.y + (self.breadth) / 2), self.rotation, self.center), rotate(point(self.center.x - (self.length) / 2, self.center.y - (self.breadth) / 2), self.rotation, self.center),
                        rotate(point(self.center.x + (self.length) / 2, self.center.y - (self.breadth) / 2), self.rotation, self.center), rotate(point(self.center.x - (self.length) / 2, self.center.y + (self.breadth) / 2), self.rotation, self.center)]
        return self.corners

    def getedges(self):
        corners = self.getcorners()
        self.edges = [linesegment(self.corners[0], self.corners[2]), linesegment(self.corners[0], self.corners[3]), linesegment(self.corners[1], self.corners[2]), linesegment(self.corners[1], self.corners[3])]
        return self.edges

    def insideorOn(self, p):
        add = 0
        mult = 1
        edges = self.getedges()
        for l in edges:
            temp = l.onLine(p)
            add = add + temp
            mult = mult * temp

        if (add * mult == 0):
            return 1
        else:
            return 0

    '''draw takes the time elapsed between frames to find new position, then draws the object on canvas'''

    def draw(self, dt):
        self.rotation = self.rotation + dt * self.angVel
        self.center.x = self.center.x + self.speedX * dt
        self.center.y = self.center.y + self.speedY * dt

        cor = self.getcorners()
        edges = self.getedges()

        xmax = int(max(cor, key=lambda point: point.x).x)
        xmin = int(min(cor, key=lambda point: point.x).x)


        for i in range(xmin, xmax):

            intrYs = []

            for l in edges:
                intersections = l.intersection(i)
                if (intersections == -1):
                    continue
                else:
                    intrYs.append(int(intersections))

            length = len(intrYs)

            if (length == 2):
                a,b = intrYs

            if (length > 2):
                a = intrYs[0]
                for p in intrYs:
                    if a == p:
                        continue
                    else:
                        b = p

            if (b > a):
                st = a
                sp = b
            else:
                st = b
                sp = a

            for j in range(st, sp):
                canvas.itemset((i, j), 1)


class circle:
    def __init__(self, centx, centy, r, vx=0, vy=0):
        self.center = point(centx, centy)
        self.radius = r
        self.speedX = vx
        self.speedY = vy

        objectslist.append(self)

    def draw(self, dt):
        self.center.x = self.center.x + self.speedX * dt
        self.center.y = self.center.y + self.speedY * dt

        radint = int(self.radius)
        centXint = int(self.center.x)
        centYint = int(self.center.y)

        for h in range(0, radint):
            w = int(sqrt(radint * radint - h * h))
            
            for j in range(-w, w):
                canvas.itemset((centXint + h, centYint + j), 1)
                canvas.itemset((centXint - h, centYint + j), 1)
                

'''
play funtion, takes a list of objects and displays them, runs a loop to display each frame
deltatime is used to diplay the time for each frame, which is sent to draw funtion to calculate new position
'''

'''def CollisionPhysics(olist):
    for i in range(0, len(olist)):
        for j in range(i + 1, len(olist)):
            a, b = olist[i], olist[j]
            
            dist = distance(a, b)

            if dist > (a.radius + b.radius):
                return
            else:'''
                


def play(objlist):
    deltatime = 0
    ctime = time.time()

    while (1):
        canvas.fill(0)

        print(deltatime)
        deltatime = time.time() - ctime
        ctime = time.time()

        for o in objlist:
            o.draw(deltatime)

        cv2.imshow('image', canvas)
        cv2.waitKey(1)


r1 = rectangle(250, 250, 100, 200, rot=30, w=3, vx=5, vy=5)
r2 = rectangle(100, 100, 20, 50, w=-1)
c1 = circle(150,650,100,vx = 10,vy = -30)
play(objectslist)


