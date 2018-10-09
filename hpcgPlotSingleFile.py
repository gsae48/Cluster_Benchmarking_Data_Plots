# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:10:37 2016

@author: Ali
"""
#!/usr/bin/python
import yaml
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

#filename = sys.argv[0]

filename = 'hpcgRuns/cube104_nodes4_ppn44_core44.yaml'

with open(filename, 'r') as stream:
    out = yaml.load(stream)
    
    nx = out['Local Domain Dimensions']['nx']    
    ny = out['Local Domain Dimensions']['ny']        
    nz = out['Local Domain Dimensions']['nz']        
        
    #memory use  
    totalMem = out['Memory Use Information']['Total memory used for data (Gbytes)']    
    bytesPerEqu = out['Memory Use Information']['Bytes per equation (Total memory / Number of Equations)']

    gfpDDOt = out['GFLOP/s Summary']['Raw DDOT']
    gfpWAXPBY = out['GFLOP/s Summary']['Raw WAXPBY']
    gfpSpMV = out['GFLOP/s Summary']['Raw SpMV']
    gfpMG = out['GFLOP/s Summary']['Raw MG']    
    gfpTotal = out['GFLOP/s Summary']['Raw Total']
    
    tDDOT = out['Benchmark Time Summary']['DDOT']
    tWAXPBY = out['Benchmark Time Summary']['WAXPBY']
    tSpMV = out['Benchmark Time Summary']['SpMV']
    tMG = out['Benchmark Time Summary']['MG']
    
    ftDDOT = out['Floating Point Operations Summary']['Raw DDOT']
    ftWAXPBY = out['Floating Point Operations Summary']['Raw WAXPBY']
    ftSpMV = out['Floating Point Operations Summary']['Raw SpMV']
    ftMG = out['Floating Point Operations Summary']['Raw MG']

    read = out['GB/s Summary']['Raw Read B/W']
    write = out['GB/s Summary']['Raw Write B/W']
    totalRW = out['GB/s Summary']['Raw Total B/W']    

title = str(nx) + 'x' + str(ny) + 'x' + str(nz)    
labels = 'DDOT', 'WAXPBY', 'SpMV', 'MG';
sizes = [gfpDDOt, gfpWAXPBY, gfpSpMV, gfpMG]
colors = ['green', 'blue', 'brown', 'red']
                  
fig1 = plt.figure(1,figsize=(10,6))
fig1.canvas.set_window_title(title)
plt.title('GFLOPs', bbox={'facecolor':'0.8', 'pad':5})
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=10)
plt.savefig("pieGFLOPS.png")

sizes = [tDDOT, tWAXPBY, tSpMV, tMG]
fig2 = plt.figure(2,figsize=(10,6))
fig2.canvas.set_window_title(title)
plt.title('Timing', bbox={'facecolor':'0.8', 'pad':5})
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=10)
plt.savefig("pieTime.png")

sizes = [ftDDOT, ftWAXPBY, ftSpMV, ftMG]
fig3 = plt.figure(3,figsize=(10,6))
fig3.canvas.set_window_title(title)
plt.title('Floating Pt', bbox={'facecolor':'0.8', 'pad':5})
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=10)
plt.savefig("pieFltPt.png")

sizes = [read, write]
colors = ['red', 'green']
labels = 'read', 'write';
fig4 = plt.figure(3,figsize=(10,6))
fig4.canvas.set_window_title(title)
plt.title('Read and Write (GB/s)', bbox={'facecolor':'0.8', 'pad':5})
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=10)
plt.savefig("pieRW.png")

