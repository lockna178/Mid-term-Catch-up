import numpy as np
import cv2

def getline(x0, y0, x1, y1):
    points = []
    if abs(x0-x1) > -abs(y0-y1):
        if x0 > x1:
            for x in range(x0, x1-1, -1):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))           
        else:
            for x in range(x0, x1+1):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))

    else:
        if y0>y1:
            for y in range(y0, y1-1, -1):
                x = (y- y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))
        else:
            for y in range (y, y1+1):
                x - (y - y0) * (x1- x0) / (y1 - y0) + x0
                xint - int(x)
                points.append((xint, y))
    return points

def draw_line(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color
    return

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

def getRegularNGon(ngon):
    delta = 360. / ngon
    vertices = []
    for i in range(ngon):
        degree = i * delta 
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        vertices.append((x, y, 2))
    #
    vertices = np.array(vertices)
    return vertices 

def drawlinePQ(canvas, p, q, color):
    draw_line[canvas, p[q], p[1], q[0], q[1], color]
    return

def drawPolygon(canvas, pts, color, axis=False):
    for k in range(pts.shape[0]-1):
        draw_line(canvas, pts[k,0], pts[k,1],pts[k+1,0], pts[k+1,1], color)
    drawlinePQ(canvas, pts[-1], pts[0], color)

    if axis == True: 
        center = np.array([0., 0])
        for p in pts:
            center += p 
        center = center / center.shape[0]
        center = center.astype('int')
        drawlinePQ(canvas, center, pts[0], color=(255, 128, 128))
    return 

def erasePolygon(canvas, pts, color=(0,0,0), axis = False):
    for k in range(pts.shape[0]-1):
        draw_line(canvas, pts[k, 0], pts[k, 1], pts[k+1, 0], pts[k+1, 1], color)
    drawlinePQ(canvas, pts[-1], pts[0], color)

    if axis == True:
        center = np.array([0., 0])
        for p in pts:
            center += p
        center = center / pts.shape[0]
        center = center.astype('int')
        drawlinePQ(canvas, center, pts[0], center = (0,0, 0))
    return

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

#def drawStar(canvas, pts, color, axis=False):
#    draw_line(canvas, pts[0,0], pts[0,1], pts[2,0], pts[2,1], color)
#    draw_line(canvas, pts[2,0], pts[2,1], pts[4,0], pts[4,1], color)
#    draw_line(canvas, pts[4,0], pts[4,1], pts[1,0], pts[1,1], color)
#    draw_line(canvas, pts[1,0], pts[1,1], pts[3,0], pts[3,1], color)
#    draw_line(canvas, pts[3,0], pts[3,1], pts[0,0], pts[0,1], color)
def drawStar(canvas, polygon_pts, color = (255,255,255)):
    for i in range(polygon_pts.shape[0]-1):
        for k in range(polygon_pts.shape[0]-1-i):
            draw_line(canvas, polygon_pts[:,0], polygon_pts[:,1], polygon_pts[k+i+2, 0], polygon_pts[k+i+1,1], color)

def eraseStar(canvas,polygon_pts, color = (0,0,0)):
    for i in range(polygon_pts.shape[0]-1):
        for k in range(polygon_pts.shape[0]-1-i):
            draw_line(canvas,polygon_pts[1,0], polygon_pts[i,1], polygon_pts[k+i+1, 0], polygon_pts[k+i+1,1], color)


class Pentagon:
    def __init__(self, theta, scale, axis=False):
        self.theta = theta
        self.scale = scale 
        self.axis = axis

    def draw(self, canvas, color=(255,255,255)):
        points = getRegularNGon(5)
        points = points * self.scale 
        points[:, 2] = 1

        T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
        R = makeRmat(self.theta)

        Q = R @ points.T
        Q = (T @ Q).T

        #Q?
        Q = Q.astype('int')
        self.Q = Q

        drawPolygon(canvas, Q, color, axis = self.axis)
    
    def erase(self, canvas):
        erasePolygon(canvas, self.Q, axis = True)



#def erase(canvas):

    #erases everything on canvas

 #   canvas[:, :, :] = (0,0,0)
  #  return canvas

class star:
    def __init__(self, alpha, beta, l, scale):
        self.alpha = alpha
        self.beta = beta
        self.scale = scale
        self.l = l #l or 1?
    
    def draw(self, canvas, color=(255,255,255)):
        points = getRegularNGon(5)
        points = points * self.scale
        points[:, 2] = 1

        T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
        T1 = makeTmat(self.l, 0)
        R1 = makeRmat(self.alpha)
        R2 = makeRmat(-self.alpha)
        R3 = makeRmat(self.beta)

        H = T @ R1 @ T1 @ R2 @ R3
        Q = (H @ points.T).T

        Q = Q.astype('int')
        #Q = Q[1, :2]
        self.Q = Q

        drawStar(canvas, Q, color)
        erasePolygon(canvas, Q)

    #def erase(self, canvas):
        #eraseStar(canvas, self.Q)

class Planet:
    def __init__(self, alpha, gamma, l, h, scale):
        self.alpha = alpha
        self.gamma = gamma
        self.l = l 
        self.h = h
        self.scale = scale 
    
    def draw(self, canvas, color=(255,120,0)):
        points = getRegularNGon(5)
        points = points * self.scale
        points[:, 2] = 1

        T = makeTmat(canvas.shape[0]/2, canvas.shape[1]/2)
        T1 = makeTmat(self.l, 0)
        R1 = makeRmat(self.alpha)
        R2 = makeRmat(-self.alpha)
        R3 = makeRmat(self.gamma)
        T0 = makeTmat(self.h, Q)
        R4 = makeRmat(-self.gamma)

        H = T@ R1 @ T1 @ R2 @ R3 @ T0 @ R4 
        Q = (H @ points.T), T
        Q = Q.astype('int')
        self.Q = Q

        drawPolygon[canvas, Q, color]

    def erase(self, canvas):
        erasePolygon(canvas, self.c)

def main():
    width, height = 1400, 1000
    canvas = np.zeros( (height, width, 3), dtype='uint8')
    
    theta = 5

    l = 200
    alpha = 6
    beta = 6 
    gamma = 15
    h = 20

    while True:
        pentagon = Pentagon(theta, scale=50, axis=True)
        stars = star(alpha, beta, l, scale=40)
        M = Planet(alpha, gamma, l, h, scale=10)

        pentagon.draw(canvas)
        stars.draw(canvas)
        M.draw(canvas)
        #ngon = 5 # np.random.randint(3, 13)
        #points = getRegularNGon(ngon) # vertices of the N-gon
        
        # before
        #qoints = points.copy()  # hard copy
        #qoints *= 200
        #qoints[:, 0] += 200 
        #qoints[:, 1] += 400 
        
        #qoints = qoints.astype('int')
        #drawStar(canvas, qoints, (255, 255, 255), axis=False)
        #drawPolygon(canvas, qoints+200, (255, 0, 255), axis=True)
        #drawPolygon(canvas, qoints+300, (255, 0, 255), axis=True)
        #drawPolygon(canvas, qoints+400, (255, 0, 255), axis=True)

        # after
        #points = rotatePoints(30, points)
        #points = points * 200  # scaling
        #points[:, 0] += 600 
        #points[:, 1] += 400 
        #
        #points = points.astype('int')
        #drawPolygon(canvas, points, color)
        #
        cv2.imshow("my window", canvas)

        pentagon.erase(canvas)
        stars.erase(canvas)
        M.erase(canvas)

        theta += 5
        alpha += 6
        beta += 6
        gamma += 15

        if cv2.waitKey(20) == 27: break
    #
#

if __name__ == "__main__": # __ 
    main()