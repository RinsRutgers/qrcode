from pdf2image import convert_from_path
import os

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
    pdf_to_jpg("scan/pdf/colour/Scan-rins_rutgers-0533_001.pdf", "scan/pdf/colour/converted")