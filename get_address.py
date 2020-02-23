'''
USAGE:
python get_address.py -i adhaar.jpeg 

'''

# import necessary packages
import numpy as np
import cv2
import pytesseract
import re
import argparse

#load image from commandline
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])


copy = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#to remove noise 
blur=cv2.medianBlur(gray ,3)

# clean the image using otsu method with the inversed binarized image
ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

#processing par by par boxing
def process_boxes(thresh,output):	
	# assign a rectangle kernel size
	kernel = np.ones((5,5), 'uint8')	
	par_img = cv2.dilate(thresh,kernel,iterations=7)

	(contours, _) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	## for debugging: 
	#count=len(contours)
	#print(count)
	
	extr_text = []
	for cnt in contours:
		
		x,y,w,h = cv2.boundingRect(cnt)
		
		## to see the bounding boxes for getting roi:
		cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)
		
		roi=output[y:y+h, x:x+w]
		extr_text.append(pytesseract.image_to_string(roi))

	#to view all the extracted text:
	'''
	for i in range(len(extr_text)):
		print(i+1)
		
		print(extr_text[i])
	'''
	
	#to match with block of text starting with Address
	pattern=re.compile("Address:")
	for i in range(len(extr_text)):
		
		if (pattern.match(extr_text[i].strip())):
			print(extr_text[i])
			break

	return output	


#to print the bounding boxes, if needed
boxed_output = process_boxes(th,copy)
cv2.imwrite("adhaar_boxes.jpg", boxed_output)

cv2.waitKey(0)
