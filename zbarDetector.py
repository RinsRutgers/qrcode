from PIL import Image, ImageDraw
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode


image = Image.open('scan/jpg/Scan-rins_rutgers-0532_006.jpg')
draw = ImageDraw.Draw(image)
for barcode in decode(image,  symbols=[ZBarSymbol.QRCODE]):
    print(barcode)
    rect = barcode.rect
    draw.rectangle(
        (
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top + rect.height)
        ),
        outline='#0080ff'
    )

    draw.polygon(barcode.polygon, outline='#e945ff')


image.save('bounding_box_and_polygon.png')