'''
Created on Oct 26, 2011

@author: hansskov-petersen
'''
from getTracks import track
from getRaster import raster
from GPS_Config import *
from geometry import getPoint, point, samplePoints, dist
#from Main import shapeFile, gpsTrack, paramDict, countPoints, countRoutes

def goCe(shapeFile, gpsTrack, paramDict, countPoints, countRoutes):
    countNoData = 0
    ceOutFileHdl = open(ceOutFileName, "w")
    firstLine = True
    print "Working on", shapeFile, len(gpsTrack.pointLists[0]), "points in a total of", len(gpsTrack.pointLists), "routes"
    if firstLine:
        gpsTrack.getSamples(1, angle, distance, numbSamplePoints, ceOutFileHdl, paramDict, True)
        firstLine = False
    for subTrack in range(len(gpsTrack.pointLists)):
        if subTrack > 1:
            countNoData += gpsTrack.getSamples(subTrack, angle, distance, numbSamplePoints, ceOutFileHdl, paramDict, False)
    
    print "Done."
    print countPoints, "points, in", countRoutes, "routes, written to", ceOutFileName
    print countNoData, "out of", countPoints, "choice sets including NoData excluded"
    
    ceOutFileHdl.close()
