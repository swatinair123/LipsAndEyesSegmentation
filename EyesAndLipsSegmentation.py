# import the necessary packages
#from pyimagesearch import imutils
import numpy as np
import argparse
import cv2
lower = np.array([8, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

for i in range(1,9) :
	
	frame= cv2.imread("TestImages/"+str(i)+".jpg")
	frame=cv2.resize(frame,(400,400))
	#framergb2bgrba=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
	#cv2.imshow("BGRtoAlpha",framergb2bgrba)
	frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#cv2.imshow("grayImage",frameGray)
	#frame = imutils.resize(frame, width = 400)
	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	cv2.imshow("HSV",converted)
	#creating teethmask
	# sizeTeethMask = 400, 400
	# teethMask = np.zeros(sizeTeethMask , dtype=np.uint8)
	

	
	#Creating hair mask
	sizeHairMask = 400, 400
	hairMask = np.zeros(sizeHairMask , dtype=np.uint8)
	for y in range (0,400):
		for x in range (0,400):
			
			if (converted[y,x][0]>converted[y,x][1]) and (converted[y,x][0]>converted[y,x][2]) :
				
				hairMask[y,x]=255
	#cv2.imshow("hairMask",hairMask)

	skinMask = cv2.inRange(converted, lower, upper)
	skinMask=~skinMask
	#detect teeth
	for y in range (200,350):
		for x in range (150,250):
			if (converted[y,x][2]>=180 and converted[y,x][1]<80 and converted[y,x][0]<20) :
				skinMask[y,x]=0
	for y in range (100,200):
		for x in range (100,300):
			if (converted[y,x][2]>=150 and converted[y,x][1]<100 and converted[y,x][0]<10) :
				skinMask[y,x]=255
	#cv2.imshow("skinMask",skinMask)
	for y in range(0,400):
	    for x in range(0,400):
	        if (y<100)or(y>350)or(x<120)or(x>300):
	            skinMask[y, x] = 0
    #
	# # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
	# # teethMask = cv2.erode(teethMask, kernel, iterations = 2)
	# # cv2.imshow("teethMaskerosion",teethMask)
	# # teethMask = cv2.dilate(teethMask, kernel, iterations = 2)
	# # cv2.imshow("teethMaskdialt",teethMask)
	# #cv2.imshow("skinMask_withTeeth",skinMask)
	# # for y in range(0,400):
	# #      for x in range(0,400):
	# #          if (y >250):
	# #              skinMask[y, x] = 255
	# # for y in range(0,400):
	# #     for x in range(0,400):
	# #         if (x <100)or(x>300):
	# #                 skinMask[y, x] = 255
	# #             # if (x not in range(100,300)):
	# #             #     skinMask[y, x] = 0
	# # cv2.imshow("Cropped",skinMask)
	# 	# apply a series of erosions and dilations to the mask
	# 	# using an elliptical kernel
	
	#cv2.imshow("skinMask2",skinMask)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	skinMask = cv2.erode(skinMask, kernel, iterations = 3)
	#cv2.imshow("skinMaskerosion",skinMask)
	skinMask = cv2.dilate(skinMask, kernel, iterations = 3)
	#cv2.imshow("skinmaskdila",skinMask)
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
	for y in range(0,400):
		for x in range(0,400):
			if (groundTruthImage[y,x][0]<=50 and groundTruthImage[y,x][1]>=240 and groundTruthImage[y,x][2]>=250):
				groundTruthMask[y,x]=255
	cv2.imshow("GtMask",groundTruthMask)
	meanAbsDistance=np.mean(skinMask-groundTruthMask)	
	print("meanAbsDistance for "+str(i)+".jpg is",meanAbsDistance)		
	#skin = cv2.bitwise_and(frame, frame, mask = skinMask)
	# 	# show the skin in the image along with the mask
	cv2.imwrite(("Results/Segmented"+str(i)+".jpg"),segmentedResultConcat)
	
	cv2.waitKey(1)
