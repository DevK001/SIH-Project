from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import img2pdf
import os


df = pd.read_csv('AnalysisReport.csv')
font = ImageFont.truetype('FRAMDCN.TTF', 25)

for index, j in df.iterrows():
    img = Image.open('AnalysisReport.jpg')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(210, 355), text='{}'.format(j['college']), fill=(0, 0, 0), font=font)
    draw.text(xy=(615, 515), text='{}'.format(j['compare']), fill=(0, 0, 0), font=font)
    img.save('Report Photos/{}.PNG'.format('FinalReport'))
    # img.save('Report Photos/{}.PNG'.format(j['reportname']))


# storing image path
img_path = "D:/hackathon/FinalReport/Report Photos/FinalReport.PNG"

# storing pdf path
pdf_path = "D:/hackathon/FinalReport/Final Pdf/FinalReport.pdf"

# opening image
image = Image.open(img_path)

# converting into chunks using img2pdf
pdf_bytes = img2pdf.convert(image.filename)

# opening or creating pdf file
file = open(pdf_path, "wb")

# writing pdf files with chunks
file.write(pdf_bytes)

# closing image file
image.close()

# closing pdf file
file.close()
