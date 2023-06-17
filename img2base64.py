import base64

with open("test.jpg", "rb") as image_file:
    print(base64.b64encode(image_file.read()).decode())