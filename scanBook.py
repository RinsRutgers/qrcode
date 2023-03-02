import glob
import cv2
# import pandas as pd
import pathlib
import numpy as np



img = cv2.imread('pictures/IMG_8747.JPG')

width = 500
height = 350

qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
print(retval)
print(decoded_info)
print(points)
idx = []
# rearrange points to correspond to qrcode 
for info in decoded_info:
    print(info)
    qrScannedNumber = info.split('.')
    number = qrScannedNumber[3]
    print(points[int(number)])
    
    # points[int(number)]= points[int(number)]
    idx.append(int(number))
print
points[np.argsort(idx)]
print(points)

start_point = points[0][3].astype(int)
end_point = points[1][0].astype(int)
img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)

img = cv2.line(img, start_point, end_point, (0, 0, 255), 5) 
deltaX = int((points[0][3][0].astype(int) - points[1][0][0].astype(int)))
deltaY = int(points[1][0][1].astype(int) - points[0][3][1].astype(int))

XA = points[0][3][0].astype(int) - int(0.15 * deltaX)
YA = points[0][3][1].astype(int) + int(0.15 * deltaY)

XB = points[0][3][0].astype(int) - int(0.62 * deltaX)
YB = points[0][3][1].astype(int) + int(0.62 * deltaY)

start_point_right = points[2][2].astype(int)
end_point_right = points[3][1].astype(int)

img = cv2.line(img, start_point_right, end_point_right, (0, 0, 255), 5) 

deltaXRight = int((points[2][2][0].astype(int) - points[3][1][0].astype(int)))
deltaYRight = int(points[3][1][1].astype(int) - points[2][2][1].astype(int))

print(deltaXRight)
print(deltaYRight)

XC = points[2][2][0].astype(int) - int(0.15 * deltaXRight)
YC = points[2][2][1].astype(int) + int(0.15 * deltaYRight)
print(XC)
print(YC)
XD = points[2][2][0].astype(int) - int(0.62 * deltaXRight)
YD = points[2][2][1].astype(int) + int(0.62 * deltaYRight)
print(XD)
print(YD)


cv2.circle(img, (XA, YA), 5, (255,0,0), 20)
cv2.circle(img, (XB, YB), 5, (0,255,0), 20)

cv2.circle(img, (XC, YC), 5, (0,0,255), 20)
cv2.circle(img, (XD, YD), 5, (255,255,0), 20)

img = cv2.line(img, (XA, YA), (XC, YC), (0, 0, 255), 5) 
img = cv2.line(img, (XB, YB), (XD, YD), (0, 0, 255), 5) 

for s, p in zip(decoded_info, points):
    img = cv2.putText(img, s, p[0].astype(int),
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imwrite('qrcode_opencv.jpg', img)

input = np.float32([[XA,YA], [XC,YC] , [XB,YB], [XD,YD]])
output = np.float32([[0,0], [1000,0],[0,700], [1000,700]])

# compute perspective matrix
matrix = cv2.getPerspectiveTransform(input,output)

# do perspective transformation setting area outside input to black
imgOutput = cv2.warpPerspective(img, matrix, (1000,700), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
print(imgOutput.shape)
cv2.imwrite("graph_warped.jpg", imgOutput)