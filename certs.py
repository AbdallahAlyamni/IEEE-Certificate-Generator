#Imports Required Packages from PIL
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO

#Import Pandas for better access of Data and .xlsx File
import pandas as pd

#Import the file that contains all the details
# data = pd.read_excel("file.xlsx")
# name_list = data['Name'].to_list()
#cert_type_list = data['type'].to_list()
#cert_text_list = data['text'].to_list()
#cert_date_list = data['date'].to_list()

#Determining the length of the list

class Generate():

    def startGeneration(test, name_list, cert_template, cert_type, cert_date, cert_txt, cert_txt_optional):
        # data = pd.read_excel("file.xlsx")
        # name_list = ["Hmam Abdalbagi Osman Taliballa"]
        max_no = len(name_list)+1
        imlist = []

        for i in range(max_no-1):
            im = Image.open(cert_template)
            d = ImageDraw.Draw(im)
            #name style
            name_location = (193, 690)
            text_color = (0, 102, 163)
            font = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 105, encoding="unic")
            d.text(name_location, name_list[i].title(), fill=text_color,font=font)
            #certficate type style
            cert_type_location = (1448,366)
            text_color = (219, 219, 219)
            font = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 86, encoding="unic")
            d.text(cert_type_location, cert_type, fill=text_color,font=font)
            #certficate text style
            cert_text_location = (288,807)
            text_color = (119, 119, 119)
            font = ImageFont.truetype("fonts/LexendDeca-Regular.ttf", 70, encoding="unic")
            font2 = ImageFont.truetype("fonts/LexendDeca-Regular.ttf", 50, encoding="unic")
            d.multiline_text(cert_text_location, cert_txt, fill=text_color,font=font)
            d.multiline_text((288,1120), cert_txt_optional, fill=text_color,font=font2)
            date_location = (346,1552)
            text_color = (0, 102, 163)
            font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 66, encoding="unic")
            d.text(date_location, cert_date, fill=text_color,font=font)
            im2 = Image.open('stamp/STAMP-01.png')
            im2 = im2.resize((444,444))
            im.paste(im2, (2364,1000), mask=im2)
            im3 = Image.open('stamp/signature2.png')
            im.paste(im3, (2337,1437), mask=im3)
            imlist.append(im)
        return imlist
        
    
    # print("""\n*************************
    # All Certificates Created! \nPlease follow me on Github for more awesome codes\n\tGitHub: https://github.com/mursalfk
    # *************************
    # """)
    #Read readme.md for further instructions
