import matplotlib.pyplot as plt
import numpy as np

# variable names match following formulae: 
# https://en.wikipedia.org/wiki/JPEG#Discrete_cosine_transform

# wiki g
g = np.matrix([
    [52,55,61,66,70,61,64,73],
    [63,59,55,90,109,85,69,72],
    [62,59,68,113,144,104,66,73],
    [63,58,71,122,154,106,70,69],
    [67,61,68,104,126,88,68,70],
    [79,65,60,70,77,68,58,75],
    [85,71,64,59,55,61,65,83],
    [87,79,69,68,65,76,78,94],
], dtype=np.float)

## my g
#g = np.matrix([
#    [70, 72, 70, 70, 72, 68, 68, 64],
#    [103,101,103,100, 99, 97, 94, 94],
#    [132,132,132,130,129,129,125,121],
#    [157,157,155,154,153,150,148,145],
#    [168,163,164,162,163,161,161,156],
#    [172,170,165,166,163,163,162,158],
#    [174,170,167,167,164,163,164,159],
#    [174,173,170,167,167,166,166,160]
#], dtype=float)

# transpose so wen can index(x,y) 
# TODO: dont forget to transpose back before i.e printing and compare to wiki
g = g.T

# A typical quantization matrix (for a quality of 50% as specified in the original JPEG Standard)
Q = np.matrix([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99],
], dtype=float)

# transpose Q to match indexing of g
Q = Q.T


def alpha(u):
    return 1/np.sqrt(2) if (u == 0) else 1

def dct(g,u,v):
    pre = (1/4) * alpha(u) * alpha(v)
    # terms for all combinations of x and y 
    xy_terms = [g[x,y] * np.cos((2*x+1)*u*np.pi/16) * np.cos((2*y+1)*v*np.pi/16) 
                for x in range(8) for y in range(8)]

    # sum the terms and multiply with the scalar
    return pre * np.sum(xy_terms)


if __name__ == '__main__':

    # normalize at 0 origin for DCT
    g -= 128

    # dct(g) =  G
    G = np.empty_like(g)
    ite = np.nditer(g, flags=['multi_index'])
    # apply dct to every element in g
    for e in ite:
        (u,v) = ite.multi_index
        G[u,v] = dct(g,u,v)

    # quantize
    B = np.around(G/Q)
    print(B.T)
