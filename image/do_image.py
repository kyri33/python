import cv2
import numpy as np
import sys
from pprint import pprint

def sort_func(x):
	bounds = x[1]
	return (bounds[0] + bounds[1] * 2)

def sort_contours(cnts):
	contours = []
	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		if w > 100 and h > 100:
			contours.append(c)
	if (len(contours) <= 1):
		return ([0], [0])
	boundingBoxes = [cv2.boundingRect(c) for c in contours]
	(cnts, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), \
							key = sort_func, reverse=False))
	return (cnts, boundingBoxes)

def strip_image(img):
	(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
	img_bin = 255-img_bin
	leng = np.array(img).shape[1]//80
	#if (int) (leng/4) > 1:
	#	leng = (int) (leng/4)
	vert_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (1, leng))
	hori_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (leng, 1))
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	img_tmp = cv2.erode(img_bin, vert_kern, iterations=100)
	img_vert = cv2.dilate(img_tmp, vert_kern, iterations=3)	

	img_tmp = cv2.erode(img_bin, hori_kern, iterations=100)
	img_hori = cv2.dilate(img_tmp, hori_kern, iterations=3)

	alpha = 0.5
	beta = 1.0 - alpha
	img_bin = cv2.addWeighted(img_vert, alpha, img_hori, beta, 0.0)
	img_bin = cv2.erode(~img_bin, kernel, iterations = 2)
	img_bin = cv2.cvtColor(img_bin, cv2.COLOR_BGR2GRAY)
	(thresh, img_bin) = cv2.threshold(img_bin, 128, 255, cv2.THRESH_BINARY)
	cv2.imshow('img', img_bin)
	cv2.waitKey(5000)
	cv2.destroyAllWindows()
	(thresh, img_bin) = cv2.threshold(img_bin, 128, 255, cv2.THRESH_BINARY)
	(cnts, hierarchy) = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	(cnts, boundingBoxes) = sort_contours(cnts)
	if len(cnts) <= 1:
		return	
	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		if (w > 80 and h > 50):
			new_img = img[y:y+h, x:x+w]
			cv2.imshow('img', new_img)
			cv2.waitKey(10000)
			cv2.destroyAllWindows()
			strip_image(new_img)

strip_image(cv2.imread(sys.argv[1]))
exit()
