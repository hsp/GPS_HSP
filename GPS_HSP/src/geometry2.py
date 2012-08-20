import math

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def getPoint(obj):
    return point(obj.GetGeometryRef().GetPoint(0)[0], obj.GetGeometryRef().GetPoint(0)[1])
    
def polar(p, angle, length):
    return point(p.x + (length * math.cos(angle)), p.y + (length * math.sin(angle)))

def dist(p1, p2):
    deltaX = abs(p1.x - p2.x) ** 2
    deltaY = abs(p1.y - p2.y) ** 2 
    return (deltaX + deltaY) ** 0.5
    
def samplePoints(p1, p2, angleWidth, length, numPoints):
    '''
    returns a list of numPoints points in a distance of length from p1 within a total angle of angleWidth
    angleWidth is given in degrees 
    if length is 0, the distance between p1 and p2 will be applied
    numPoints is the total number of points across (excluding the point that will coninside with p2)
    '''
    lP = []
    angle = getAngle(p1, p2)
    grain = int(numPoints/2)
    deltaAngle = math.radians(angleWidth) / 2
    if length == 0:
        length = dist(p1, p2)
    startAngle = angle - deltaAngle
    for i in range(int(numPoints/2)):
        lP.append(polar(p1, startAngle, length))
        startAngle = startAngle + (deltaAngle / grain)
    endAngle = angle  + (deltaAngle / grain)
    for i in range(int(numPoints/2)):
        lP.append(polar(p1, endAngle, length))
        endAngle = endAngle + (deltaAngle / grain)
    return lP
   
def getAngle(p1, p2):
    deltaX = p2.x - p1.x
    deltaY = p2.y - p1.y
    return math.atan2(deltaY, deltaX)

    

