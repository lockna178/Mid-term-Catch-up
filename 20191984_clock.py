import numpy as np
import cv2
import datetime
import time

def get_block(h=30, w=120):
    block_vertices = np.array([
        [0, h, 1],
        [0, 0, 1],
        [w, 0, 1],
        [w, h, 1]])
    return block_vertices

def get_line(x0, y0, x1, y1):
    points = []

    if abs(x1 - x0) >= abs(y1 - y0):
        if x0 < x1:
            for x in range(x0, x1+1):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))

        else:
            for x in range(x1, x0-1):
                y = (x-x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))
        return points

    else:
        if y0 < y1:
            for y in range(y0, y1+1):
                x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))

        else:
            for y in range(y1, y0-1):
                x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))
        return points

def draw_line(p, q, canvas, color):
    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = get_line(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return

def getRegularNGon(ngon): #for making the circle around clock?
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

def draw_polygon(vertices, canvas, color=()):
    vertices = vertices.astype('int')
    for k in range(vertices.shape[0] - 1):
        draw_line(vertices[k], vertices[k+1], canvas, color)
    draw_line(vertices[-1], vertices[0], canvas, color)
    return

#converts degrees into radians
def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad

def makeRmat(degree):
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)
    Rmat = np.eye(3)
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    return Rmat

def makeTmat(tx, ty):
    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty
    return Tmat

def erase(canvas):
    canvas[:, :, :] = (0,0,0)
    return canvas

def main():
    width, height = 1000, 600
    window = np.zeros((height, width, 3), dtype = 'uint8')
    clock = datetime.datetime.now()
    hour = clock.strftime('%H')
    min = clock.strftime('%M')

    ngon = 5
    points = getRegularNGon(ngon)

    qoints = points.copy()
    qoints *= 200
    qoints[:, 0] += 200 
    qoints[:, 1] += 400 

    qoints = qoints.astype('int')
    #draw_polygon(window, qoints, color=(0, 0, 255)) #couldn't make this work yet

    block_height, block_width = 150, 5
    block = get_block(block_height, block_width).T

    T0 = makeTmat(width/2, height/2)
    T1 = makeTmat(-block_width/2, -block_height)

    angleH = (int(hour)/12)*360
    angleM = (int(min)/60)*360

    v1= 0.25 
    v2= 0.1

    while True:
        erase(window)

        R1 = makeRmat(angleH)
        R2 = makeRmat(angleM)

        H1 = T0 @ R1 @ T1
        block1 = (H1 @ block).T
        draw_polygon(block1, window, color=(155, 93, 229)) 

        H2 = T0 @ R2 @ T1
        block2 = (H2 @ block).T
        draw_polygon(block2, window, color=(254, 228, 64)) 

        if(angleM % 6 == 0): #using time imports
            angleH += v1
        angleM += v2

        cv2.imshow("clock", window)
        if cv2.waitKey(10) == 27: break

if __name__ == "__main__":
       main()