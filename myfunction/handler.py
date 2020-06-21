from PIL import Image
import requests
from io import BytesIO
import json

GATEWAY_URL = "http://35.223.47.36:8080/function/myfunction"

def handle(req):
    response = requests.get(req)
    image = Image.open(BytesIO(response.content))

    width = image.width
    height = image.height

    for y in range(height-1):
        for x in range(width-1):
            pos = (x, y)
            pixel = image.getpixel(pos)
            oldR = pixel[0]
            oldG = pixel[1]
            oldB = pixel[2]

            factor = 1

            newR = int(round(factor * oldR / 255) * (255/factor))
            newG = int(round(factor * oldG / 255) * (255/factor))
            newB = int(round(factor * oldB / 255) * (255/factor))

            errR = oldR - newR
            errG = oldG - newG
            errB = oldB - newB
            
            pixel1 = image.getpixel((x+1, y  ))
            pixel2 = image.getpixel((x-1, y+1))
            pixel3 = image.getpixel((x  , y+1))
            pixel4 = image.getpixel((x+1, y+1))

            pixel1 = tuple(map(operator.add, pixel1, (round(errR * 7/16), round(errG * 7/16), round(errB * 7/16))))
            pixel2 = tuple(map(operator.add, pixel2, (round(errR * 3/16), round(errG * 3/16), round(errB * 3/16))))
            pixel3 = tuple(map(operator.add, pixel3, (round(errR * 5/16), round(errG * 5/16), round(errB * 5/16))))
            pixel4 = tuple(map(operator.add, pixel4, (round(errR * 1/16), round(errG * 1/16), round(errB * 1/16))))


            image.putpixel((x+1, y  ), pixel1)
            image.putpixel((x-1, y+1), pixel2)
            image.putpixel((x  , y+1), pixel3)
            image.putpixel((x+1, y+1), pixel4)
            
    image = image.convert(mode="L")

    image.save("ditheredimg.jpg")
    
    headers = {
    'content-type': "img/jpeg",
    'accept': "application/json"
    }

    files={
        'image':open("ditheredimg.jpg", "rb")
    }
    
    with open("ditheredimg.jpg", "rb") as f:
        r = request("POST", url, headers=headers, files=files)
        with open("ditheredimg.jpg", "wb") as f:
            f.write(r.content)
            
    
    



