from pdf2image import convert_from_path
import os

import cv2
import numpy as np
import imutils

from PIL import Image, ImageDraw
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode

def crop_image(img):
    # Read image
    img = cv2.imread(img)
    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
    img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)
    puntA = 0
    puntB = 0
    puntC = 0
    puntD = 0

    for s, p in zip(decoded_info, points):
        qrScannedNumber = s.split('.')
        number = int(qrScannedNumber[3])
        print(f"proefpersoon: {decoded_info}")
        # print(number)
        if number == 0:
            print(f'dag: {int(qrScannedNumber[2])}')
            # print(p[3])
            puntA = p[3].astype(int)
        elif number == 1:
            # print('qr punt 1:')
            # print(p[2])
            puntB = p[2].astype(int)
        elif number == 2:
            # print('qr punt 2:')
            # print(p[0])
            puntC = p[0].astype(int)
        elif number == 3:
            # print('qr punt 3:')
            # print(p[1])
            puntD = p[1].astype(int)
        # img = cv2.putText(img, number, p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
        img = cv2.putText(img, str(p[0]), p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)

    # print(f'puntA: {puntA}')
    # print(f'puntB: {puntB}')
    # print(f'puntC: {puntC}')
    # print(f'puntD: {puntD}')

    cv2.circle(img, puntA, 5, (255,0,0), 20)
    cv2.circle(img, puntB, 5, (255,0,0), 20)
    cv2.circle(img, puntC, 5, (255,0,0), 20)
    cv2.circle(img, puntD, 5, (255,0,0), 20)

    img = cv2.line(img, puntA, puntC, (0, 0, 255), 5) 
    img = cv2.line(img, puntB, puntD, (0, 0, 255), 5) 


    deltaXAC = puntA[0] - puntC[0]
    deltaYAC = puntA[1] - puntC[1]

    deltaXBD = puntB[0] - puntD[0]
    deltaYBD = puntB[1] - puntD[1]

    XE = puntA[0] - int(0.18 * deltaXAC)
    YE = puntA[1] - int(0.18 * deltaYAC)

    XF = puntA[0] - int(0.68 * deltaXAC)
    YF = puntA[1] - int(0.68 * deltaYAC)

    XG = puntB[0] - int(0.18 * deltaXBD)
    YG = puntB[1] - int(0.18 * deltaYBD)

    XH = puntB[0] - int(0.68 * deltaXBD)
    YH = puntB[1] - int(0.68 * deltaYBD)

    cv2.circle(img, (XE, YE), 3, (255,0,0), 20)
    cv2.circle(img, (XF, YF), 3, (255,0,0), 20)

    cv2.circle(img, (XG, YG), 3, (255,0,0), 20)
    cv2.circle(img, (XH, YH), 3, (255,0,0), 20)

    input = np.float32([[XE,YE], [XG,YG] , [XF,YF], [XH,YH]])
    output = np.float32([[0,0], [2084,0],[0,1100], [2084,1100]])

    # compute perspective matrix
    matrix = cv2.getPerspectiveTransform(input,output)

    # do perspective transformation setting area outside input to black
    imgOutput = cv2.warpPerspective(img, matrix, (2084,1100), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    # cv2.imwrite("graph_warped.jpg", imgOutput)

    # Cropping an image
    cropped_image = imgOutput[0:1100, 130:2000]
    

    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    (T, threshInv) = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV,
 	cv2.THRESH_OTSU)


    return(threshInv, cropped_image)

def seperate(cropped_img_inv, cropped_image):
    height, width = cropped_img_inv.shape
    cv2.imshow(f"cropped_img_inv", cropped_img_inv)
    cv2.imshow(f"cropped_image", cropped_image)

    # print(height)
    # print(width)
    score = []
    columns = []
    col_width = int(width/10)
    for j in range(10):
        col_start = j * col_width
        col_end = min((j+1) * col_width, width)
        col = cropped_img_inv[0:width, col_start:col_end]
        columns.append(col)
        cv2.imshow(f"column_{j}", columns[j])
        
        cropped_image_lines = cv2.line(cropped_image, (col_end, 0), (col_end, height), (0, 0, 255), 5) 
        cv2.imshow(f"line", cropped_image_lines)
        row_height = int(height/11)
        highest = 0
        highestIndex = 0
        for i in range(11):
            
            row_start = i * row_height
            row_end = min((i+1) * row_height, height)

            row = columns[j][row_start:row_end, 0:col_width]
            cropped_image_lines = cv2.line(cropped_image, (0, row_end), (width, row_end), (0, 0, 255), 5) 
            # cv2.imshow(f"row: {10-i} of column_{j}", row)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            white = cv2.countNonZero(row)
            if (white > highest):
                print(f"highest: {highest}    current white: {white}     i:{i}    score:{score}")
                
                highestIndex = i
                highest = white
            # cv2.imshow(f"col{j} row{i}", columns[j][i])
        if (highest > 50):
            score.append(10-highestIndex)
        else:
            score.append("NaN")

        print(f"highestIndex: {highestIndex}")        
    print(f"score: {score}")
    cv2.waitKey(0)
            # columns[j][i] = row

def detect_qr_code_zbar(image_path):
    image = Image.open(image_path)
    decoded_info = decode(image,  symbols=[ZBarSymbol.QRCODE])
    return decoded_info

def detect_qr_code(image_path):
    img = cv2.imread(image_path)

    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

    img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)

    return decoded_info

def pdf_to_jpg(pdf_path, output_dir):
    """
    Convert each page of a PDF document to a separate JPEG image.

    :param pdf_path: the path to the input PDF document
    :param output_dir: the directory to save the output JPEG images
    """
    # convert the PDF pages to a list of PIL image objects
    pages = convert_from_path(pdf_path)

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # iterate through the pages and save each one as a JPG image
    jpg_paths = []
    for i, page in enumerate(pages):
        jpg_path = f'{output_dir}/page_{i+1}.jpg'
        page.save(jpg_path, 'JPEG')
        jpg_paths.append(jpg_path)
    
    return jpg_paths

if __name__ == "__main__":
    path_list = pdf_to_jpg("scan/pdf/colour/Scan-rins_rutgers-0545_001.pdf", "scan/pdf/colour/converted")
    for path in path_list:
        decoded_info = detect_qr_code(path)
        # print(decoded_info)
        cropped_img_inv, cropped_image = crop_image(path)
        seperate(cropped_img_inv, cropped_image)
    # for path in path_list:
    #     decoded_info = detect_qr_code_zbar(path)
    #     for data in decoded_info:
    #         print(data.data)
