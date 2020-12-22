# Download Unsplash image of a certain category and sets it as Windows wallpaper
## Improved upon based on https://gist.github.com/jdah/d3d7a4ec4b12bdf74bdd0de4bc12a2e2

from functools import reduce
import ctypes, os, winreg, sys
from numpy.random import randint
import requests # to get image from the web
import shutil # to save it locally

from PIL import Image


# >>>> CONFIGURATION VARIABLES <<<<
MONITOR_COUNT = 1
MONITOR_SIZE = '1920x1080'

SPI_SETDESKWALLPAPER    = 0x0014
SPI_SETDESKPATTERN      = 0x0015
SPIF_UPDATEINIFILE      = 0x01
SPIF_SENDWININICHANGE   = 0x02

# Map of wallpaper filenames to the number of times that they have been used
wallpapers = {}

# Next wallpaper in the sequence to be changed
next_change = 0

# Names of the current wallpapers
current_wallpapers = [None] * MONITOR_COUNT

def set_wallpaper(path):
    # Load all images
    images= [Image.open(path).resize(MONITOR_SIZE, Image.BILINEAR)]

    
    for k, v in {("TileWallpaper", "1"), ("WallpaperStyle", "0")}:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_WOW64_32KEY | winreg.KEY_WRITE)
        winreg.SetValueEx(key, k, 0, winreg.REG_SZ, v)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(path), SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE)

def get_unsplash(keyword="nature"):
    ## Set up the image URL and filename
    image_url = f"https://source.unsplash.com/{MONITOR_SIZE}/?{keyword}"
    foldername = keyword # Change path 
    filename = f'{foldername}/{randint(0,100)}.jpg'
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')
    
    return filename

if __name__ == "__main__":
    try:
        print(f'Wallpaper Category : {sys.argv[1]}')
        wallpaper = get_unsplash(sys.argv[1])
    except:
        print('Wallpaper Category : Cat')
        wallpaper = get_unsplash()
    set_wallpaper(wallpaper)