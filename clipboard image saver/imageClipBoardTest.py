from PIL import ImageGrab, Image
import os

#testing the ImageGrap functionality, also my first git usage !

img = ImageGrab.grabclipboard() #if the last thing you copied is an image, it returns a PIL of the image
#if it's directories, it returns a list of the paths in string format.
print(img)

print(type(img))

print(img.size)