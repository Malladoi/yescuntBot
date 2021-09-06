from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

degree_sign = u'\N{DEGREE SIGN}'


def createCurrWeatherImg(icon, scale, dt, city, temp, description, feelslike, humidity):
    fd = requests.get("https://openweathermap.org/img/wn/{0}@{1}x.png".format(icon, scale))
    reqRobotoRegular = requests.get(
        "https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true")
    datefont = ImageFont.truetype(font=BytesIO(reqRobotoRegular.content), size=10 * scale)
    citynamefont = ImageFont.truetype(font=BytesIO(reqRobotoRegular.content), size=30 * scale)
    tempfont = ImageFont.truetype(font=BytesIO(reqRobotoRegular.content), size=35 * scale)
    descrfont = ImageFont.truetype(font=BytesIO(reqRobotoRegular.content), size=15 * scale)
    weathericon = BytesIO(fd.content)
    pb_logo = Image.open(weathericon)
    im = Image.new(mode='RGBA', size=(300 * scale, 170 * scale), color='white')
    pb_logo = pb_logo.convert("RGBA")
    im.paste(pb_logo, (0 * scale, 60 * scale), pb_logo)
    d = ImageDraw.Draw(im)
    d.text(xy=(10 * scale, 5 * scale), text=dt, font=datefont, fill=(235, 110, 75))
    d.text(xy=(10 * scale, 15 * scale), text=city, font=citynamefont, fill=(72, 72, 74))
    d.text(xy=(45 * scale, 60 * scale), text="{0} C{1}".format(temp, degree_sign), font=tempfont, fill=(72, 72, 74))
    d.text(xy=(10 * scale, 100 * scale),
           text="{0}\nощущается как {1} C{2}\nвлажность {3}%".format(description, feelslike, degree_sign, humidity),
           font=descrfont, fill=(72, 72, 74))
    return im
