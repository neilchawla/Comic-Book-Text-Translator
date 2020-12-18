import cv2
import pytesseract
from googletrans import Translator

translator = Translator()

img = cv2.imread("future.jpeg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.Canny(img, 100, 200)
# OTSU Threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img.copy()

# Adding boxes to identified characters
h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

cv2.imshow('Output', img)
cv2.waitKey(0)

# Creating a new text file
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Open the file in append mode
    file = open("recognized.txt", "a")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(im2)
    jap = translator.translate(text, 'ja')
    print("Original text: ", text)
    print("========JAPANESE============")
    print(jap)

    # Saving translated text to the file
    file.write(text)
    file.write("\n")

    file.close
