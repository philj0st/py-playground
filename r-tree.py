# multidimensional spatial indexing
# range/similarity/nearest neighbour search required
# height balanced
# non-leaf node holds closed bounded interval for every dimension

# fanout / maximum number of entries in one node / blocking factor
M = 50

# must be at least half of the fanout m >= M/2
m = 25


# every leaf node contains m <= index records <= M. unless it is the root.
# every index record (I,id)'s I spatially contains the n-dim data obj represented by it's id


# non-leaf nodes has m<= entries <=M of (I,ptr), I being the minimum bounding rectangle (MBR) that contains all rectangles in the child node.




# all leafs appear on the same level
# height of the R-Tree is <= ceil(log_m(N)). N being the number of index records.jo

ndim = 2

# multiply all dimensions of the bounding space (rectangle for 2d, box for 3d, ..)
def ndim_space(vec):
    return np.prod(vec, where=vec!=0)

import numpy as np
class RTree(object):
    def __init__(self):
        self.root = None

class Node(object):
    def __init__(self, mbr_lower, mbr_upper, children):
        self.mbr_lower = mbr_lower
        self.mbr_upper = mbr_upper
        self.children = children
        self.indicies = []

    def insert(self, index, value):
        # if currently in a non-leaf node, insert the index in the best fit child node
        if(self.children):
            self.best_fit_child(index).insert(index,value)
#            import pdb
#            pdb.set_trace()

        # once a child node was reached, just add the index
        else:
            self.indicies.append((index,value))

    # returns mbr's size: multiply all dimensions of the bounding space (rectangle for 2d, box for 3d, ..)
    def mbr_size(self):
        vec = self.mbr_upper - self.mbr_lower
        return ndim_space(vec)

    # find the child node that enlarges the least when encompassing the index
    def best_fit_child(self, index):
        # if there's a tie, pick the smallest in size
        best, *_ = sorted(self.children, key=lambda child: (child.new_mbr(index)[2],child.mbr_size))
        return best


    # returns the new minimum bounding rectangle (mbr) after encompassing the given index
    def new_mbr(self, index):
        lower = self.mbr_lower.copy()
        upper = self.mbr_upper.copy()

        # adjust where index is out of bounds (oob)
        lower_oob = (index - lower < 0)
        lower[lower_oob] = index[lower_oob]

        upper_oob = (index - upper > 0)
        upper[upper_oob] = index[upper_oob]

        # new mbr - old one
        # #TODO suboptimal
        enlargement = ndim_space(upper - lower) - self.mbr_size()
        return lower, upper, enlargement

    # check if the mbr of this node encompasses the given index
    def encompasses(self, index):
        lower, upper, _ = self.new_mbr(index)
        return np.array_equal(lower, self.mbr_lower) and np.array_equal(upper, self.mbr_upper)


lower = np.array([0,0])
upper = np.array([100,100])
zero_to_fifty = Node(lower,np.array([50,50]),[])
fifty_to_hundred = Node(np.array([50,50]),upper,[])
n = Node(lower,upper,[zero_to_fifty, fifty_to_hundred])

idx = np.array([33,15])
idx2 = np.array([66,115])
print(n.encompasses(idx))
print(n.new_mbr(idx2))
print(n.mbr_size())
print(zero_to_fifty.mbr_size())
# most fitting subtree for given index
print(sorted(n.children, key=lambda child: child.new_mbr(idx)[2])[0].mbr_lower)
n.insert(idx,'some-id')
n.insert(idx2,'some-id')
