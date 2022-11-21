#code is unfinished

import numpy as np 
import cv2 

width, height = 1600, 1000
canvas = np.zeros((height, width, 3), dtype = np.uint8)

def getline(x0, y0, x1, y1):
    points = []
    width, height = 1600, 1000
    canvas = np.zeros((height, width, 3), dtype = np.uint8)
    if x0 > x1:
        for x in range(x0, x1+1):
            y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
            yint = int(y)
            points.append((x, yint))           
    else:
        for x in range(x0, x1+1):
        #if x0 == x1:
        #    y = y0
        #else:
            y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
            yint = int(y)
            points.append((x, yint))

    return points


def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    if False:
        # xys = getline(x0, y0, x1, y1)
        # for xy in xys:
        #     x, y = xy
        #     canvas[y, x, :] = color
        pass 
    else:
        # cv2.line(canvas, (x0, y0), (x1, y1), color=tuple([int(c) for c in color]))
        cv2.line(canvas, (x0, y0), (x1, y1), 
                color=(int(color[0]), int(color[1]), int(color[2])))
    return
#

def radom_lines(canvas):
    # draw random line segment
    x0 = np.random.randint(0, canvas.shape[1])
    y0 = np.random.randint(0, canvas.shape[0])
    x1 = np.random.randint(0, canvas.shape[1])
    y1 = np.random.randint(0, canvas.shape[0])
    color = np.random.randint(0, 256, size=3)
    drawLine(canvas, x0, y0, x1, y1, color)
#

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta 
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append( (x, y) )
    #
    points = np.array(points)
    return points 

def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 

def drawPolygon(canvas, pts, color, axis=False):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k,0], pts[k,1], 
                        pts[k+1,0], pts[k+1,1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)

    if axis == True: # center - pts[0]
        center = np.array([0., 0])
        for p in pts:
            center += p 
        center = center / center.shape[0]
        center = center.astype('int')
        drawLinePQ(canvas, center, pts[0], color=(255, 128, 128))
    #
    return 

def rotation(degree):
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)
    Rmat = np.zeros((2,2))
    Rmat[0,0] = c 
    Rmat[0,1] = -s 
    Rmat[1,0] = s 
    Rmat[1,1] = c 
    return Rmat 

def rotatePoints(degree, points):
    R = rotation(30)
    qT = R @ points.T
    points = qT.T 
    return points 

def main():
    width, height = 1400, 1000
    canvas = np.zeros( (height, width, 3), dtype='uint8')

    while True:

        color = (255, 255, 255)
        ngon = 5 # np.random.randint(3, 13)
        points = getRegularNGon(ngon) # vertices of the N-gon
        
        # before
        qoints = points.copy()  # hard copy
        qoints *= 200
        qoints[:, 0] += 200 
        qoints[:, 1] += 400 
        
        #qoints = qoints.astype('int')
        #drawPolygon(canvas, qoints, color, axis=True)

        # after
        points = rotatePoints(30, points)
        points = points * 200  # scaling
        points[:, 0] += 600 
        points[:, 1] += 400 
        #
        points = points.astype('int')
        drawPolygon(canvas, points, color)
        #
        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: break
    #



while True:
    xinit = np.random.randint(1, width, size=2)
    yinit = np.random.randint(1, height, size=2)
    xys = getline(xinit[0], yinit[0], xinit[1], yinit[1])

    for p in xys:
        x, y = p
        #canvas[y, x] = (252, 170, 230)

    cv2.imshow('show', canvas)
    ch = cv2.waitKey(30)
    if ch == 27:
        break

#

    if __name__ == "__main__": # __ 
       main()