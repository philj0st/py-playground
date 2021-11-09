from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from dct import DCT, Q
import operator

im = Image.open("./lenargb.jpg")
ycbcr = im.convert('YCbCr')


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

Ya = np.matrix(Cb, dtype=float)
Ya -= 128

print("* performing DCT on", im.format, im.size, im.mode)

DCs = []
# get all DC components
for x in range(64):
    for y in range(64):

        # get coefficients
        Yc = DCT(index64(Ya,x,y))

        # quantize
        Yc = np.around(Yc/Q)

        DCs += [Yc[0,0]]

print("first 10 DC Components")
print(DCs[:10])


# delta = difference between current and previous DC component
deltas = list(map(operator.sub, DCs[1:], DCs[:-1]))
# prepend first DC value because there's no previous block

deltas = [DCs[0]]+deltas
print("first 10 deltas of DC Components")
print(deltas[:10])

# generate Huffman codebook to encode theese deltas
# nonprefix property: code cannot be part of another code -> uniquely decodable
uniq = set(deltas)
freq = {}

# init all deltas as keys to a dict with another dict as value
while len(uniq):
    freq[uniq.pop()] = 0

# count their occurances
for delta in deltas:
    freq[delta] +=1

# get tuples for all symbols and their occurance count
tupes = sorted(list(freq.items()), key=lambda el: el[1])


class Node(object):
    def __init__(self, weight, symbol=None):
        self.weight = weight
        self.symbol = symbol
        self.left = None
        self.right = None


# instantiate nodes for all tuples
remaining = [Node(occ,sym) for (sym,occ) in tupes]

while len(remaining)>2:
    remaining = sorted(remaining, key=lambda node: node.weight)

    # take two least frequent ones
    [left, right, *rest] = remaining

    # create a new node connecting the two adding their weights
    new = Node(left.weight+right.weight)
    new.left = left
    new.right = right

    # add the node back to remaining
    remaining = [new]+rest

# create final root
[left, right] = remaining
root = Node(left.weight+right.weight)
root.left = left
root.right = right

# create huffman code while traversing
def traverse(node, code):
    # process left sub tree
    if node.left:
        for leaf in traverse(node.left, code+"0"):
            yield leaf

    # process myself in case i'm a leaf
    if (not isinstance(node.left, Node)) and (not isinstance(node.right, Node)):
        yield (node.symbol, code)

    # process right sub tree
    if node.right:
        for leaf in traverse(node.right, code+"1"):
            yield leaf

codebook = list(traverse(root,""))
print("*******CODEBOOK******************")
print(sorted(codebook,key=lambda x:len(x[1])))

print("\nBitstring for entropy encoded deltaDCs:")
# create dict from codebook
encode = {}
for (symbol, code) in codebook:
    encode[symbol]=code

encodedDeltas = list(map(lambda d: encode[d], deltas))
print("".join(encodedDeltas))



# entropy encode the deltas
## Huffman code
# category  values          bits
# 1         -1,1            0,1
# 2         -3,-2,2,3       00,01,10,11
# 3         -15..-8,8..15   000,001,010,011,100,101,110,111
# ...



# concat category codeword and member index

# Huffman Table marker 2B
DHT = 0xFFC4

# block length except for the marker 2B so remaining are Lh-2 bytes
Lh = 0
# table class. 0 -> DC table 0.5B
Tc = 0x0
# table number. 0 for luminance / 1 for chrominance  0.5B
Tc = 0x0

# L<i> = #codes with len=i
Li = []

# theese Huffman tables will be wrapped in Segments and Frames and are part of the .jpeg file
