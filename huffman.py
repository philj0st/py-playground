from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from dct import DCT, Q
import operator

im = Image.open("./lenargb.jpg")
print(im.format, im.size, im.mode)

ycbcr = im.convert('YCbCr')
print(ycbcr.format, ycbcr.size, ycbcr.mode)


# split the image into individual bands
(R, G, B) = im.split()
(Y, Cb, Cr) = ycbcr.split()

# translate indexing from (512,512) -> (64, 64)@(8,8)
#┌───────64x64...
#│┌┐┌┐─8x8
#│└┘└┘─[1,0]
#│┌┐─[0,1]
#.└┘
def index64(M,x,y):
    return M[(x*8):(x*8)+8,(y*8):(y*8)+8]

Ya = np.matrix(Y, dtype=float)
Ya -= 128
print(index64(Ya,0,0))

Yc = DCT(index64(Ya,0,0))
Yc = np.around(Yc/Q)

print(Yc)

DCs = []
# get all DC components
for x in range(64):
    for y in range(64):

        # get coefficients
        Yc = DCT(index64(Ya,x,y))

        # quantize
        Yc = np.around(Yc/Q)

        DCs += [Yc[0,0]]

print(DCs[:10])

# entropy encode the quantized coefficients

# calculate difference in DC components
deltas = list(map(operator.sub, DCs[1:], DCs[:-1]))
print(deltas[:10])

# delta = difference between current and previous block

# deltaDC equals original DC value because there's no previous block


## Huffman code
# category  values          bits
# 1         -1,1            0,1
# 2         -3,-2,2,3       00,01,10,11
# 3         -15..-8,8..15   000,001,010,011,100,101,110,111
# ...

# concat category codeword and member index
