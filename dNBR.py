# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:18:58 2021

@author: Samed
"""

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

onc = gdal.Open("time1.tif")
snr = gdal.Open("time2.tif")

gt1 = onc.GetGeoTransform()
gt2 = snr.GetGeoTransform()

time1= onc.ReadAsArray()
time1= np.swapaxes(time1,0,2)
time1= np.swapaxes(time1,0,1)
time2= snr.ReadAsArray()
time2 = np.swapaxes(time2,0,2)
time2 = np.swapaxes(time2,0,1)

NIR=3
SWIR=4

NBRo=(time1[:,:,NIR]-time1[:,:,SWIR])/(time1[:,:,NIR]+time1[:,:,SWIR])
NBRs=(time2[:,:,NIR]-time2[:,:,SWIR])/(time2[:,:,NIR]+time2[:,:,SWIR])
dNBR=NBRo-NBRs
[m,n]=dNBR.shape
snc=np.zeros([m,n])
            
for i in range(m):
    for j in range(n):
        if dNBR[i,j]<-0.25:
            snc[i,j]=0
        elif dNBR[i,j]>-0.25 and dNBR[i,j]<-0.1:
            snc[i,j]=1
        elif dNBR[i,j]>-0.1 and dNBR[i,j]<0.1:
            snc[i,j]=2
        elif dNBR[i,j]>0.1 and dNBR[i,j]<0.27:
            snc[i,j]=3
        elif dNBR[i,j]>0.27 and dNBR[i,j]<0.44:
            snc[i,j]=4
        elif dNBR[i,j]>0.44 and dNBR[i,j]<0.66:
            snc[i,j]=5
        elif dNBR[i,j]>0.66:
            snc[i,j]=6

def cm_to_inch(value):
    return value/2.54

fig, ax = plt.subplots(figsize=(cm_to_inch(40),cm_to_inch(30)))
ax.axis('off')
plt.imshow(snc)
cbar=plt.colorbar()
tick_font_size = 36
cbar.ax.tick_params(labelsize=tick_font_size)
plt.title('dNBR',fontsize=36)

fig, ax = plt.subplots(figsize=(cm_to_inch(40),cm_to_inch(30)))
ax.axis('off')
plt.imshow(NBRo)
cbar=plt.colorbar()
tick_font_size = 24
cbar.ax.tick_params(labelsize=tick_font_size)
plt.title('NBR yangın öncesi',fontsize=36)

fig, ax = plt.subplots(figsize=(cm_to_inch(40),cm_to_inch(30)))
ax.axis('off')
plt.imshow(NBRs)
cbar=plt.colorbar()
tick_font_size = 24
cbar.ax.tick_params(labelsize=tick_font_size)
plt.title('NBR yangın sonrası',fontsize=36)


## Rasteri tif olarak kaydetmek için 

# import gdal, osr
# import numpy as np


# def array2raster(rasterfn,newRasterfn,array):
#     raster = gdal.Open(rasterfn)
#     geotransform = raster.GetGeoTransform()
#     originX = geotransform[0]
#     originY = geotransform[3]
#     pixelWidth = geotransform[1]
#     pixelHeight = geotransform[5]
#     cols = raster.RasterXSize
#     rows = raster.RasterYSize

#     driver = gdal.GetDriverByName('GTiff')
#     outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
#     outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
#     outband = outRaster.GetRasterBand(1)
#     outband.WriteArray(array)
#     outRasterSRS = osr.SpatialReference()
#     outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
#     outRaster.SetProjection(outRasterSRS.ExportToWkt())
#     outband.FlushCache()



# rasterfn = 'time1.tif'
# newRasterfn = 'New.tif'

# array2raster(rasterfn,newRasterfn,snc)
# array2raster(rasterfn,'NBRo.tif',NBRo)
# array2raster(rasterfn,'NBRs.tif',NBRs)
