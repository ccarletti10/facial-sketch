#import library
import cv2
import easygui


filename = easygui.fileopenbox()

#get image location and the image file name

#read in the image
img = cv2.imread(filename)

#convert image to greyscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#invert image
inverted_gray_img = 255 - gray_img

#blur image
blurred_img = cv2.GaussianBlur(inverted_gray_img, (21,21), 0)

#invert blurred image
inverted_blurred_img = 255 - blurred_img

#create pencil sketch image
pencil_sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)

#show the image
cv2.imshow('Original Image', img)
cv2.imshow('New Image', pencil_sketch_img)
cv2.waitKey(0)

path = easygui.filesavebox(filetypes="*.png")
path = path + ".png"
cv2.imwrite(path, pencil_sketch_img)