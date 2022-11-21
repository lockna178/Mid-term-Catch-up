import numpy as np
import cv2

def get_line(x0, y0, x1, y1):

    #returns coordinates of line connecting (x0,y0) and (x1, y1)

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

    #draws line connecting p and q on the canvas

    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = get_line(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return

def drawPolygon(vertices, canvas, color=(255,255,255)):

    #draws a polygon on canvas

    vertices = vertices.astype('int')
    for k in range(vertices.shape[0] - 1):
        draw_line(vertices[k], vertices[k+1], canvas, color)
    draw_line(vertices[-1], vertices[0], canvas, color)
    return

def deg2rad(deg):

    #converts degrees into radians

    rad = deg * np.pi / 180.
    return rad

def makeRmat(degree):

    #generates rotation matrix

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

    #generates translation matrix

    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty
    return Tmat

def main():

    while True:        
        #170 Pillar
        #Hpillar = Translation([x0, y0])
        Hpillar = makeTmat([x0, y0])
        Qpillar = Hpillar @ Pillar
        drawPolygon(canvas, Qpillar.T)

        #wing1
        for shift in [0, 90, 180, 270]:
            #H1 = np.eye(3) @ Hpillar @ Translation([w/2, 0]) @ Rotation(degree + shift) @ Translation([-200, 0])
            H1 = np.eye(3) @ Hpillar @ makeTmat([w/2, 0]) @ makeRmat(degree + shift) @ makeTmat([-200, 0])
            Wing1 = H1 @ Wing
            drawPolygon(canvas, Wing1.T, color-(255,255,0))
            drawTriangleFilled(canvas, Wing1[:,0], Wing1[:,1], Wing1[:2], (255,125,55))

        cv2.imshow('Canvas', canvas)
        ch = cv2.waitKey(38)
        if ch == 27: break

        degree += 15

if __name__ == "__main__": # __ 
       main()