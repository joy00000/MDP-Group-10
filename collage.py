from PIL import Image
import os

def makeCollage():
    path = "C:/Users/user/Desktop/IRS/receivedimg/"
    i,j=0,0
    collage = Image.new('RGB',(3*240, 3*240), (250,250,250))
    files = os.listdir(path)
    for f in files:
        if f == None:
            continue
        else:
            if(i == 3):
                i = 0
                j+=1
            im = Image.open(path + f)
            im = im.resize((240, 240)) 
            collage.paste(im,(i*im.size[0],j*im.size[0]))
            i+=1

    collage.save("collage.jpg","JPEG")
    collage.show()