import requests
from PIL import Image
import streamlit as st

def img_requests(txt):
    response = requests.get("https://source.unsplash.com/random/600*300/?{0}".format(txt))
    file = open('image.jpg', 'wb')
    file.write(response.content)
    img = Image.open(r"image.jpg")
    img.show()
    file.close()
    return file.name, img.size[0], img.size[1]


unspl_access_key = st.secrets['unspl_access_key']

from pyunsplash import PyUnsplash

def new_requests(target):
    pu = PyUnsplash(api_key=unspl_access_key)

    photos = pu.photos(type_='random', count=1, featured=True, query=target)
    [photo] = photos.entries
    # print(photo)
    print(photo.id, photo.link_download)
    return photo.link_download
    


if __name__ == "__main__":
    # img = img_requests("sky")
    # print(img[0], img[1], img[2])
    
    new_requests()