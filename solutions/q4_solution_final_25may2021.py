# -*- coding: utf-8 -*-
"""Q4_Solution_final_25May2021.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WkuiO-06P84L2SXyFgr6ybCIvAR76xCX
"""

!sudo apt install tesseract-ocr
!pip install pytesseract
!pip install easyocr
!apt-get install poppler-utils 
!pip install PyMuPDF
!sudo python -m nltk.downloader all

!which tesseract

import pytesseract
from PIL import Image
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#from pdf2image import convert_from_path, convert_from_bytes
import os
import tempfile
#from pdf2image import convert_from_path
#import poppler
import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image

import pytesseract
from PIL import Image
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import tempfile
import cv2
import numpy as np

import cv2
import numpy as np

#img = cv2.imread('image1_1.jpg')

# get grayscale image
def get_grayscale(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
  return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
  return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
  kernel = np.ones((5,5),np.uint8)
  return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
  kernel = np.ones((5,5),np.uint8)
  return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
  kernel = np.ones((5,5),np.uint8)
  return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
  return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
  coords = np.column_stack(np.where(image > 0))
  angle = cv2.minAreaRect(coords)[-1]
  if angle < -45:
    angle = -(90 + angle)
  else:
    angle = -angle
  (h, w) = image.shape[:2]
  center = (w // 2, h // 2)
  M = cv2.getRotationMatrix2D(center, angle, 1.0)
  rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
  return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def flattenList(nestedList):
  
    # check if list is empty
    if not(bool(nestedList)):
        return nestedList
  
     # to check instance of list is empty or not
    if isinstance(nestedList[0], list):
  
        # call function with sublist as argument
        return flattenList(*nestedList[:1]) + flattenList(nestedList[1:])
  
    # call function with sublist as argument
    return nestedList[:1] + flattenList(nestedList[1:])

## Pytesseract Method

import fitz
import io
from PIL import Image
import pandas as pd
import pytesseract
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import re
import tempfile
import cv2
import numpy as np
from tqdm import tqdm

dataset = '/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Test'
df_train = pd.read_csv('/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Train.csv', sep=',', header=0)
df_test = pd.read_csv('/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Test.csv', sep=',', header=0)
output = []

for files in tqdm(os.listdir(dataset)):
  file_name=os.path.join(dataset, files)
  pdf_file = fitz.open(file_name)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.getImageList()
    for image_index, img in enumerate(page.getImageList(), start=1):
      xref = img[0]
      base_image = pdf_file.extractImage(xref)
      image_bytes = base_image["image"]
      image_ext = base_image["ext"]
      image = Image.open(io.BytesIO(image_bytes))
      image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb")) 

  
  #img = Image.open('image1_1.jpeg').convert('L')
  img = get_grayscale(cv2.imread('image1_1.jpeg'))
  text = pytesseract.image_to_string(img)
  processed_text = text.lower()
  processed_text = processed_text.replace('\n', ' ')
  processed_text = processed_text.replace('*', ' ')
  text_tokens = word_tokenize(processed_text)
  text_without_stopwords = [word for word in text_tokens if not word in stopwords.words()]
  processed_text = " ".join(text_without_stopwords)
  text_list = word_tokenize(processed_text)
  Total_Amount_List = []
  for index in range (len(text_list)):
    if text_list[index] == 'total' or text_list[index] == 'tot' or text_list[index] == 'tctal' or text_list[index] == 'tct':
      try:
        Total_Amount_List.append(text_list[index+1])
        Total_Amount_List.append(text_list[index+2])
      except IndexError:
        Total_Amount_List.append(0.0)


  print(Total_Amount_List)
  Total_Amount = [] 
  for item in Total_Amount_List:
    try:
      amt = [float(s) for s in re.findall(r'-?\d+\.?\d*', item)]
      Total_Amount.append(amt)
    except TypeError:
      pass
  Total_Amount = flattenList(Total_Amount)
  try:
    output.append(max(Total_Amount))
  except ValueError:
    output.append(0.0)

df_test["Predicted Amt 2"] = output
df_train.head()



'''
  Total_Amount_List = []
  for index in range (len(text_list)):
    if text_list[index] == 'total' or text_list[index] == 'tot':
      try:
        Total_Amount_List.append(text_list[index+1])
        Total_Amount_List.append(text_list[index+2])
      except IndexError:
        Total_Amount_List.append(0.0)


  print(Total_Amount_List)
  Total_Amount = [] 
  for item in Total_Amount_List:
    try:
      Total_Amount.append(float(item))
    except ValueError:
      pass
  try:
    output.append(max(Total_Amount))
  except ValueError:
    output.append(0.0)

df_test["Predicted Amt 2"] = output
df_train.head()
'''

df_test.head()

## Easy-OCR Method

import fitz
import io
from PIL import Image
import pandas as pd
import easyocr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import tempfile
import cv2
import numpy as np
from tqdm import tqdm

dataset = '/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Test'
df_train = pd.read_csv('/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Train.csv', sep=',', header=0)
df_test = pd.read_csv('/content/drive/MyDrive/CTRL_HACK_DEL/Final_Test_Q4/Dataset_test/Test.csv', sep=',', header=0)
output = []

for files in tqdm(os.listdir(dataset)):
  file_name=os.path.join(dataset, files)
  pdf_file = fitz.open(file_name)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.getImageList()
    for image_index, img in enumerate(page.getImageList(), start=1):
      xref = img[0]
      base_image = pdf_file.extractImage(xref)
      image_bytes = base_image["image"]
      image_ext = base_image["ext"]
      image = Image.open(io.BytesIO(image_bytes))
      image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb")) 

  
  #img = Image.open('image1_1.jpeg').convert('L')
  #img = get_grayscale(cv2.imread('image1_1.jpeg'))
  #text = pytesseract.image_to_string(img)
  reader = easyocr.Reader(['en'])
  text = reader.readtext('image1_1.jpeg', detail = 0)
  #text_list = text

  #processed_text = text.lower()
  #processed_text = processed_text.replace('\n', ' ')
  #processed_text = processed_text.replace('*', ' ')
  #text_tokens = word_tokenize(processed_text)
  #text_without_stopwords = [word for word in text_tokens if not word in stopwords.words()]
  #processed_text = " ".join(text_without_stopwords)
  #text_list = word_tokenize(processed_text)
  text_list = [x.lower() for x in text]
  Total_Amount_List = []
  for index in range (len(text_list)):
    if text_list[index] == 'total' or text_list[index] == 'tot' or text_list[index] == 'tctal' or text_list[index] == 'tct':
      try:
        Total_Amount_List.append(text_list[index+1])
        Total_Amount_List.append(text_list[index+2])
      except IndexError:
        Total_Amount_List.append(0.0)


  print(Total_Amount_List)
  Total_Amount = [] 
  for item in Total_Amount_List:
    try:
      amt = [float(s) for s in re.findall(r'-?\d+\.?\d*', item)]
      Total_Amount.append(amt)
    except TypeError:
      pass
  Total_Amount = flattenList(Total_Amount)
  try:
    output.append(max(Total_Amount))
  except ValueError:
    output.append(0.0)

df_test["Predicted Amt 2"] = output
df_train.head()

df_test.to_csv('Q4_submission_pytesseract_1.csv', header=True, index=False)

import fitz
import io
from PIL import Image
import pandas as pd
import easyocr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import tempfile
import cv2
import numpy as np
import re
from tqdm import tqdm

output = []
reader = easyocr.Reader(['en'])
text = reader.readtext('image1_1.jpeg', detail = 0)
print(text)
text_list = text
#processed_text = text.lower()
#processed_text = processed_text.replace('\n', ' ')
#processed_text = processed_text.replace('*', ' ')
#text_tokens = word_tokenize(processed_text)
#text_without_stopwords = [word for word in text_tokens if not word in stopwords.words()]
#processed_text = " ".join(text_without_stopwords)
#text_list = word_tokenize(processed_text)
text_list = [x.lower() for x in text]
Total_Amount_List = []
for index in range (len(text_list)):
  if text_list[index] == 'total' or text_list[index] == 'tot':
    try:
      Total_Amount_List.append(text_list[index+1])
      Total_Amount_List.append(text_list[index+2])
    except IndexError:
      Total_Amount_List.append(0.0)


print(Total_Amount_List)
#Total_Amount_List = [float(s) for s in re.findall(r'-?\d+\.?\d*', 'he33.45llo -42 I\'m a 32 string 30')]
Total_Amount = [] 
for item in Total_Amount_List:
  try:
    amt = [float(s) for s in re.findall(r'-?\d+\.?\d*', item)]
    Total_Amount.append(amt)
  except ValueError:
    pass
print(Total_Amount)
Total_Amount = flattenList(Total_Amount)
print(Total_Amount)
try:
  output.append(max(Total_Amount))
except ValueError:
  output.append(0.0)

print(max(Total_Amount))
print(output)