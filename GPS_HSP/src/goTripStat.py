'''
Created on Oct 26, 2011

@author: hansskov-petersen
'''
from GPS_Config import *

def goTripStat(shapeFile, gpsTrack, paramDict, header=False):
    print "Working on", shapeFile, len(gpsTrack.pointLists[0]), "points in a total of", len(gpsTrack.pointLists), "routes"
    for subTrack in range(len(gpsTrack.pointLists)):
        if header:
            tsOutFileHdl = open(tsOutFileName, "w")
            gpsTrack.getTrackStat(shapeFile, subTrack, tsOutFileHdl, paramDict, True)
        else:
            tsOutFileHdl = open(tsOutFileName, "a")
        if subTrack >= 0:
            ##countNoData += gpsTrack.getSamples(subTrack, angle, distance, numbSamplePoints, ceOutFileHdl, paramDict, False)
            gpsTrack.getTrackStat(shapeFile, subTrack, tsOutFileHdl, paramDict, False)
        header = False
    print "Done. Statistics written to", tsOutFileName
#    print countPoints, "points, in", countRoutes, "routes, written to", tsOutFileName
#    print countNoData, "out of", countPoints, "choice sets including NoData excluded"
    
    tsOutFileHdl.close()
