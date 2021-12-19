import numpy as np
import pdb

M=50
ndim = 2
# rectangle R in Euclidean space E(n) of dim n defined by the 2 endpoints S and T of its major diagonal

s = np.random.randint(101, size=(M, ndim))
t = np.random.randint(101, size=(M, ndim))

# where S[i] < T[i] for all i
S = np.minimum(s,t)
T = np.maximum(s,t)

# MINDIST(P,R) between point P and rectangle  R = (S,T)
def MINDIST(p,s,t):
    r = np.maximum(s,p)
    r = np.minimum(t,r)
    pdb.set_trace()
    return np.sum(np.square(p - r), axis=1)

ss = S[:3]
tt = T[:3]
pp = s[-3:]

P = np.random.randint(101, size=(M, ndim))

lengths = MINDIST(P,S,T)



# upper bound MINMAXDIST to any object inside a MBR
def MINMAXDIST(p,s,t):
    # ( p_i - rm_i )**2
    # where rm_i = s_i if p_i <= (s_i+t_i)/2  ..  t_i otherwise
    ref = (s+t)/2
    return ref

mmd = MINMAXDIST(P,S,T)
