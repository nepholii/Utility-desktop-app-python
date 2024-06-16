# Importing library
import qrcode

def qrgenerator(data="no data"):
 
    # Encoding data using make() function
    img = qrcode.make(data)
 
    # Saving as an image file
    img.save('MyQRCode1.png')


