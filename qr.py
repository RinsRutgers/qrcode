import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('RR.2637.1.2')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")