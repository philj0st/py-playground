import numpy as np

M = np.arange(512*512).reshape((512,512)).T

s = M[0:8,0:8]

#┌───────64x64...
#│┌┐┌┐─8x8
#│└┘└┘─[1,0]
#│┌┐─[0,1]
#.└┘
def index64(M,x,y):
    return M[(x*8):(x*8)+8,(y*8):(y*8)+8]

print(s)
print(index64(M,0,0))
print(index64(M,1,0))

# last 8x8 block top right corner
print(index64(M,63,0))
