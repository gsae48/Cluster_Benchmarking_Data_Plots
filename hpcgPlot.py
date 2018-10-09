# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:51:49 2016

@author: Ali
"""
#!/usr/bin/python
import yaml
import numpy;
import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

class Cube(object):
  
    def __init__(self, x, y, z):
        self.nx = x
        self.ny = y
        self.nz = z
        self.index = 0
        self.plot1list = numpy.zeros(shape=(0,2))
        self.plot2list = numpy.zeros(shape=(0,2))
        self.plot3list = numpy.zeros(shape=(0,2))
        self.plot4list = numpy.zeros(shape=(0,2))
        
        

def plotIt(whichPlotlist, subplotnum, xlab, ylab):
    plt.subplot(subplotnum)
    for key, cube in cubeDict.items():
        if (whichPlotlist == 1):
            plotlist = cube.plot1list
        elif (whichPlotlist == 2):
            plotlist = cube.plot2list
        elif (whichPlotlist == 3):
            plotlist = cube.plot3list
        elif (whichPlotlist == 4):
            plotlist = cube.plot4list
        plotlist = plotlist[plotlist[:,0].argsort()]
        xaxis = []
        yaxis = []
        for i in range(plotlist.shape[0]):
            xaxis.append(plotlist[i,0])
            yaxis.append(plotlist[i,1])    
        
        plt.plot(xaxis, yaxis, label=str(key), marker="o")
        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
        yaxis.sort()
        xaxis.sort()
        scaley = yaxis
        scalex = xaxis
        #plt.ylim(scaley[0]-10, scaley[len(scaley)-1]+10)
        plt.xlabel(xlab)
        plt.ylabel(ylab)  
        plt.show()
    

cubeDict = {}

i = 0
for filename in glob.iglob('hpcgRuns/*.yaml'):
    #print (filename)
    
    with open(filename, 'r') as stream:
        out = yaml.load(stream)
        
        nx = out['Local Domain Dimensions']['nx']    
        ny = out['Local Domain Dimensions']['ny']        
        nz = out['Local Domain Dimensions']['nz']        
        strDimensions = str(nx) + 'x' + str(ny) + 'x' + str(nz)
        probSize = nx #assumming nx=ny=nz
        #print ('dimensions: ', strDimensions)
        
        '''For plotting runtime as a function of the number of cores'''
        if  strDimensions not in cubeDict:
            cubeDict[strDimensions] = Cube(nx, ny, nz)            
        
        #print ('hi im: ', strDimensions)
        currIndex = cubeDict[strDimensions].index
        
        newplot1list = numpy.zeros(shape=(currIndex+1, 2))
        newplot1list[0:currIndex] = cubeDict[strDimensions].plot1list          
        newplot1list[currIndex] = [out['Machine Summary']['Distributed Processes'], out['Benchmark Time Summary']['Total']]           
        cubeDict[strDimensions].plot1list = newplot1list
        
        newplot2list = numpy.zeros(shape=(currIndex+1, 2))        
        newplot2list[0:currIndex] = cubeDict[strDimensions].plot2list
        newplot2list[currIndex] = [out['Machine Summary']['Distributed Processes'], out['GFLOP/s Summary']['Raw Total']]           
        cubeDict[strDimensions].plot2list = newplot2list        
        
        newplot3list = numpy.zeros(shape=(currIndex+1, 2))        
        newplot3list[0:currIndex] = cubeDict[strDimensions].plot3list
        newplot3list[currIndex] = [out['Machine Summary']['Distributed Processes'], out['Floating Point Operations Summary']['Total']]           
        cubeDict[strDimensions].plot3list = newplot3list
        
        newplot4list = numpy.zeros(shape=(currIndex+1, 2))        
        newplot4list[0:currIndex] = cubeDict[strDimensions].plot4list
        newplot4list[currIndex] = [out['Machine Summary']['Distributed Processes'], out['Memory Use Information']['Total memory used for data (Gbytes)']]           
        cubeDict[strDimensions].plot4list = newplot4list                
        
        currIndex = currIndex + 1
        cubeDict[strDimensions].index = currIndex         

                            
    i = i + 1

print ('number of files: ', i)

plt.figure(1,figsize=(15,6))
#plotGraphs
plotIt(1, 211, 'number of cores', 'run time (sec)')
plotIt(2, 212, 'number of cores', 'GFLOPs')
plt.savefig("hpcgFig1.png")

plt.figure(2,figsize=(15,6))
plotIt(3, 211, 'number of cores', 'Floating Point Operations')
plotIt(4, 212, 'number of cores', 'Total memory used (Gbytes)')
plt.savefig("hpcgFig2.png")