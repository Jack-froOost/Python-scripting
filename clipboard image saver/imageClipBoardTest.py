from PIL import ImageGrab, Image
from datetime import datetime
import os
import time

from io import BytesIO
import hashlib

SAVE_DIR        = r"C:\Users\mhnd0\OneDrive\Desktop\temp"
TTL             = 24 * 60 * 60  #delete files that are more than 24 hours
HOW_OFTEN_CHECK = 1             #check if a new image arrived every one second

os.makedirs(SAVE_DIR, exist_ok=True)
lastCleanup= 0
lastHash   = None #store hash of last image to not save the same image twice.
#honestly this is the fastest way i could find to compare to PIL images

#run every 5 minutes, delete all files older than TTL
def clean_files(dir: str, ttl):
    for file in os.listdir(dir):
        p = os.path.join(dir, file)
        if os.path.getmtime(p) < (time.time()-ttl):
            try: #file could be removed or re-located while in this loop
                os.remove(p)
            except Exception as e:
                print(f"couldn't delete {p}, {e}")

def image_to_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()



while True:
    img = ImageGrab.grabclipboard() 
    if isinstance(img, Image.Image):
        byte = image_to_bytes(img)
        hsh  = hashlib.sha256(byte).hexdigest() #return a fixed size hashed value in hexadecimal of img
        if hsh != lastHash:
            ts = datetime.now().strftime("%H;%M  %Ss")
            out = f"image-{ts}.png"
            out_path = os.path.join(SAVE_DIR, out)
            img.save(out_path, "PNG")
            print(f"Saved {out}")
            
            lastHash = hsh
    else:
        print("No image found in clipboard.")
    
    #every 5 minutes, we check the images folder to clean.
    now = time.time()
    for file in os.listdir(SAVE_DIR):
        if now - lastCleanup < 60*5:
            clean_files()
            lastCleanup = now

    time.sleep(1)

