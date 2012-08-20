'''
Created on Oct 10, 2011

@author: hansskov-petersen
'''
from osgeo import gdal
import struct
from GPS_Config import noDataValue

def convertGeoLocationToPixelLocation(xGeo, yGeo, GetGeoTransformParams):
    ##xGeo, yGeo = geoLocation
    g0, g1, g2, g3, g4, g5 = GetGeoTransformParams
    if g2 == 0:
        xPixel = (xGeo - g0) / float(g1)
        yPixel = (yGeo - g3 - xPixel*g4) / float(g5)
    else:
        xPixel = (yGeo*g2 - xGeo*g5 + g0*g5 - g2*g3) / float(g2*g4 - g1*g5)
        yPixel = (xGeo - g0 - xPixel*g1) / float(g2)
    return int(round(xPixel)), int(round(yPixel))

#def convertGeoDimensionsToPixelDimensions(geoWidth, geoHeight, GetGeoTransformParams):
#    g0, g1, g2, g3, g4, g5 = GetGeoTransformParams
#    return int(round(abs(float(geoWidth) / g1))), int(round(abs(float(geoHeight) / g5)))

class raster(object):
    '''
    class of a raster grid
    '''
    def __init__(self, fileName):
        '''
        Constructor
        '''
        try:
            self.obj = gdal.Open(fileName)
            ##self.band = self.obj.GetRasterBand(1)
            self.fileName = fileName
            self.band = self.obj.GetRasterBand(1)
            self.array = self.band.ReadAsArray()
        except:
            print "ERROR: Could not open or handle raster file", fileName
 
    def getCellValueAtGeolocation(self, geoLocationX, geoLocationY):
        cellLocation = convertGeoLocationToPixelLocation(geoLocationX, geoLocationY, self.obj.GetGeoTransform())
#        rows = self.array.shape[0] 
#        cols = self.array.shape[1]
        try:
            return self.array[cellLocation[1], cellLocation[0]]
        except:
            return noDataValue
