import numpy as np
import cv2

def get_rec(h=30, w=120): #vertices of the rectangles
    rec_vertices = np.array([
        [0, h, 1],
        [0, 0, 1],
        [w, 0, 1],
        [w, h, 1]])
    return rec_vertices

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

    #p and q on the canvas

    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = get_line(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return

def draw_polygon(vertices, canvas, color=(255,255,255)):

    vertices = vertices.astype('int')
    for k in range(vertices.shape[0] - 1):
        draw_line(vertices[k], vertices[k+1], canvas, color)
    draw_line(vertices[-1], vertices[0], canvas, color)
    return

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

    #generates translation matrix

    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty
    return Tmat

def erase(canvas):

    #erases everything on canvas

    canvas[:, :, :] = (0,0,0)
    return canvas

def main():
    height, width = 600, 1000
    window = np.zeros((height, width, 3), dtype = 'uint8')

    rec_height, rec_width = 120, 30
    rec = get_rec(rec_height, rec_width).T

    T0 = makeTmat(width/2, height-rec_height-1)
    T1 = makeTmat(-rec_width/2, -rec_height)
    T2 = makeTmat(rec_width/2, rec_height)
    T3 = makeTmat(0, -rec_height)

    degree1 = 0
    degree2 = 0
    degree3 = 0

    v1 = 1
    v2 = 2
    v3 = 3

    while True:
        erase(window)

        R1 = makeRmat(degree1)
        R2 = makeRmat(degree2)
        R3 = makeRmat(degree3)

        #five blocks = one arm
        H1 = T0
        rec1 = (H1 @ rec).T
        draw_polygon(rec1, window, color=(255, 229, 236))

        H2 = T3 @ T2 @ R1 @ T1
        rec2 = (H1 @ H2 @ rec).T
        draw_polygon(rec2, window, color=(255, 194, 209))

        H3 = T3 @ T2 @ R2 @ T1
        rec3 = (H1 @ H2 @ H3 @ rec).T
        draw_polygon(rec3, window, color=(255, 179, 198))

        H4 = T3 @ T2 @ R3 @ T1
        rec4 = (H1 @ H2 @ H3 @ H4 @ rec).T
        draw_polygon(rec4, window, color=(255, 143, 171))

        H5 = T3 @ T2 @ R3 @ T1
        rec5 = (H1 @ H2 @ H3 @ H4 @ H5 @ rec).T
        draw_polygon(rec5, window, color=(251, 111, 146))

        if degree1 >= 10 or degree1 < -10:
            v1 = -v1
        if degree2 >= 20 or degree2 <= -30:
            v2 = -v2
        if degree3 >= 4 or degree3 <= -45:
            v3 = -v3
        degree1 += v1
        degree2 += v2
        degree3 += v3

        cv2.imshow("robotarm", window)
        if cv2.waitKey(20) == 27: break

if __name__ == "__main__": # __ 
       main()