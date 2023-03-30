from reportlab.graphics.barcode import qr
import qrcode

from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics import renderPDF


#----------------------------------------------------------------------
def createBook(uuid):
    """
    Create qr code with graphs and embed in a PDF
    """
    c = canvas.Canvas("book.pdf", pagesize=A4)

    def createPage(c, p):
        widthPage, heightPage = A4
        # draw a QR code
        d = {}
        qr_size = 100  # set the size of the QR codes
        qr_border = 1  # set the border size of the QR codes
        for qr_number in range(0, 4):
            qrText = f"{uuid}.{p}.{qr_number}"
            qr = qrcode.QRCode(version=1, box_size=10, border=qr_border, error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(qrText)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            d[qr_number] = img
        # position the QR codes in the corners
        qr_x_margin = 20  # set the margin size for the x-axis
        qr_y_margin = 20  # set the margin size for the y-axis
        c.drawInlineImage(d[0], qr_x_margin, heightPage - qr_size - qr_y_margin, width=qr_size, height=qr_size)
        c.drawInlineImage(d[1], widthPage - qr_size - qr_x_margin, heightPage - qr_size - qr_y_margin, width=qr_size, height=qr_size)
        c.drawInlineImage(d[2], qr_x_margin, qr_y_margin, width=qr_size, height=qr_size)
        c.drawInlineImage(d[3], widthPage - qr_size - qr_x_margin, qr_y_margin, width=qr_size, height=qr_size)
        # add day text
        dayHeight = heightPage - 140
        dayText = f'Dag {p}'
        c.drawString(90, dayHeight, dayText)
        # add graph
        c.drawImage("static/graph.png", 15, -300, 512, preserveAspectRatio=True)
        

    for p in range(1, 15):
        createPage(c, p)
        c.showPage()

    c.save()
    
if __name__ == "__main__":
    createBook("RR.1234")