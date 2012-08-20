'''
Created on Oct 26, 2011

@author: hansskov-petersen
'''
from GPS_Config import *
from linearRegression import linreg

def goSlopeSpeedStat(shapeFile, gpsTrack, paramDict, header=False):
    print "Working on", shapeFile, len(gpsTrack.pointLists[0]), "points in a total of", len(gpsTrack.pointLists), "routes"
    allSlopeList = []
    allSpeedList = []
    for subTrack in range(len(gpsTrack.pointLists)):
        if subTrack > 0:
            if header:
                slopeSpeedOutFileHdl = open(slopeSpeedOutFileName, "w")
                slopeSpeedLists = gpsTrack.getSpeedSlope(shapeFile, subTrack, slopeSpeedOutFileHdl, paramDict, True)
                slopeSpeedOutRegFileHdl  = open(slopeSpeedOutRegFileName, "w")
                slopeSpeedOutRegFileHdl.write("shapeFile"  + delim + "numPoints" + delim + "AvgSpeed" + delim + "beta_slope" + delim + "alpha_intersection" + delim + "rSqr" + "\n")
                slopeSpeedOutAllRegFileHdl  = open(slopeSpeedOutAllRegFileName, "w")
                slopeSpeedOutAllRegFileHdl.write("shapeFile"  + delim + "numPoints" + delim + "AvgSpeed" + delim + "beta_slope" + delim + "alpha_intersection" + delim + "rSqr" + "\n")
            else:
                slopeSpeedOutFileHdl = open(slopeSpeedOutFileName, "a")
                slopeSpeedOutRegFileHdl  = open(slopeSpeedOutRegFileName, "a")
                slopeSpeedLists = gpsTrack.getSpeedSlope(shapeFile, subTrack, slopeSpeedOutFileHdl, paramDict, False)
            header = False
            ##print "----->", len(slopeSpeedLists), slopeSpeedLists[1], slopeSpeedLists[0]
            if len(slopeSpeedLists[0]) >= minNumbPointsSpeedSlope:
                ##print type(slopeSpeedLists), len(slopeSpeedLists), "\n", slopeSpeedLists[0], "\n", slopeSpeedLists[1]
                regParams = linreg(slopeSpeedLists[0], slopeSpeedLists[1])
                sumSpeed = 0
                for speed in slopeSpeedLists[1]:
                    sumSpeed += speed
                avgSpeed = sumSpeed / len(slopeSpeedLists[1])
                slopeSpeedOutRegFileHdl.write(shapeFile + delim + str(subTrack) + delim + str(len(slopeSpeedLists[1])) + delim + str(avgSpeed) + delim + str(regParams[0]) + delim + str(regParams[1]) + delim + str(regParams[2]) + "\n")
            allSlopeList += slopeSpeedLists[0]
            allSpeedList += slopeSpeedLists[1]
    ##print "Done. Slope/Speed parameters written to", slopeSpeedOutFileName, "and regression aggregates to", slopeSpeedOutRegFileName
    ##slopeSpeedLists = gpsTrack.getSpeedSlope(shapeFile, subTrack, slopeSpeedOutAllRegFileHdl, paramDict, False)
    allRegParams = linreg(allSlopeList, allSpeedList)
    slopeSpeedOutAllRegFileHdl  = open(slopeSpeedOutAllRegFileName, "a")
    sumSpeed = 0
    for speed in allSpeedList:
        sumSpeed += speed
    avgSpeed = sumSpeed / len(allSpeedList)
    ##allRegParams = linreg(slopeSpeedLists[0], slopeSpeedLists[1])
    slopeSpeedOutAllRegFileHdl.write(shapeFile + delim + str(len(allSlopeList)) + delim + str(avgSpeed) + delim + str(allRegParams[0]) + delim + str(allRegParams[1]) + delim + str(allRegParams[2]) + "\n")
    print "writing to ", slopeSpeedOutAllRegFileName,shapeFile + delim + str(len(allSlopeList)) + delim + str(avgSpeed) + delim + str(allRegParams[0]) + delim + str(allRegParams[1]) + delim + str(allRegParams[2])  
    slopeSpeedOutFileHdl.close()
    slopeSpeedOutRegFileHdl.close()
    slopeSpeedOutAllRegFileHdl.close()
    pass