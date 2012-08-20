##from xml.dom import minidom

basePath = "/Users/hansskov-petersen/git/GPSAnalysis/GPS_HSP/"

## Raster information
rasterPath = basePath + "HSP_Data"
demFile  = rasterPath + "/dem.txt"
slopeFile = rasterPath + "/slope.txt"
visibilityFile = rasterPath + "/viewshed5000m.txt"
landcoverFile = rasterPath + "/landCover.txt"

## GPS point information
trackPath = basePath + "shp_20111006"
shapeTrack = trackPath + "/trip_000157_20090803.shp"
##shapeTrack = trackPath + "/trip_000199_20090803.shp"
##shapeTrack = trackPath + "/HSP1.shp"

pointTimeDateAttributeName = "zeittxt"
pointIdAttributeName = "datenid"
minNumbPointsInSubRoute = 50

## Boinding box
minX = 800000
maxX = 850000
minY = 158000
maxY = 181000

## CE: Analytical parameters
angle = 180
distance = 0
numbSamplePoints = 4
ceStartFileName = "RP_MAFREINA"
ceAddToFileName = "ver1"
ceOutFilePath = basePath + "results/JBJ"
ceOutFileName =  ceOutFilePath + "/" + ceStartFileName + "_Dist" + str(int(distance)) + "mAng" + str(int(angle)) + "dg_" + ceAddToFileName + ".txt"

## CE: Trip Stat
tsStartFileName = "TripStat_MAFREINA"
tsAddToFileName = "all2"
tsOutFilePath = basePath + "results/JBJ"
tsOutFileName =  tsOutFilePath + "/" + tsStartFileName + "_" + tsAddToFileName + ".txt"

## Slope Speed assessment
slopeSpeedResolution = 100
minSlope = -50
maxSlope =  50
minFlat  = -5
maxFlat  = 5
minSpeed = 2
maxSpeed = 30
slowFastThreshold = 6
allSlowSlopeList = [] 
allSlowSpeedList = []
allFastSlopeList = [] 
allFastSpeedList = []

slopeSpeedStartFileName = "SlopeSpeed_MAFREINA"
slopeSpeedAddToFileName = "all2"
slopeSpeedOutFilePath = basePath + "results/JBJ"
slopeSpeedOutFileName =  slopeSpeedOutFilePath + "/" + slopeSpeedStartFileName + "_" + str(slopeSpeedResolution) + "m_" + slopeSpeedAddToFileName + ".txt"

# Regression analysis, trips by trip
minNumbPointsSpeedSlope = 50
slopeSpeedStartRegFileName = "SlopeSpeed_Regression_MAFREINA"
slopeSpeedAddToRegFileName = "all2"
slopeSpeedOutRegFilePath = basePath + "results/JBJ"
slopeSpeedOutRegFileName =  slopeSpeedOutFilePath + "/" + slopeSpeedStartRegFileName + "_" + str(slopeSpeedResolution) + "m_" + slopeSpeedAddToFileName + ".txt"
slopeSpeedList = []

# Regression analysis, for all trips per respondent.
slopeSpeedStartAllRegFileName = "SlopeSpeed_All_Regression_MAFREINA"
slopeSpeedAddToAllRegFileName = ""
slopeSpeedOutAllRegFilePath = basePath + "results/JBJ"
slopeSpeedOutAllRegFileName =  slopeSpeedOutAllRegFilePath + "/" + slopeSpeedStartAllRegFileName + "_" + str(slopeSpeedResolution) + "m_" + slopeSpeedAddToAllRegFileName + ".txt"


## General
delim = ","
noDataValue = -8888
writeNoData = False
countNoData = 0

