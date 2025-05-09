#!/usr/bin/python

#import library
import cv2
import easygui
import numpy as np
import cv2
import typing

class PencilSketch:
    def __init__(
        self,
        blur_simga: int = 5,
        ksize: typing.Tuple[int, int] = (0, 0),
        sharpen_value: int = None,
        kernel: np.ndarray = None,
        ) -> None:
        """
        Args:
            blur_simga: (int) - sigma ratio to apply for cv2.GaussianBlur
            ksize: (float) - ratio to apply for cv2.GaussianBlur
            sharpen_value: (int) - sharpen value to apply in predefined kernel array
            kernel: (np.ndarray) - custom kernel to apply in sharpen function
        """
        self.blur_simga = blur_simga
        self.ksize = ksize
        self.sharpen_value = sharpen_value
        self.kernel = np.array([[0, -1, 0], [-1, sharpen_value,-1], [0, -1, 0]]) if kernel == None else kernel


    def dodge(self, front: np.ndarray, back: np.ndarray) -> np.ndarray:
        """The formula comes from https://en.wikipedia.org/wiki/Blend_modes
        Args:
            front: (np.ndarray) - front image to be applied to dodge algorithm
            back: (np.ndarray) - back image to be applied to dodge algorithm

        Returns:
            image: (np.ndarray) - dodged image
        """
        result = back*255.0 / (255.0-front) 
        result[result>255] = 255
        result[back==255] = 255
        return result.astype('uint8')

    def sharpen(self, image: np.ndarray) -> np.ndarray:
        """Sharpen image by defined kernel size
        Args:
            image: (np.ndarray) - image to be sharpened

        Returns:
            image: (np.ndarray) - sharpened image
        """
        if self.sharpen_value is not None and isinstance(self.sharpen_value, int):
            inverted = 255 - image
            return 255 - cv2.filter2D(src=inverted, ddepth=-1, kernel=self.kernel)

        return image

cont = True
pic_selection = True
save = True
#loop that always the user to select a picture and convert it to a sketch. They can do this as many times as they like
while cont == True:
    easygui.msgbox("Please select an image to convert to a pencil sketch", "Welcome", ok_button="OK")

    #this loop forces the user to select and image or ends the program
    while pic_selection == True:
        #get image location and the image file name
        filename = easygui.fileopenbox(filetypes=("Image Files", '*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp'))

        if filename:
            #read in the image
            img = cv2.imread(filename)
            break
        else:
            msg = "No selection made. Do you wish to continue?"
            title = "No selection"
            if easygui.ynbox(msg, title):     #show a yes/NO dialog
                True  #user chose yes
            else:
                quit() #user chose no and closes the program

    #Alowing the user to select the amount of detail they would like in the sketch
    choices = ["Least", "Normal", "Most"]
    selection_index = easygui.indexbox("How much detail would you like for the sketch:", "Detail Selection", choices=choices)
    if selection_index is not None:
        if choices[selection_index] == "Least":
            selection = 1
        elif choices[selection_index] == "Normal":
            selection = 2
        elif choices[selection_index] == "Most":
            selection = 3
    else:
        # User canceled the selection
        easygui.msgbox("Selection cancelled", "Cancel")
        quit()

    #these 3 if statements determine the blur and sharpness values that get passed changing the level of sketch detail
    if selection == 1:
        pencil_Sketch = PencilSketch(blur_simga=1.5, sharpen_value=5)
        grayscale = np.array(np.dot(img[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)
        grayscale = np.stack((grayscale,) * 3, axis=-1) # convert 1 channel grayscale image to 3 channels grayscale

        inverted_img = 255 - grayscale

        blur_img = cv2.GaussianBlur(inverted_img, ksize=pencil_Sketch.ksize, sigmaX=pencil_Sketch.blur_simga)

        final_img = pencil_Sketch.dodge(blur_img, grayscale)

        sharpened_image = pencil_Sketch.sharpen(final_img)
            
    elif selection == 2:
        pencil_Sketch = PencilSketch(blur_simga=4, sharpen_value=5)
        grayscale = np.array(np.dot(img[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)
        grayscale = np.stack((grayscale,) * 3, axis=-1) # convert 1 channel grayscale image to 3 channels grayscale

        inverted_img = 255 - grayscale

        blur_img = cv2.GaussianBlur(inverted_img, ksize=pencil_Sketch.ksize, sigmaX=pencil_Sketch.blur_simga)

        final_img = pencil_Sketch.dodge(blur_img, grayscale)

        sharpened_image = pencil_Sketch.sharpen(final_img)
        
    elif selection == 3:
        pencil_Sketch = PencilSketch(blur_simga=15, sharpen_value=5)
        grayscale = np.array(np.dot(img[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)
        grayscale = np.stack((grayscale,) * 3, axis=-1) # convert 1 channel grayscale image to 3 channels grayscale

        inverted_img = 255 - grayscale

        blur_img = cv2.GaussianBlur(inverted_img, ksize=pencil_Sketch.ksize, sigmaX=pencil_Sketch.blur_simga)

        final_img = pencil_Sketch.dodge(blur_img, grayscale)

        sharpened_image = pencil_Sketch.sharpen(final_img)

    #show the image
    cv2.imshow('Original Image', img)
    cv2.imshow('New Image', sharpened_image)
    cv2.waitKey(0) 
    
    msg = "Do you want to save the sketch?"
    title = "Save"
    #asking the user if they would like to save the picture
    if easygui.ynbox(msg, title):     # show a yes/no dialog
        True  # user chose Continue
        while save == True:
            path = easygui.filesavebox(filetypes="*.png")
            if path:
                #save the image
                path = path + ".png"
                cv2.imwrite(path, sharpened_image)
                save = False
            else:
                msg = "Are you sure you dont want to save the sketch?"
                title = "No selection"
                if easygui.boolbox(msg, title, ["save", "cancel"]):     #show a yes/NO dialog
                    True  #user chose yes
                else:
                    break


    msg = "Would you like to convert another image"
    title = "Convert again"
    if easygui.ynbox(msg, title):     # show a yes/NO dialog
        True  # user chose Continue
    else:
        cont = False
quit()