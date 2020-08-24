# LipsAndEyesSegmentation

Problem Description:

To segment Eyes and Lips in a given face .

Algorithm :
1. Read the input image.(Current dimensions of input image is 1024x1024x3 whichcorresponds to height ,width and the number of channels of the image .
2. Preprocessing: Resize the input image to 400x400 where height=400 and width=400 .
3. Convert the BGR image to HSV color model.
4. Create a binary mask for the skin region by thresholding the HSV image values between the lower and the upper ranges .
5. Invert the skin mask.
6. Detect teeth pixels by detecting the pixels which is satisfying the If condition values and set it to 0 .(Since we have to eliminate from the mask).
7. Detect eyes pixels by detecting the pixels which is satisfying the If condition values and set it to 255(SO that we dont miss out on any eyes pixels).
8. Eliminate all the pixels other then the centre area pixels ,since eyes and lips are located in the center of the face .
9. Perform Erosion and dilation on the skin mask obtained .
10. Use a Gaussian filter to remove any noises in the mask .
11. Validation is done Using Mean Accuracy Distance .
 
Prerequisites for running the code :

python 3.6 ,openCv
(Current code is tested on Ubuntu 18.04.4)

Steps to Run the code :
1.Open the Ubuntu terminal
2.Go to LipsAndEyesSegmentation folder and run the below command .
  python3 main.py

Test Images:
Test Images are in the TestImages folder

Results
The segmented results are stored in Results folder in the LipsAndEyesSegmentation repo.

