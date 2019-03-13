import cv2
import numpy as np
import sys
from pprint import pprint

img = cv2.imread(sys.argv[1])
(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

img_bin = 255-img_bin
cv2.imwrite("Image_bin.jpg", img_bin)

kernel_length = np.array(img).shape[1]//80

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

img_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=100)
vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)
#cv2.imwrite("verticle_lines.jpg", vertical_lines_img)

img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=100)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
#cv2.imwrite("horizontal_linses.jpg", horizontal_lines_img)

alpha = 0.5
beta = 1.0 - alpha

img_final_bin = cv2.addWeighted(vertical_lines_img, alpha, horizontal_lines_img, beta, 0.0)
img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
img_final_bin = cv2.cvtColor(img_final_bin, cv2.COLOR_BGR2GRAY);
(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY)
cv2.imwrite("img_final_bin.jpg", img_final_bin)

(contours, hierarchy) = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(cnts, method="left-to-right"):
	reverse = False
	i = 0
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key = lambda b:b[1][1], reverse=reverse))
	return (cnts, boundingBoxes)

(contours, boundingBoxes) = sort_contours(contours)

for c in contours:
	x,y,w,h = cv2.boundingRect(c)
	if (w > 30 and h > 30):
		new_img = img[y:y+h, x:x+w]
		cv2.imshow('image', new_img)
		cv2.waitKey(5000)
		cv2.destroyAllWindows()

exit()
