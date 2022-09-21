from drawille import Canvas, line
import math, locale, time, curses

locale.setlocale(locale.LC_ALL,"")
stdscr = curses.initscr()
stdscr.refresh()

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        rad = angle * math.pi / 180
        cosa, sina = math.cos(rad), math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        rad = angle * math.pi / 180
        cosa, sina = math.cos(rad), math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        rad = angle * math.pi / 180
        cosa, sina = math.cos(rad), math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

cuboid1 = [[0,0,0],[15,0,0],[15,15,0],[0,15,0],[0,0,15],[15,0,15],[15,15,15],[0,15,15]]
cuboid2 = [[16,0,0],[31,0,0],[31,15,0],[16,15,0],[16,0,15],[31,0,15],[31,15,15],[16,15,15]]
cuboid3 = [[32,0,0],[47,0,0],[47,15,0],[32,15,0],[32,0,15],[47,0,15],[47,15,15],[32,15,15]]
cuboid4 = [[0,0,16],[15,0,16],[15,15,16],[0,15,16],[0,0,31],[15,0,31],[15,15,31],[0,15,31]]
cuboid5 = [[0,0,32],[15,0,32],[15,15,32],[0,15,32],[0,0,47],[15,0,47],[15,15,47],[0,15,47]]
face1 = [[0,1,2,3],[1,2,6,5],[4,5,6,7],[0,3,7,4],[2,3,7,6],[0,1,5,4]]
vertices = [Point3D(0,0,0),Point3D(15,0,0),Point3D(15,15,0),Point3D(0,15,0),Point3D(0,0,15),Point3D(15,0,15),Point3D(15,15,15),Point3D(0,15,15),]
faces = []

def xdir(temp):
    for i in range(2):
        for e in temp:
            x,y,z = e[0],e[1],e[2]
            if i == 0:
                vertices.append(Point3D(x+16,y,z))
            else:
                vertices.append(Point3D(x+32,y,z))
def ydir(temp):
    for i in range(2):
        for e in temp:
            x,y,z = e[0],e[1],e[2]
            if i == 0:
                vertices.append(Point3D(x,y+16,z))
            else:
                vertices.append(Point3D(x,y+32,z))
def zdir(temp):
    for i in range(2):
        for e in temp:
            x,y,z = e[0],e[1],e[2]
            if i == 0:
                vertices.append(Point3D(x,y,z+16))
            else:
                vertices.append(Point3D(x,y,z+32))

def makefaces():
    for i in range(len(vertices)//8):
        for f in face1:
            faces.append((f[0]+(i*8),f[1]+(i*8),f[2]+(i*8),f[3]+(i*8)))

def makecube():
    xdir(cuboid1)
    ydir(cuboid1);ydir(cuboid2);ydir(cuboid3);ydir(cuboid4);ydir(cuboid5)
    zdir(cuboid1);zdir(cuboid2);zdir(cuboid3)
    makefaces()


def __main__(stdscr, projection=False):
    angleX, angleY, angleZ = 15, -20, 0
    c = Canvas()
    while 1:
        t = []
        for v in vertices:
            p = v.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
            if projection:
                p = p.project(50, 50, 50, 50)
            t.append(p)

        for f in faces:
            for x,y in line(t[f[0]].x, t[f[0]].y, t[f[1]].x, t[f[1]].y):
                c.set(x,y)
            for x,y in line(t[f[1]].x, t[f[1]].y, t[f[2]].x, t[f[2]].y):
                c.set(x,y)
            for x,y in line(t[f[2]].x, t[f[2]].y, t[f[3]].x, t[f[3]].y):
                c.set(x,y)
            for x,y in line(t[f[3]].x, t[f[3]].y, t[f[0]].x, t[f[0]].y):
                c.set(x,y)

        f = c.frame(-30, -20, 50, 50)
        stdscr.addstr(0, 0, '{0}\n'.format(f))
        stdscr.refresh()
        time.sleep(1)
        c.clear()

if __name__ == '__main__':
    makecube()
    from sys import argv
    projection = False
    if '-p' in argv:
        projection = True
    curses.wrapper(__main__, projection)
