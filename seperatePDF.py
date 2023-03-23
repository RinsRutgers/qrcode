from pdf2image import convert_from_path
import os

import cv2
import numpy as np
import imutils

from PIL import Image, ImageDraw
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode


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
    path_list = pdf_to_jpg("scan/pdf/colour/Scan-rins_rutgers-0540_001.pdf", "scan/pdf/colour/converted")
    for path in path_list:
        decoded_info = detect_qr_code(path)
        print(decoded_info)

    for path in path_list:
        decoded_info = detect_qr_code_zbar(path)
        for data in decoded_info:
            print(data.data)
