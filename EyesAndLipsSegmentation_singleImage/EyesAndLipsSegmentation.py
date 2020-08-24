# import the necessary packages
#from pyimagesearch import imutils
import numpy as np
import argparse
import cv2
lower = np.array([8, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

for i in range(1,2) :
	frame= cv2.imread("TestImages/"+str(i)+".jpg")
	frame=cv2.resize(frame,(400,400))
	frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	cv2.imshow("HSV",converted)

	skinMask = cv2.inRange(converted, lower, upper)
	skinMask=~skinMask
	cv2.imshow("skinMaskinitial",skinMask)
	for y in range(0,400):
	    for x in range(0,400):
	        if (y<100)or(y>350)or(x<120)or(x>300):
	            skinMask[y, x] = 0
    
	cv2.imshow("skinMask2",skinMask)
	kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
	skinMask = cv2.erode(skinMask, kernel1, iterations =3)
	cv2.imshow("skinMaskerosion",skinMask)
	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	skinMask = cv2.dilate(skinMask, kernel2, iterations =3)
	cv2.imshow("skinmaskdila",skinMask)
	# 	# blur the mask to help remove noise, then apply the
	# 	# mask to the frame
	skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
	#finalMask=cv2.cvtColor(skinMask,cv2.COLOR_GRAY2BGR)
	finalMask = np.zeros((400,400,3), np.uint8)
	finalMask[:,0:400] = (128,0,128)
	for y in range(0,400):
		for x in range(0,400):
			if skinMask[y,x]==255:
				finalMask[y,x][2]=255
				finalMask[y,x][1]=255
				finalMask[y,x][0]=0
			
	#cv2.imshow("finalMask",finalMask)
	segmentedResult=cv2.add(frame,finalMask)
	segmentedResultConcat = np.concatenate((frame, finalMask,segmentedResult), axis=1)
	cv2.imshow("segmentation result",segmentedResultConcat)
	groundTruthImage=cv2.imread("TestImages/"+str(i)+"_GT.jpg")
	
	groundTruthImage=cv2.resize(groundTruthImage,(400,400))
	cv2.imshow("GTImage",groundTruthImage)
	groundTruthMask = np.zeros((400,400), np.uint8)
	for y in range(0,400):#Convert the color mask ground truth to binary
		for x in range(0,400):
			if (groundTruthImage[y,x][0]<=50 and groundTruthImage[y,x][1]>=240 and groundTruthImage[y,x][2]>=250):
				groundTruthMask[y,x]=255
	cv2.imshow("GtMask",groundTruthMask)
	meanAbsDistance=np.mean(skinMask-groundTruthMask)	
	print("meanAbsDistance for "+str(i)+".jpg is",meanAbsDistance)		
	#skin = cv2.bitwise_and(frame, frame, mask = skinMask)
	# 	# show the skin in the image along with the mask
	cv2.imwrite(("Results/Segmented"+str(i)+".jpg"),segmentedResultConcat)
	
	cv2.waitKey(0)