import numpy as np
import queue
from PIL import Image
import sys
import matplotlib.pyplot as plt
from random import randint
from math import sqrt

import random
import scipy
import scipy.misc
import scipy.ndimage


INIT=-1
MASK=-2
WSHED=0
fictious_point = [-5,-5]
def load_image( infilename ) :
    return scipy.misc.imread(infilename, mode="L")

def save_image( npdata, outfilename ) :
    img = Image.fromarray(npdata)
    img.save( outfilename )

def get_index(x,y, width):
    return x * width + y

def conv(image, x, y, filtre):
    sum = 0
    center = len(filtre) // 2
    for i in range(-center,
                   center + 1):
        for j in range(-center, center + 1):
            if filtre[i + center][
                j + center] != 0:
                if 0 <= x + i < image.width and 0 <= y + j < image.height:
                    xl = x + i
                    yl = y + j
                else:
                    xl = x - i
                    yl = y - j

                if not 0 <= xl < image.width or not 0 <= yl < image.height:
                    xl = x
                    yl = y
                sum += (image.getpixel((xl, yl)) * filtre[i + center][j + center])
    return sum


def sobel(file):
    image = Image.open(file).convert('L')
    res = image.copy()
    x_mask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    y_mask = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    for x in range(image.width):
        for y in range(image.height):
            dx = conv(image, x, y, x_mask)
            dy = conv(image, x, y, y_mask)

            val = int(round(sqrt(dx ** 2 + dy ** 2) * 255 / (
                        sqrt(2) * 1020)))
            res.putpixel((x, y), (val))
    return np.array(res)

def get_neighbourhood(tab, x, y):
    n = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x+i >= 0 and (x + i < tab.shape[0]) and (y + j >= 0 and (y + j < tab.shape[1])):
                n.append([x+i, y+j])
    return n

def seuillage(result, step):
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = int(result[i, j]/step) * step
    return result

def watershed(filename, output, seuil):
    current_label = 0
    current_dist = 0
    q = queue.Queue()

    imi = sobel(filename)
    imi = seuillage(imi, seuil)
    imo = np.full(imi.shape, INIT)
    imd = np.full(imi.shape, 0)

    hmin = np.amin(imi)
    hmax = np.amax(imi)


    index = [ [] for elem in range(hmax-hmin+1)]

    for u, v in np.ndindex(imi.shape):
        index[imi[u,v] - hmin].append([u,v])

    for h in range(hmax-hmin+1):
        for p in index[h]:
            imo[p[0],p[1]] = MASK
            # check neighbourhood
            neigh = get_neighbourhood(imi, p[0], p[1])
            for n in neigh:
                if imo[n[0], n[1]] > 0 or imo[n[0], n[1]] == WSHED:
                    imd[p[0], p[1]] = 1
            q.put([p[0], p[1]])
        current_dist = 1
        q.put(fictious_point)

        while True:
            p = q.get()
            if(p == fictious_point):
                if(q.empty()):
                    break
                else:
                    q.put(fictious_point)
                    current_dist = current_dist + 1
                    p = q.get()
            neigh = get_neighbourhood(imi, p[0], p[1])
            for n in neigh:
                if(imd[n[0],n[1]] < current_dist and
                        (imo[n[0], n[1] ] > 0 or imo[n[0], n[1]] == WSHED)):
                    if(imo[n[0], n[1]] > 0):
                       if(imo[p[0], p[1]] == MASK or imo[p[0],p[1]] == WSHED) :
                           imo[p[0], p[1]] = imo[n[0], n[1]]
                       elif (imo[p[0], p[1]] != imo[n[0], n[1]]):
                           imo[p[0], p[1]] = WSHED
                    elif (imo[p[0], p[1]] == MASK):
                        imo[p[0], p[1]] = WSHED
                elif(imo[n[0],n[1]] == MASK and imd[n[0],n[1]] == 0):
                    imd[n[0],n[1]] = current_dist +1
                    q.put([n[0],n[1]])

        for p in index[h]:
            imd[p[0],p[1]] = 0
            if(imo[p[0],p[1]] == MASK):
                current_label = current_label + 1
                q.put([p[0], p[1]])
                imo[p[0],p[1]] = current_label
                while not q.empty():
                    p2 = q.get()
                    neigh = get_neighbourhood(imi, p2[0], p2[1])
                    for nb in neigh:
                        if imo[nb[0], nb[1]] == MASK:
                            q.put(nb)
                            imo[nb[0], nb[1]] = current_label

    fusion = np.array(imo)
    for i in range(imo.shape[0]):
        for j in range(imo.shape[1]):
            value = imo[i, j]
            if value == WSHED:
                neighbors = get_neighbourhood(imo, i, j)
                for n in neighbors:
                    v = imo[n[0], n[1]]
                    if v != WSHED:
                        fusion[i, j] = v
                        break

    segmentation = Image.new('RGB', (imo.shape[1], imo.shape[0]))
    colors = [0]*(current_label + 1)
    for c in range(len(colors)):
        colors[c] = (randint(100, 200), randint(100, 200), randint(100, 200))

    for i in range(imo.shape[1]):
        for j in range(imo.shape[0]):
            if imo[j][i] == WSHED:
                segmentation.putpixel((i, j), (0,0,0))
            else:
                segmentation.putpixel((i, j), colors[imo[j][i]])


    split = np.array(fusion)

    for i in range(split.shape[0]):
        for j in range(split.shape[1]):
            neighbors = get_neighbourhood(fusion, i, j)
            for n in neighbors:
                if fusion[i,j] < fusion[n[0], n[1]]:
                    split[i,j] = WSHED
                    break

    save_image(imi, "gradient-" + output)
    segmentation.save("segmentation-" + output)
    scipy.misc.imsave("merge-" + output, fusion)
    scipy.misc.imsave("separation-" + output, split)


    return

if __name__ == '__main__':
    watershed(sys.argv[1], sys.argv[2], int(sys.argv[3]))
