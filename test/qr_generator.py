import qrcode


img = qrcode.make('4442365621388')
type(img)  # qrcode.image.pil.PilImage
img.save("4442365621388.jpg")
# img.save("4442365621388.svg")