from pdf2image import convert_from_path
import os
import math
import cv2
import numpy as np

def crop_image(img):
    # Read image
    img = cv2.imread(img)
    qcd = cv2.QRCodeDetector()
    decodedText, points, _ = qcd.detectAndDecode(img)
    print(points)
    # Oorspronkelijke array met vier coördinaten
    
    
    img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)
    puntA = points[0][0].astype(int)
    puntB = points[0][1].astype(int)
    puntC = points[0][2].astype(int)
    puntD = points[0][3].astype(int)
    
    length_AD = np.linalg.norm(puntD - puntA)
    print(f'Lengte AD: {length_AD}')
    
    # Factor waarmee de driehoek wordt vergroot
    x = 5.4  # Vervang dit met de gewenste factor
    x2 = 2.2
    # Nieuwe afstand tussen punt A en het nieuwe punt C
    new_distance_AD = length_AD * x
    new_distance_AD2 = length_AD * x2
    
    angle = math.atan2(puntD[1] - puntA[1], puntD[0] - puntA[0])
    print(f'hoek: {angle}')
    
    new_C = puntA + np.array([new_distance_AD * math.cos(angle), new_distance_AD * math.sin(angle)])
    new_C_formatted = np.array([int(new_C[0]), int(new_C[1])])
    new_C2 = puntA + np.array([new_distance_AD2 * math.cos(angle), new_distance_AD2 * math.sin(angle)])
    new_C2_formatted2 = np.array([int(new_C2[0]), int(new_C2[1])])
    
    puntE = new_C2_formatted2
    puntF = new_C_formatted
    print(f'puntE: {puntE}')
    print(f'puntF: {puntF}')
    
    
    
    cv2.circle(img, new_C_formatted, 5, (0,255,0), 5)
    cv2.circle(img, new_C2_formatted2, 5, (0,255,0), 5)

    print(puntA)
    print(puntB)
    print(puntC)
    print(puntD)

    original_array = np.array([[[puntA[0], puntA[1]*2], [400, 200], [400, 800], [200, 800]]]) 
    img = cv2.polylines(img, original_array.astype(int), True, (0, 255, 255), 10)

    print(original_array)

    splittedText = decodedText.split('.')
    print(splittedText)
    
    cv2.circle(img, puntA, 5, (255,0,0), 5)
    cv2.circle(img, puntB, 5, (255,255,0), 5)
    cv2.circle(img, puntC, 5, (0,255,0), 5)
    cv2.circle(img, puntD, 5, (255,0,255), 5)
    
    img = cv2.line(img, puntA, puntC, (0, 0, 255), 5)   

    # Hoek bij punt A (in graden) en lengte van zijde AC
    # angle_A = angle_AC
    # length_AC = 200

    # # Richtingshoek van zijde AC (in radialen)
    # angle_AC = math.radians(angle_A)

    # # Bereken de coördinaten van punt C
    # C = new_C_formatted + np.array([length_AC * math.cos(angle_AC), length_AC * math.sin(angle_AC)])  # Coördinaten van punt C

    # # Coördinaten van punt C in de gewenste vorm
    # C_formatted = np.array([int(C[0]), int(C[1])])

    # print("Coördinaten van punt C:", C_formatted)
    # print(f'nieuwe punt: {C_formatted}')

    # cv2.circle(img, C_formatted, 5, (0,255,0), 5)
    # for s, p in zip(decodedText, points):
    #     qrScannedNumber = s.split('.')
    #     print(qrScannedNumber)
        # number = int(qrScannedNumber[5])
        # print(number)

        # img = cv2.putText(img, number, p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
        # img = cv2.putText(img, str(p[0]), p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow(f"cropped_image", img)
    cv2.waitKey(0)


    # img = cv2.line(img, puntA, puntC, (0, 0, 255), 5) 
    # img = cv2.line(img, puntB, puntD, (0, 0, 255), 5) 


    # deltaXAC = puntA[0] - puntC[0]
    # deltaYAC = puntA[1] - puntC[1]

    # deltaXBD = puntB[0] - puntD[0]
    # deltaYBD = puntB[1] - puntD[1]

    # XE = puntA[0] - int(0.18 * deltaXAC)
    # YE = puntA[1] - int(0.18 * deltaYAC)

    # XF = puntA[0] - int(0.68 * deltaXAC)
    # YF = puntA[1] - int(0.68 * deltaYAC)

    # XG = puntB[0] - int(0.18 * deltaXBD)
    # YG = puntB[1] - int(0.18 * deltaYBD)

    # XH = puntB[0] - int(0.68 * deltaXBD)
    # YH = puntB[1] - int(0.68 * deltaYBD)

    # cv2.circle(img, (XE, YE), 3, (255,0,0), 20)
    # cv2.circle(img, (XF, YF), 3, (255,0,0), 20)

    # cv2.circle(img, (XG, YG), 3, (255,0,0), 20)
    # cv2.circle(img, (XH, YH), 3, (255,0,0), 20)

    # input = np.float32([[XE,YE], [XG,YG] , [XF,YF], [XH,YH]])
    # output = np.float32([[0,0], [2084,0],[0,1100], [2084,1100]])

    # # compute perspective matrix
    # matrix = cv2.getPerspectiveTransform(input,output)

    # do perspective transformation setting area outside input to black
    # imgOutput = cv2.warpPerspective(img, matrix, (2084,1100), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    # cv2.imwrite("graph_warped.jpg", imgOutput)

    # Cropping an image
    # cropped_image = imgOutput[0:1100, 130:2000]
    

    # gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # (T, threshInv) = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV,
 	# cv2.THRESH_OTSU)


    return(img)
    # return(threshInv, cropped_image)

def seperate(cropped_img_inv, cropped_image):
    height, width = cropped_img_inv.shape
    cv2.imshow(f"cropped_img_inv", cropped_img_inv)
    cv2.imshow(f"cropped_image", cropped_image)

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
                highestIndex = i
                highest = white
            # cv2.imshow(f"col{j} row{i}", columns[j][i])
        if (highest > 50):
            score.append(10-highestIndex)
        else:
            score.append("NaN")
        cropped_image_lines = cv2.putText(cropped_image_lines, str(score[j]), (col_start+5 , height-5),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
        cv2.imshow(f"line", cropped_image_lines)
    print(f"score: {score}")
    

def detect_qr_code(image_path):
    attempts = 3
    decoded_info = None

    for _ in range(attempts):
        img = cv2.imread(image_path)
        qcd = cv2.QRCodeDetector()

        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
        if len(decoded_info) == 1:
            print(decoded_info)
            img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)
            # cv2.imshow(f"qr", img)
            # cv2.waitKey(0)
            break
        else:
            decoded_info = None
    # img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 10)
    
    if decoded_info is None:
    # if decoded_info is None or len(decoded_info) != 4:
        cv2.imshow(f"qr", img)
        cv2.waitKey(0)
        print("QR code detection failed.")

    
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
    path_list = pdf_to_jpg("./05041502.PDF", "../scan/pdf/colour/converted")
    for path in path_list:
        decoded_info = detect_qr_code(path)
        # cropped_img_inv, cropped_image = crop_image(path)
        img = crop_image(path)
        # seperate(cropped_img_inv, cropped_image)

