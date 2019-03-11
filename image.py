import cv2
import numpy as np

img = cv2.imread("testpdf.jpg")
(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

img_bin = 255-img_bin
cv2.imwrite("Image_bin2.jpg", img_bin)

kernel_length = np.array(img).shape[1]//80

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

img_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=100)
vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)
cv2.imwrite("verticle_lines.jpg", vertical_lines_img)

img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=100)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
cv2.imwrite("horizontal_linses.jpg", horizontal_lines_img)

exit();
