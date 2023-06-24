import requests
from PIL import Image

def img_requests(txt):
    response = requests.get("https://source.unsplash.com/random/600*300/?{0}".format(txt))
    file = open('image.jpg', 'wb')
    file.write(response.content)
    img = Image.open(r"image.jpg")
    # img.show()
    # file.close()
    return file.name, img.size[0], img.size[1]

if __name__ == "__main__":
    img = img_requests("nature")
    print(img[0], img[1], img[2])