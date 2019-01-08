import numpy as np
import queue
from PIL import Image
import sys
import matplotlib.pyplot as plt
import random


INIT=-1
MASK=-2
WSHED=0
fictious_point = [-5,-5]
def load_image( infilename ) :
    img = Image.open( infilename ).convert('L')
    img.load()
    data = np.asarray( img, dtype=np.uint8)
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray(npdata, 'L')
    img.save( outfilename )

def get_index(x,y, width):
    return x * width + y

def watershed(filename, output):
    current_label = 0
    current_dist = 0
    q = queue.Queue()
    imi = load_image(filename)
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
            for nx in range(p[0]-1,p[0]+1):
                for ny in range(p[1]-1,p[1]+1):
                    if(imo[nx,ny] > 0 or imo[nx,ny] == WSHED):
                        imd[p[0],p[1]] = 1
                        q.put([p[0],p[1]])

        current_dist=1
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

            for nx in range(p[0]-1,p[0]+1):
                for ny in range(p[1]-1,p[1]+1):
                    if(imd[nx,ny] < current_dist and
                            (imo[nx, ny ] > 0 or imo[nx, ny] == WSHED)):
                        if(imo[nx, ny] > 0):
                           if(imo[p[0], p[1]] == MASK or imo[p[0],p[1]] == WSHED) :
                               imo[p[0], p[1]] = imo[nx, ny]
                           elif (imo[p[0], p[1]] != imo[nx, ny]):
                               imo[p[0], p[1]] = WSHED
                        elif (imo[p[0], p[1]] == MASK):
                            imo[p[0], p[1]] = WSHED
                    elif(imo[nx,ny] == MASK and imd[nx,ny] == 0):
                        imd[nx,ny] = current_dist +1
                        q.put([nx,ny])

        for p in index[h]:
            imd[p[0],p[1]] = 0
            if(imo[p[0],p[1]] == MASK):
                current_label = current_label +1
                q.put([p[0], p[1]])
                imo[p[0],p[1]] = current_label
                while not q.empty():
                    p2 = q.get()
                    for nx in range(p2[0] - 1, p2[0] + 1):
                        for ny in range(p2[1] - 1, p2[1] + 1):
                            if(imo[nx, ny] == MASK):
                                q.put([nx,ny])
                                imo[nx,ny] = current_label


    I8 = (((imo - imo.min()) / (imo.max() - imo.min())) * 255).astype(np.uint8)
    save_image(I8, output)

    plt.imshow(imo)
    plt.show()

    return

if __name__ == '__main__':
    watershed(sys.argv[1], sys.argv[2])
