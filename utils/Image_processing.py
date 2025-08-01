import cv2
import numpy as np
from PIL import Image
import pytesseract

def load_image(uploaded_file):
    image = Image.open(uploaded_file).convert('RGB')
    return np.array(image)
    
def preprocessing_image(image_array):
    gray=cv2.cvtColor(image_array,cv2.COLOR_RGB2GRAY)
    height, width = gray.shape
    gray = cv2.resize(gray, (width * 2, height * 2))
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresholded = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return thresholded

def extract_text_from_image(image_array):
    if len(image_array.shape) == 2:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image_array, config=custom_config)

def resize_image(image_array,width=800):
    ratio=width/image_array.shape[1]
    dim=(width,int(image_array.shape[0]*ratio))
    return cv2.resize(image_array,dim,interpolation=cv2.INTER_AREA)
    