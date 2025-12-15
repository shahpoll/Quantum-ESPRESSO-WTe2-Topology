import qrcode # You might need: pip install qrcode[pil]
import matplotlib.pyplot as plt

# Your actual repo URL
url = "https://github.com/shahpoll/Quantum-ESPRESSO-WTe2-Topology"

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("Fig_Repo_QR.png")
print(f"QR Code generated for {url}")
