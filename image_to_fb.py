import os
import base64
import pyrebase
from PIL import Image
from io import BytesIO

config = {
    "apiKey": "AIzaSyAhaOe24nDVf_6PRgjfffu1PwQss2QI3I4",
    "authDomain": "fishbowl-c47d5.firebaseapp.com",
    "databaseURL": "https://fishbowl-c47d5.firebaseio.com",
    "projectId": "fishbowl-c47d5",
    "storageBucket": "fishbowl-c47d5.appspot.com",
    "messagingSenderId": "230121294113",
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

ENCODING = "utf-8"

# https://stackoverflow.com/a/13957446
# i guess our snapshots are small (< 10Mb) so i only implemented the base64 version
def store_image_to_fb():
    store_base64_image()


def store_base64_image():
    print("store base64 image")
    dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, "./fish2.jpeg")
    # filename = os.path.join(dirname, "./fish3.jpeg")
    filename = os.path.join(dirname, "./fish.png")
    try:
        image = Image.open(filename)
        # image.show()
        rgb_im = image.convert("RGB")
        img_buffer = BytesIO()
        rgb_im.save(img_buffer, format="JPEG")
        img_bytes = base64.b64encode(img_buffer.getvalue())
        base64_string = img_bytes.decode(ENCODING)
        # print(img_str)

        new_img_ref = database.child("images").push({"id": "", "data": ""})
        id = new_img_ref["name"]
        # print(id)
        database.child("images").child(id).update({"id": id, "data": base64_string})

    except Exception as e:
        print(str(e))

    # open and encode image as base64 string
    # push to firebase realtime database


def store_binary_image():
    print("store binary image")
    # push a json to realtime database and get id
    # update the json with value equal to the new id
    # open an image
    # save the image to storage with the name equal to id


if __name__ == "__main__":
    store_image_to_fb()
