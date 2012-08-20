'''
Created on Oct 10, 2011

@author: hansskov-petersen
'''
from getTracks import track
from getRaster import raster
from goCe import goCe
from goTripStat import goTripStat
from goSlopeSpeedStat import goSlopeSpeedStat
from GPS_Config import *
from geometry import getPoint, point, samplePoints, dist
from utils import *

if __name__ == '__main__':
    pass

dem = raster(demFile)
slope = raster(slopeFile)
visibility = raster(visibilityFile)
landcover = raster(landcoverFile)
# paramDict: The key is the header name
#            The dict value is the variable referring to the rasters
paramDict = {}
paramDict["Altitude"]   = dem
paramDict["Slope"]      = slope
paramDict["Visibility"] = visibility
paramDict["LandCover"]  = landcover

shapeFiles = listFilesByExtention(trackPath, "shp")
#for f in shapeFiles:
#    print f
##shapeFiles = [shapeTrack.split("/")[-1]]
countPoints = 0
countRoutes = 0
countNoData = 0

statHeader = True
slopeSpeedHeader = True
for shapeFile in shapeFiles:
    gpsTrack = track(trackPath + "/" + shapeFile)
    gpsTrack.route2subs('pause', 'f', 't', minNumbPointsInSubRoute)
    countPoints += len(gpsTrack.pointLists[0])
    countRoutes += len(gpsTrack.pointLists)
    ##import pdb;pdb.set_trace()
    ##goCe.goCe(shapeFile, gpsTrack, paramDict, countPoints, countRoutes)
    ##goTripStat(shapeFile, gpsTrack, paramDict, statHeader)
    ##statHeader = False
    goSlopeSpeedStat(shapeFile, gpsTrack, paramDict, slopeSpeedHeader)
    slopeSpeedHeader = False
