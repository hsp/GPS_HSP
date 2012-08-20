'''
Created on Oct 10, 2011

@author: hansskov-petersen
'''

from osgeo import ogr
from datetime import datetime
import sys
import shapely.wkt
from GPS_Config import pointTimeDateAttributeName, delim, pointIdAttributeName
from geometry import point, getPoint, samplePoints, getAngle, dist
from utils import getFileNameFromPath

def list2dt(dtText):
    ## 03.08.2009 08:00:00 = august 3 2009
    date = dtText.split(" ")[0].split(".")
    time = dtText.split(" ")[1].split(":")
    return datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]), int(time[2]))
    
def openShape(inFile, index=0):
    shapeFile = ogr.Open(inFile)
    if shapeFile is None:
        print "Failed to open " + inFile + ".\n"
        sys.exit( 1 )
    else:
        return shapeFile #.GetLayer(index) 
    
class GPSPoint():
    '''
    class for points as read from a shapefile
    '''
    def __init__(self, dateTime, obj):
        self.dateTime = dateTime
        self.obj = obj

class route(object):
    def __init__(self, pointList):
        self.pointList = pointList
        self.length = 0
        selfuclidLength = 0
        self.duration = 0   
        
class track(object):
    '''
    Class for a list of tracks within a single track (which might include stops)
    returns a list of instances of GPSPoint : dateTime and features
    Sorted by dataTime
    '''
    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.pointLists = [[]]
        try:
            shapePoints = ogr.Open(fileName) 
            self.shapeLayerPoints = shapePoints.GetLayer(0)
            self.path = fileName
            self.fileName = getFileNameFromPath(fileName)
            self.count = 0
            for index in range(self.shapeLayerPoints.GetFeatureCount()):
                fea = self.shapeLayerPoints.GetFeature(index)
                self.count += 1
                dtText = fea.GetField(pointTimeDateAttributeName)
                dt = list2dt(dtText)
                p = GPSPoint(dt, fea)
                self.pointLists[0].append(p)
            self.pointLists[0] = sorted(self.pointLists[0], key=lambda GPSPoint: GPSPoint.dateTime)
        except:
            print "ERROR: Could not open shape file", fileName
            
    def route2subs(self, stopAttributName, goValue, stopValue, minNumbPoints):
        '''
        devides the points of index 0 in pointList into sub-routes
        according a given selection criteria (e.g. that the attribute 'pause' = 't'
        subroutes are stored in indexes following 0
        '''
        prevPoint = self.pointLists[0][0]
        self.pointLists = [self.pointLists[0]]
        subRoute = []
        for i in range(len(self.pointLists[0])):
            presentPoint = self.pointLists[0][i]
            if prevPoint.obj.GetField(stopAttributName) == stopValue and presentPoint.obj.GetField(stopAttributName) == goValue:
                subRoute = [prevPoint] ## New subRoute is instanciated from the last stop point
            else:
                if presentPoint.obj.GetField(stopAttributName) == goValue:
                    subRoute.append(presentPoint) ## Points are added to the subRoute
                else: 
                    if prevPoint.obj.GetField(stopAttributName) == goValue and presentPoint.obj.GetField(stopAttributName) == stopValue:
                        subRoute.append(presentPoint) ## sbRoute is terminated
                        if len(subRoute) >= minNumbPoints:
                            self.pointLists.append(subRoute)
                    ##subRoute = []
            prevPoint = presentPoint
            
    def getSamples(self, subIndex, angleWidth, length, numPoints, targetFileHdl, rasterDataDict={}, header=False):
        ##print length
        pointList    = self.pointLists[subIndex]    
        lastPoint    = pointList[-1].obj
        ##import pdb;pdb.set_trace()

        p3 = lastPoint.GetGeometryRef().GetPoint(0)
        paramListStr = ""
        orgLength = length
        for key in rasterDataDict.keys():
            paramListStr = paramListStr + delim + key
        if header:
            targetFileHdl.write("FileName" + delim + "SubTrack" + delim + "Id" + delim + "Choice" + delim + "Distance" + delim + "X" + delim + "Y" + delim + "AngPrev" + delim + "AngLast" + paramListStr + "\n")
        for i in range(len(pointList)):
            length = orgLength
            if i == 0:
                presentPoint = pointList[0].obj
            if i == 1:
                previousPoint = presentPoint
                presentPoint = pointList[1].obj
            if i > 1:
                for ii in  range(len(pointList)):
                    if ii >= i:
                        pp1 = presentPoint.GetGeometryRef().GetPoint(0)
                        pp1 = point(pp1[0], pp1[1])
                        pp2 = pointList[ii].obj.GetGeometryRef().GetPoint(0)
                        pp2 = point(pp2[0], pp2[1])
                        akkuLength = dist(pp1, pp2) 
                        ##import pdb;pdb.set_trace()
                        ##print "Length", length, "akkuLength", akkuLength
                        if akkuLength >= length:
                            samplePoint = pointList[ii].obj
                            ##pp2 = nextPoint.GetGeometryRef().GetPoint(0)
                            break
                        else:
                            ##nextPoint = pointList[ii - 1].obj
                            pass
                length = akkuLength    
                nextPoint = pointList[i].obj                
                id =  presentPoint.GetField(pointIdAttributeName)
                p0 = previousPoint.GetGeometryRef().GetPoint(0)
                p1 =  presentPoint.GetGeometryRef().GetPoint(0)
                p2 =     samplePoint.GetGeometryRef().GetPoint(0)
                samples = samplePoints(point(p1[0], p1[1]), point(p2[0], p2[1]), angleWidth, length, numPoints, point(p0[0], p0[1]), point(p3[0], p3[1]))
                for p in samples:
                    ## Here raster values are collected.
                    paramValueStr = ""
                    for key in rasterDataDict.keys():
                        paramValueStr = paramValueStr + delim + str(rasterDataDict[key].getCellValueAtGeolocation(p.x, p.y))
                    targetFileHdl.write(self.fileName + delim + str(subIndex) + delim + str(id) + delim + str(p.selected) + delim + str("%.2f" % p.length) + delim + str(p.x) + delim + str(p.y) + delim + str("%.4f" % p.angleToLast) + delim + str("%.4f" % p.angleFromPrevious) + paramValueStr + "\n")
                previousPoint = presentPoint
                presentPoint = nextPoint


