from reportlab.graphics.barcode import qr
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
        for qr_number in range(0,4):
            qrText = f"{uuid}.{p}.{qr_number}"
            qr_code = qr.QrCodeWidget(qrText, barLevel = 'H', width=240, height=240)
            bounds = qr_code.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            d[qr_number] = Drawing(300, 300)
            d[qr_number].add(qr_code)
            qr_placement_x = widthPage - width
            qr_placement_y = heightPage - height
        dayHeight = heightPage - 80
        dayText = f'Dag {p}'
        c.drawString(90, dayHeight, dayText)
        renderPDF.draw(d[2], c, 0, 0)
        renderPDF.draw(d[1], c, qr_placement_x, qr_placement_y)
        renderPDF.draw(d[0], c, 0, qr_placement_y)
        renderPDF.draw(d[3], c, qr_placement_x, 0)
        c.drawImage("static/graph.png", 15, -500, 550, preserveAspectRatio=True)
        
    
    for p in range(1, 15):
        createPage(c, p)
        c.showPage()

    c.save()
    
if __name__ == "__main__":
    createBook("RR.4637")