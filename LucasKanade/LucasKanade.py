import math
from scipy import signal
from PIL import Image
import numpy as np
from numpy import *
from matplotlib import pyplot as plt
from pylab import *
import random
import cv2
import os


def lucas_kanade(Image1,Image2,ImageLocation):
    t = 0.3
    I1 = np.array(Image1)
    I2 = np.array(Image2)
    S = np.shape(I1)
    
    I1_smooth = cv2.GaussianBlur(I1,(3,3),0)
    I2_smooth = cv2.GaussianBlur(I2,(3,3),0)
    
    Ix = signal.convolve2d(I1_smooth,[[-0.25,0.25],[-0.25,0.25]],'same')+signal.convolve2d(I2_smooth,[[-0.25,0.25],[-0.25,0.25]],'same')
    Iy = signal.convolve2d(I1_smooth,[[-0.25,-0.25],[0.25,0.25]],'same')+signal.convolve2d(I2_smooth,[[-0.25,-0.25],[0.25,0.25]],'same')
    It = signal.convolve2d(I1_smooth,[[0.25,0.25],[0.25,0.25]],'same')+signal.convolve2d(I2_smooth,[[-0.25,-0.25],[-0.25,-0.25]],'same')
    
    features = cv2.goodFeaturesToTrack(I1_smooth,10000,0.01,10)
    feature = np.int0(features)
        
    u = v = np.nan*np.ones(S)
    
    for l in feature:
        j,i = l.ravel()
        
        IX = ([Ix[i-1,j-1],Ix[i,j-1],Ix[i-1,j-1],Ix[i-1,j],Ix[i,j],Ix[i+1,j],Ix[i-1,j+1],Ix[i,j+1],Ix[i+1,j-1]])
        IY = ([Iy[i-1,j-1],Iy[i,j-1],Iy[i-1,j-1],Iy[i-1,j],Iy[i,j],Iy[i+1,j],Iy[i-1,j+1],Iy[i,j+1],Iy[i+1,j-1]])
        IT = ([It[i-1,j-1],It[i,j-1],It[i-1,j-1],It[i-1,j],It[i,j],It[i+1,j],It[i-1,j+1],It[i,j+1],It[i+1,j-1]])
        
        LK = (IX,IY)
        LK = np.matrix(LK)
        LK_T = np.array(np.matrix(LK))
        LK = np.array(np.matrix.transpose(LK))
        
        A1 = np.dot(LK_T,LK)
        A2 = np.linalg.pinv(A1)
        A3 = np.dot(A2,LK_T)
        
        (u[i,j],v[i,j]) = np.dot(A3,IT)
    
    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)    
    plt.imshow(I1)

    for i in range(S[0]):
        for j in range(S[1]):
            if abs(u[i,j])>t or abs(v[i,j])>t:
                plt.arrow(j,i,v[i,j],u[i,j],head_width = 5, head_length = 5, color = 'r')
    
    plt.close()
    fig.savefig(ImageLocation+'.jpg')

Image1 = Image.open('basketball1.png').convert('L')
Image2 = Image.open('basketball2.png').convert('L')
lucas_kanade(Image1, Image2,'OpticalFlow')

def optical_flow(videoname):
    cap = cv2.VideoCapture(videoname)
    i=0

    framefolder = videoname+'Frames'
    opticalflowfolder = 'OpticalFlow'
    
    os.mkdir(framefolder)
    os.mkdir(os.path.join(framefolder, opticalflowfolder))
    
    while(cap.isOpened()):
        ret,frame = cap.read()
        if ret == False:
            break
    
        if i%10 == 0:
            cv2.imwrite(framefolder+'/frame%d.jpg'%i,frame)    
        i += 1
        
    number_of_frames = i//10
    
    for i in range(0,number_of_frames):
        image1 = Image.open(framefolder+('/frame%d.jpg'%(i*10))).convert('L')
        image2 = Image.open(framefolder+('/frame%d.jpg'%((i+1)*10))).convert('L')
    
        lucas_kanade(image1, image2,framefolder+'/'+opticalflowfolder+('/oframe%d'%i))

optical_flow('Butterfly.mp4')



