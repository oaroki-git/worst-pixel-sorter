from PIL import Image
import numpy
import tqdm
import tomllib
import os
from multiprocessing import Pool

def getContrastMap(array, whiteVal, blackVal):
    cmap = numpy.empty(array.shape)
    for row in range(array.shape[0]):
        cmap[row] = numpy.array([1 if x > blackVal and x < whiteVal else 0 for x in array[row]])
    print("contrast map done!")
    return cmap

def getSortMap(cmap):
    pixels = 0
    smap = []
    for row in range(cmap.shape[0]):
        col = 0
        index = -1
        while col < cmap.shape[1]:
            if not cmap[row][col]:
                col += 1
                continue
            colPeg = col
            length = 0
            while col < cmap.shape[1] and cmap[row][col]:
                col += 1
                length += 1
            smap.append((row, colPeg, length,))
            pixels += length
    print("sort map done!")
    return (numpy.array(smap), pixels)

def sortBuffer(pixArr, grsclArr, bufferInfo):
    row = bufferInfo[0]
    col = bufferInfo[1]
    length = bufferInfo[2]
    zipBuffer = zip(grsclArr[row][col:col+length:], pixArr[row][col:col+length:])
    sortedBuffer = list(list(zip(*sorted(zipBuffer, key=lambda x: x[0])))[1])
    return (row, col, sortedBuffer)
    #print(f"sorted {length} pixels starting from {row}, {col}")
    #return pixArr



def getWrapper(pixArr, grsclArr):
    """ legacy code
    for buffer in smap:
        row, col, sortedBuffer = sortBuffer(pixArr, grsclArr, buffer, progress)
        pixArr[row][col:col+len(sortedBuffer):] = sortedBuffer
        progress.update(len(sortedBuffer))
    """
    global wrapper
    def wrapper(bufferInfo):
        return sortBuffer(pixArr, grsclArr, bufferInfo)

def sortImage(path, whiteVal, blackVal, savePath = ""):
    image = Image.open(os.path.expanduser(path))
    pixArr = numpy.array(image)
    grsclArr = numpy.array(image.convert("L"))

    cmap = getContrastMap(grsclArr, whiteVal, blackVal)
    smap, pixels = getSortMap(cmap)
    progress = tqdm.tqdm(total=pixels)

    print(f"sorting {pixels} pixels..")
    getWrapper(pixArrm grsclArr)
    with Pool() as pool:
        global wrapper
        results = [pool.map(wrapper, smap)]
    
    for buffer in results:
        pixArr[row][col:col+len(sortedBuffer):] = sortedBuffer
        progress.update(len(sortedBuffer))

    newImage = Image.fromarray(pixArr)

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

if __name__ == "__main__":
    readConfig()
