'''
Created on Oct 10, 2011

@author: hansskov-petersen
'''

from osgeo import ogr
from datetime import datetime
import sys
import shapely.wkt
##from GPS_Config import pointTimeDateAttributeName, delim, pointIdAttributeName, noDataValue, writeNoDataToo, countNodata
from GPS_Config import *
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
        self.orgCount = 0
        self.newCount = 0
        self.obj = obj

class route(object):
    def __init__(self, pointList):
        self.pointList = pointList
        self.length = 0
        self.uclidLength = 0
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
            oc = 0
            for index in range(self.shapeLayerPoints.GetFeatureCount()):
                fea = self.shapeLayerPoints.GetFeature(index)
                dtText = fea.GetField(pointTimeDateAttributeName)
                dt = list2dt(dtText)
                p = GPSPoint(dt, fea)
                pCoords = p.obj.GetGeometryRef().GetPoint(0)
                x = pCoords[0]
                y = pCoords[1]
                p.orgCount = oc
                if x > minX and y > minY and x < maxX and y < maxY: 
                    self.pointLists[0].append(p)
                oc += 1
            self.pointLists[0] = sorted(self.pointLists[0], key=lambda GPSPoint: GPSPoint.dateTime)
            nc = 0
            for i in range(len(self.pointLists[0])):
                self.pointLists[0][i].newCount = nc
                nc += 1
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
                        subRoute.append(presentPoint) ## subRoute is terminated
                        if len(subRoute) >= minNumbPoints:
                            self.pointLists.append(subRoute)
                    ##subRoute = []
            prevPoint = presentPoint
            
    def getSamples(self, subIndex, angleWidth, length, numPoints, targetFileHdl, rasterDataDict={}, header=False):
        pointList    = self.pointLists[subIndex]    
        lastPoint    = pointList[-1].obj
        countNoData = 0

        p3 = lastPoint.GetGeometryRef().GetPoint(0)
        paramListStr = ""
        orgLength = length
        for key in rasterDataDict.keys():
            paramListStr = paramListStr + delim + key
        if header:
            targetFileHdl.write("FileName" + delim + "SubTrack" + delim + "Id" + delim + "Panel" + delim + "Choice" + delim + "Distance" + delim 
                                + "X" + delim + "Y" + delim + "AngLast" + delim + "AngPrev" + paramListStr + delim + "\n")
        for i in range(len(pointList)):
            length = orgLength
            if i == 0:
                presentPoint = pointList[0].obj
            if i == 1:
                previousPoint = presentPoint
                presentPoint = pointList[1].obj
            if i > 1:
                pp1 = presentPoint.GetGeometryRef().GetPoint(0)
                pp1 = point(pp1[0], pp1[1])
                for ii in  range(len(pointList)):
                    if ii >= i:
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
                id =  presentPoint.GetField(pointIdAttributeName)
                p0 = previousPoint.GetGeometryRef().GetPoint(0)
                p1 =  presentPoint.GetGeometryRef().GetPoint(0)
                p2 =   samplePoint.GetGeometryRef().GetPoint(0)
                samples = samplePoints(point(p1[0], p1[1]), point(p2[0], p2[1]), angleWidth, length, numPoints, point(p0[0], p0[1]), point(p3[0], p3[1]), id)
                pointValDict = {}
                noDataFlag = False
                for p in samples:
                    valDict = {}
                    for key in rasterDataDict.keys():
                        valDict[key] = rasterDataDict[key].getCellValueAtGeolocation(p.x, p.y)
                        if valDict[key] == noDataValue:
                            noDataFlag = True
                    pointValDict[p] = valDict
                ##import pdb;pdb.set_trace()
                if not noDataFlag and not writeNoData:
                    for p in samples:
                        ## Here raster values are collected.
                        paramValueStr = ""
                        for key in rasterDataDict.keys():
                            paramValueStr = paramValueStr + delim + str(pointValDict[p][key])
                        targetFileHdl.write(self.fileName + delim + str(subIndex) + delim + str(id) + delim + str(len(pointList) * len(samples)) + delim 
                                            + str(p.selected) + delim + str("%.2f" % p.length) + delim + str(p.x) + delim + str(p.y) + delim 
                                            + str("%.4f" % p.angleToLast) + delim + str("%.4f" % p.angleFromPrevious) + paramValueStr + "\n")
                    else:
                    ##print "Nodata found"
                        countNoData += 1
                nextPoint = pointList[i].obj                
                previousPoint = presentPoint
                presentPoint = nextPoint
        return countNoData

    def getSubtrackDuration(self, subTrack):
        totalDuration = 0
        pointList = self.pointLists[subTrack]
        t0 = False
        ## t0.dateTime
        for iP in range(len(pointList)):
            t1 = pointList[iP].dateTime
            if iP == 0:
                tFirst = t1 
            t0 = t1
        return (t1 - tFirst).seconds / 60
    
    def getSubTrackLength(self, subTrack):
        pointList = self.pointLists[subTrack]
        totalLength = 0
        p0 = point(0,0)
        for iP in range(len(pointList)):
            p1 = pointList[iP].obj.GetGeometryRef().GetPoint(0)
            p1 = point(p1[0], p1[1])
            if iP > 0:
                totalLength += dist(p0, p1)
            else:
                pFirst = p1 
            p0 = p1
        return totalLength, dist(pFirst, p1)
     
    def getRasterMinMax(self, subTrack, raster):
        pointList = self.pointLists[subTrack]
        minRaster =   9999999
        maxRaster =  -9999999
        akkuVal = 0
        for iP in range(len(pointList)):
            p1 = pointList[iP].obj.GetGeometryRef().GetPoint(0)
            p1 = point(p1[0], p1[1])
            rasterVal = raster.getCellValueAtGeolocation(p1.x, p1.y)
            akkuVal += rasterVal
            if iP == 0:
                startVal = rasterVal
            if rasterVal < minRaster:
                minRaster = rasterVal
            if rasterVal > maxRaster:
                maxRaster = rasterVal
        endVal = rasterVal
        return (startVal, endVal, minRaster, maxRaster, akkuVal / len(pointList))
    
    def getTrackStat(self, shapeFile, subTrack, tsOutFileHdl, paramDict, header=False):
        trackStatDict = {}
        # get duration
        # get distance
        ##print "Subtrack length", subTrack, self.getSubTrackLength(subTrack), len(self.pointLists[subTrack])
        
        lengthList = self.getSubTrackLength(subTrack)
        trackStatDict[1] = "Length", lengthList[0]
        trackStatDict[2] = "EclidLength", lengthList[1]
        trackStatDict[3] = "NumPoints", len(self.pointLists[subTrack])
        ##print "Subtrack duration", subTrack, self.getSubtrackDuration(subTrack), len(self.pointLists[subTrack])
        trackStatDict[5] = "DurationMin", self.getSubtrackDuration(subTrack)
        trackStatDict[6] = "AvgSpeed", (trackStatDict[1][1] / 1000.0) / (trackStatDict[5][1] / 60.0)
        trackStatDict[4] = "AvgSegment", trackStatDict[1][1] / trackStatDict[3][1] 
        altList = self.getRasterMinMax(subTrack, paramDict["Altitude"])
        trackStatDict[7] = "StartAlt", altList[0]
        trackStatDict[8] = "EndAlt", altList[1]
        trackStatDict[9] = "MinAlt", altList[2]
        trackStatDict[10] = "MaxAlt", altList[3]
        trackStatDict[11] = "AvgAlt", altList[4]
        ##print "Subtrack altitudes", subTrack, altList
        paramHeaderList = "ShapeFile" + delim + "subTrack"  
        keysList = trackStatDict.keys()
        keysList.sort()
        if header:
            for key in keysList:
                paramHeaderList += delim + trackStatDict[key][0]
            tsOutFileHdl.write(paramHeaderList + "\n")
        header = False
        paramValueList = shapeFile + delim + str(subTrack) 
        for key in keysList:
            paramValueList += delim + str(trackStatDict[key][1])
        tsOutFileHdl.write(paramValueList + "\n")
        # get average speed
        # get min/max altitude
        # get start/end altitude
        # one record per subTrack
        return trackStatDict
        
    def getSpeedSlope(self, shapeFile, subTrack, slopeSpeedOutFileHdl, paramDict, speedSlopeOutFileHdl):
        # one record per point
        # get distance
        # get duration
        # get speed
        # get altitudes
        # get slope
        #write speed and slope
        pointList = self.pointLists[subTrack]
        if speedSlopeOutFileHdl:
            slopeSpeedOutFileHdl.write("ShapeFile" + delim + "SubTrack" + delim + "Distance" + delim + "FromID" + delim + 
                                       "ToID" + delim + "Speed" + delim + "Slope" + delim + "\n")
        pp0 = point(0,0)
        slopeList = []
        speedList = []
        for iP in range(len(pointList)):
            p1 = pointList[iP].obj.GetGeometryRef().GetPoint(0)
            pp1 = point(p1[0], p1[1])
            distance = 0.0
            offset = 1
            if iP > 0:
                while distance < slopeSpeedResolution and iP+offset < len(pointList):
                    ##print iP+offset, len(pointList)
                    p2 = pointList[iP+offset].obj.GetGeometryRef().GetPoint(0)
                    pp2 = point(p2[0], p2[1])
                    p3 = pointList[iP+offset-1].obj.GetGeometryRef().GetPoint(0)
                    pp3 = point(p3[0], p3[1])
                    ## Collect slopes on the way (as a list). Enable average slopes by the end.
                    distance += dist(pp3, pp2)
                    startId   = pointList[iP].obj.GetField(pointIdAttributeName)
                    endId     = pointList[iP+offset].obj.GetField(pointIdAttributeName)
                    startTime = pointList[iP].dateTime
                    endTime   =  pointList[iP+offset].dateTime
                    offset += 1
                deltaTimeHours = (endTime - startTime).seconds / 3600.00
                rasterVal1 = paramDict["Altitude"].getCellValueAtGeolocation(pp2.x, pp2.y)
                rasterVal0 = paramDict["Altitude"].getCellValueAtGeolocation(pp0.x, pp0.y)
                deltaAltitude = rasterVal1 - rasterVal0
                if distance != 0:
                    ## Calc slopePCT as the average oof all segments slope
                    slopePct = (deltaAltitude * 100.00) / distance
                else:
                    slopePct = 0
                speed = (distance / 1000) / deltaTimeHours
                if slopePct > minSlope and slopePct < maxSlope and speed > minSpeed and speed < maxSpeed:
                    slopeSpeedOutFileHdl.write(shapeFile + delim + str(subTrack) + delim + str(distance) + delim + str(startId) + delim + 
                                               str(endId) + delim + str(speed) + delim + str(slopePct) + "\n")
                    slopeList.append(slopePct)
                    speedList.append(speed)
            p0 = p1
            pp0 = point(p0[0], p0[1])
        ##print len(slopeList), len(speedList), len([slopeList, speedList])
        return [slopeList, speedList]


