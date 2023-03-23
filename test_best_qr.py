import qrcode
from PIL import Image
from PyPDF2 import PdfWriter
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics import renderPDF

def createBook(uuid):
    """
    Create qr code with graphs and embed in a PDF
    """
    c = canvas.Canvas("book_test.pdf", pagesize=A4)

    def createPage(c, p):
        widthPage, heightPage = A4
        # draw a QR code
        # List of data to encode
        data = ['Data 1', 'Data 2', 'Data 3', 'Data 4']

        # Generate QR codes and save them to files
        for i, d in enumerate(data):
            qr = qrcode.QRCode(version=1, box_size=10, border=4, )
            qr.add_data(d)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            print(img.size[0])
            qr_placement_x = widthPage - img.size[0]
            qr_placement_y = heightPage - img.size[1]
            
            # img.save(f'qrcode{i+1}.png')
            c.drawInlineImage(img, 0, 0, 0, preserveAspectRatio=True)
        
    
    for p in range(1, 15):
        createPage(c, p)
        c.showPage()

    c.save()
    
if __name__ == "__main__":
    createBook("RR.1234")