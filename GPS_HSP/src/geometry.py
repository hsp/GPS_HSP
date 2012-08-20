import math

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angleToLast = 0
        self.angleFromPrevious = 0
        self.selected = 0
        self.length = 0

def getPoint(obj):
    return point(obj.GetGeometryRef().GetPoint(0)[0], obj.GetGeometryRef().GetPoint(0)[1])
    
def polar(p, angle, length):
    return point(p.x + (length * math.cos(angle)), p.y + (length * math.sin(angle)))

def dist(p1, p2):
    deltaX = abs(p1.x - p2.x) ** 2
    deltaY = abs(p1.y - p2.y) ** 2 
    return (deltaX + deltaY) ** 0.5
    
def samplePoints(p1, p2, angleWidth, length, numPoints, p0, lastPoint, id):
    '''
    returns a list of numPoints points in a distance of length from p1 within a total angle of angleWidth
    angleWidth is given in degrees 
    if length is 0, the distance between p1 and p2 will be applied
    numPoints is the total number of points across (excluding the point that will coinside with p2)
    '''
    if length == 0: 
        #Dynamic distance: Distance to next point in track applied
        length = dist(p1, p2)
    p = p2     
    p.angleToLast = abs(getAngle(p1, p2) - getAngle(p1, lastPoint))
    p.angleFromPrevious = abs(getAngle(p0, p1) - getAngle(p1, p2))
    p.selected = 1
    p.length = dist(p1, p2)
#    p.angleToLast =       abs(math.degrees(p.angleToLast)) % 180
#    p.angleFromPrevious = abs(math.degrees(p.angleFromPrevious)) % 180

    lP = [p]
    angle = math.radians(getAngle(p1, p2))
    grain = int(numPoints/2)
    deltaAngle = math.radians(angleWidth) / 2

    ##print "Length: ", length, "Angle:", math.degrees(angle)
    startAngle = angle - deltaAngle
    for i in range(int(numPoints/2)):
        p = polar(p1, startAngle, length)
        p.angleToLast = abs(getAngle(p1, p) - getAngle(p1, lastPoint))
        p.angleFromPrevious = abs(getAngle(p0, p1) - getAngle(p1, p))
        lP.append(p)
        startAngle = startAngle + (deltaAngle / grain)
    endAngle = angle  + (deltaAngle / grain)
    for i in range(int(numPoints/2)):
        p = polar(p1, endAngle, length)
        p.angleToLast = abs(getAngle(p1, p) - getAngle(p1, lastPoint))
        p.angleFromPrevious = abs(getAngle(p0, p1) - getAngle(p1, p))
        lP.append(p)
        endAngle = endAngle + (deltaAngle / grain)
    for p in lP:
        p.angleToLast = p.angleToLast % 360
        if p.angleToLast > 180:
            p.angleToLast = abs(p.angleToLast - 360) 
        p.angleFromPrevious = p.angleFromPrevious % 360
        if p.angleFromPrevious > 180:
            p.angleFromPrevious = abs(p.angleFromPrevious - 360) 
#        if  id == 1735923 and p.selected == 1:
#            print "angPrev", p.angleFromPrevious
#            print "p0", p0.x, p0.y
#            print "p1", p1.x, p1.y
#            print "p2", p2.x, p2.y
#            import pdb;pdb.set_trace()
#    
        if p.selected == 0:
            p.length = length
    return lP

def getAngle(p1, p2):
    deltaX = p2.x - p1.x
    deltaY = p2.y - p1.y
    return math.degrees(math.atan2(deltaY, deltaX))

    

