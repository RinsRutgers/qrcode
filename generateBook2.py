from reportlab.graphics.barcode import qr
import qrcode
from PIL import Image
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader


#----------------------------------------------------------------------
def createBook(uuid):
    """
    Create qr code with graphs and embed in a PDF
    """
    c = canvas.Canvas("book.pdf", pagesize=A4)

    def createPage(c, p):
        widthPage, heightPage = A4
        # draw a QR code
        d = []
        for qr_number in range(0,4):
            qrText = f"{uuid}.{p}.{qr_number}"
            qr1 = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr1.add_data(qrText)
            qr1.make(fit=True)
            qr_code = qr1.make_image(fill_color="black", back_color="white")
            matrix = qr_code.size
            print(matrix)
            # Get the bounding box of the QR code
            width = matrix[0]
            height = matrix[1]

            d.append(qr_code)
            # d[qr_number] = Drawing(90, 90)
            # d[qr_number].add(qr_code)
            qr_placement_x = widthPage - width
            qr_placement_y = heightPage - height
        dayHeight = heightPage - 80
        dayText = f'Dag {p}'
        c.drawString(90, dayHeight, dayText)
        # qr_code = Image.open(d[2])

        # c.drawImage(d[2], 0, 0)
        renderPDF.draw(d[2], c, 0, 0)
        renderPDF.draw(d[1], c, qr_placement_x, qr_placement_y)
        renderPDF.draw(d[0], c, 0, qr_placement_y)
        renderPDF.draw(d[3], c, qr_placement_x, 0)
        c.drawImage("static/graph.png", 15, -300, 550, preserveAspectRatio=True)
        
    
    for p in range(1, 15):
        createPage(c, p)
        c.showPage()

    c.save()
    
if __name__ == "__main__":
    createBook("RR.1234")