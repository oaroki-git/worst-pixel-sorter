from PIL import Image
import numpy
import tqdm
import tomllib
import os

def getContrastMap(array, whiteVal, blackVal):
    cmap = numpy.empty(array.shape)
    for row in range(array.shape[0]):
        cmap[row] = numpy.array([1 if x > blackVal and x < whiteVal else 0 for x in array[row]])
    print("contrast map done!")
    return cmap

def getSortMap(cmap):
    global pixels
    smap = numpy.empty(cmap.shape)
    for row in range(cmap.shape[0]):
        col = 0
        index = -1
        while col < cmap.shape[1]:
            if not cmap[row][col]:
                col += 1
                continue
            index = col
            length = 0
            while col < cmap.shape[1] and cmap[row][col]:
                col += 1
                length += 1
            #if length > cmap.shape[1]:
            smap[row][index] = length
            pixels += length
    print("sort map done!")
    return smap

def sortBuffer(pixArr, grsclArr, smap, row, col, progress):
    length = int(smap[row][col])
    if length == 0:
        return pixArr
    buffer = zip(grsclArr[row][col:col+length:], pixArr[row][col:col+length:])
    buffer = list(list(zip(*sorted(buffer, key=lambda x: x[0])))[1])
    pixArr[row][col:col+length:] = buffer
    progress.update(length)
    #print(f"sorted {length} pixels starting from {row}, {col}")
    return pixArr

def mainsort(pixArr, grsclArr, smap, progress):
    for row in range(pixArr.shape[0]):
        for col in range(pixArr.shape[1]):
            pixArr = sortBuffer(pixArr, grsclArr, smap, row, col, progress)
    return pixArr

def sortImage(path, whiteVal, blackVal, savePath = ""):
    global pixels
    image = Image.open(os.path.expanduser(path))
    pixArr = numpy.array(image)
    grsclArr = numpy.array(image.convert("L"))

    cmap = getContrastMap(grsclArr, whiteVal, blackVal)
    smap = getSortMap(cmap)
    print(f"sorting {pixels} pixels..")
    progress = tqdm.tqdm(total=pixels)
    output = mainsort(pixArr, grsclArr, smap, progress)

    newImage = Image.fromarray(output)

    if savePath == "":
        newImage.show()
    else:
        newImage.save(os.path.expanduser(savePath))

def UIprompt():
    path = input("enter path/to/image (no need to escape spaces): ")
    white = int(input("enter white threshold for sorting: "))
    black = int(input("enter black threshold for sorting: "))
    save = input("enter path/to/save the file (not the directory) (press enter if you don't want to save): ")
    
    sortImage(path, white, black, save)

def readConfig():
    with open(os.path.expanduser("~/.config/pixelsort.toml")) as file:
        config = tomllib.loads(file.read())

    path = config["image"]["original_path"]
    save = config["image"]["save_path"]
    white = config["processing"]["white_threshold"]
    black = config["processing"]["black_threshold"]

    sortImage(path, white, black, save)

pixels = 0
readConfig()
