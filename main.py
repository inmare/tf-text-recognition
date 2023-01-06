import qrcode
import binascii
import sys

filename = "phaser.min.zip"
with open(filename, "rb") as f:
    content = f.read()

hex_string = binascii.hexlify(content)

# max_len = 4296
max_len = 2953

data = content[:max_len]
# print(len(text))

qr = qrcode.QRCode(
    version=40,
    error_correction=qrcode.ERROR_CORRECT_L,
    box_size=3,
    border=4,
)

qr.add_data(data)
qr.make()

# img = qr.make_image()
# img.save("test.png")
# img.save("test.png")
