
from glob import glob

def buscarImg(palabra):
    img = glob('*/*')
    for elem in img:
        try:
            ext=(elem.split("/")[1]).split(".")[1]
            if(ext=="png" or ext=="jpg" or ext=="gif" or ext=="jpeg" or ext=="eps"):
                if palabra in elem.split("/")[1]:
                    print(elem.split("/")[1])
                if not linea:
                    break
        except:
            pass

buscarImg("avatar")
