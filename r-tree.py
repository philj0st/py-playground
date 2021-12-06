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

import numpy as np
class RTree(object):
    def __init__(self):
        self.root = None

class Node(object):
    def __init__(self, mbr_lower, mbr_upper, children):
        self.mbr_lower = mbr_lower
        self.mbr_upper = mbr_upper
        self.children = children

    def split():
        return

    # returns the new mbr after encompassing the given index
    def new_mbr(self, index):
        lower = self.mbr_lower.copy()
        upper = self.mbr_upper.copy()

        # adjust where index is out of bounds (oob)
        lower_oob = (index - lower < 0)
        lower[lower_oob] = index[lower_oob]

        upper_oob = (index - upper > 0)
        upper[upper_oob] = index[upper_oob]

#        import pdb
#        pdb.set_trace()
        return lower, upper

    # check if the mbr of this node encompasses the given index
    def contains(self, index):
        for idx, (dim_min, dim_max) in enumerate(self.index_ranges):
            if index[idx] < dim_min or dim_max < index[idx]:
                return False
        return True

lower = np.array([0,0])
upper = np.array([100,100])
n = Node(lower,upper,[])

idx = np.array([33,15])
idx2 = np.array([11,15])
print(n.new_mbr(idx))
print(n.new_mbr(idx2))
