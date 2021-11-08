from PIL import Image

im = Image.open("./lenargb.jpg")
print(im.format, im.size, im.mode)

ycbcr = im.convert('YCbCr')
print(ycbcr.format, ycbcr.size, ycbcr.mode)


# split the image into individual bands
(R, G, B) = im.split()
(Y, Cb, Cr) = ycbcr.split()

# entropy encode the quantized coefficients

# apply run length encoding

# store quant. coeffs. in zig-zag pattern

# store difference in DC parts

# delta = difference between current and previous block

# deltaDC equals original DC value because there's no previous block


## Huffman code
# category  values          bits
# 1         -1,1            0,1
# 2         -3,-2,2,3       00,01,10,11
# 3         -15..-8,8..15   000,001,010,011,100,101,110,111
# ...

# concat category codeword and member index
