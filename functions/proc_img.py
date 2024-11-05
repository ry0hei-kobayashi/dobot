import os
from PIL import Image, ImageEnhance, ImageOps

def proc_img(input_image):
    #image_path = '../images/img.jpg'
    #image = Image.open(image_path)

    #cv2 to pil
    pil_image = Image.fromarray(input_image)

    # Convert to grayscale
    gray_image = ImageOps.grayscale(pil_image)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    
    # Invert BW
    inverted_image = ImageOps.invert(enhanced_image)
    
    # Save and display enhanced image
    enhanced_image_path = './images/img.jpg' # if you read this function from main.py
    inverted_image.save(enhanced_image_path)
    inverted_image.show()

