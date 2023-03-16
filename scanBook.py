import cv2
import numpy as np
import imutils


img = cv2.imread('pictures/IMG_8752.JPG')
cv2.imshow('image',img)
cv2.waitKey(0)

qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
# print(retval)


img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)
cv2.imshow('image',img)
cv2.waitKey(0)
puntA = 0
puntB = 0
puntC = 0
puntD = 0

for s, p in zip(decoded_info, points):
    qrScannedNumber = s.split('.')
    number = int(qrScannedNumber[3])
    print(number)
    if number == 0:
        print('qr punt 0:')
        print(p[3])
        puntA = p[3].astype(int)
    elif number == 1:
        print('qr punt 1:')
        print(p[2])
        puntB = p[2].astype(int)
    elif number == 2:
        print('qr punt 2:')
        print(p[0])
        puntC = p[0].astype(int)
    elif number == 3:
        print('qr punt 3:')
        print(p[1])
        puntD = p[1].astype(int)
    # img = cv2.putText(img, number, p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
    img = cv2.putText(img, str(p[0]), p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)

cv2.imshow('image',img)
cv2.waitKey(0)
print(f'puntA: {puntA}')
print(f'puntB: {puntB}')
print(f'puntC: {puntC}')
print(f'puntD: {puntD}')

cv2.circle(img, puntA, 5, (255,0,0), 20)
cv2.circle(img, puntB, 5, (255,0,0), 20)
cv2.circle(img, puntC, 5, (255,0,0), 20)
cv2.circle(img, puntD, 5, (255,0,0), 20)
cv2.imshow('image',img)
cv2.waitKey(0)

img = cv2.line(img, puntA, puntC, (0, 0, 255), 5) 
img = cv2.line(img, puntB, puntD, (0, 0, 255), 5) 
cv2.imshow('image',img)
cv2.waitKey(0)

deltaXAC = puntA[0] - puntC[0]
deltaYAC = puntA[1] - puntC[1]

deltaXBD = puntB[0] - puntD[0]
deltaYBD = puntB[1] - puntD[1]

print(deltaXBD)
print(deltaYBD)

XE = puntA[0] - int(0.2 * deltaXAC)
YE = puntA[1] - int(0.2 * deltaYAC)

XF = puntA[0] - int(0.64 * deltaXAC)
YF = puntA[1] - int(0.64 * deltaYAC)

XG = puntB[0] - int(0.2 * deltaXBD)
YG = puntB[1] - int(0.2 * deltaYBD)

XH = puntB[0] - int(0.64 * deltaXBD)
YH = puntB[1] - int(0.64 * deltaYBD)

cv2.circle(img, (XE, YE), 5, (255,0,0), 20)
cv2.circle(img, (XF, YF), 5, (255,0,0), 20)

cv2.circle(img, (XG, YG), 5, (255,0,0), 20)
cv2.circle(img, (XH, YH), 5, (255,0,0), 20)
cv2.imshow('image',img)
cv2.waitKey(0)

input = np.float32([[XE,YE], [XG,YG] , [XF,YF], [XH,YH]])
output = np.float32([[0,0], [2084,0],[0,1100], [2084,1100]])

# compute perspective matrix
matrix = cv2.getPerspectiveTransform(input,output)



# do perspective transformation setting area outside input to black
imgOutput = cv2.warpPerspective(img, matrix, (2084,1100), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
cv2.imwrite("graph_warped.jpg", imgOutput)
cv2.imshow('image',imgOutput)
cv2.waitKey(0)

# Cropping an image
cropped_image = imgOutput[0:1100, 200:1900]
 
# Display cropped image
cv2.imshow("cropped", cropped_image)
cv2.waitKey(0)

gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('image',gray)
cv2.waitKey(0)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('image',blurred)
cv2.waitKey(0)
(T, threshInv) = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV,
	cv2.THRESH_OTSU)
cv2.imshow("Threshold Binary Inverse", threshInv)
cv2.waitKey(0)

cnts = cv2.findContours(threshInv.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questionCnts = []
# loop over the contours
for c in cnts:
	# compute the bounding box of the contour, then use the
	# bounding box to derive the aspect ratio
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)
	# in order to label the contour as a question, region
	# should be sufficiently wide, sufficiently tall, and
	# have an aspect ratio approximately equal to 1
	if w >= 4 and h >= 4 and ar >= 0.8 and ar <= 1.2:
		questionCnts.append(c)
print(len(cnts))
print(len(questionCnts))

cv2.drawContours(cropped_image, questionCnts, -1, (0,255,0), 3)
cv2.imshow("Threshold Binary Inverse", cropped_image)
cv2.waitKey(0)



questionCnts = cv2.contours.sort_contours(questionCnts,
	method="left-to-right")[0]
correct = 0
# each question has 5 possible answers, to loop over the
# question in batches of 5
for (q, i) in enumerate(np.arange(0, len(questionCnts), 10)):
	# sort the contours for the current question from
	# left to right, then initialize the index of the
	# bubbled answer
	cnts = cv2.contours.sort_contours(questionCnts[i:i + 10])[0]
	bubbled = None

cv2.imwrite('qrcode_bare.jpg', cropped_image)