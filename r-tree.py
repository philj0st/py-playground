import numpy as np
import pdb
import random as rnd

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

# multiply all dimensions of the bounding space (area for 2d, volume for 3d, ..) to receive a notion of size
def ndim_space(mbr_lower, mbr_upper):
    vec = mbr_upper - mbr_lower
    return np.prod(vec, where=(vec!=0))

# get a mbr for two points
def mbr_points(pointx, pointy):
    lower = np.minimum(pointx, pointy)
    upper = np.maximum(pointx, pointy)
    return lower, upper

# pick a seed pair from the M+1 entries that when paired make for the biggest mbr
def split_points_quadratic(points):
    remaining = points.copy()
    # cartesian product of points without duplicates
    pairs = [(one,other) for one in remaining for other in remaining if one is not other]

    #  sort by the size of the their mbr
    furthest_apart = sorted(pairs, key=lambda pair: ndim_space(*mbr_points(*pair)), reverse=True)
    (seedl, seedr), *_ = furthest_apart
    # delete the two seeds
    pdb.set_trace()
    remaining.remove(seedl)
    remaining.remove(seedr)

    # recalculate the mbr for every remaining point not assigned to a seed group
    # pick the one with the biggest difference in mbrs to the two seed groups

    return seedl, seedr


one = np.array([0,0])
two = np.array([100,100])
indicies = [np.array([rnd.randint(0,100),rnd.randint(0,100)]) for _ in range(51)] + [one, two]
seedl, seedr = split_points_quadratic(indicies)

# pdb.set_trace()


#def split_ranges():

class RTree(object):
    def __init__(self):
        self.root = None

class Node(object):
    def __init__(self, mbr_lower, mbr_upper, children):
        self.mbr_lower = mbr_lower
        self.mbr_upper = mbr_upper
        self.children = children
        self.indicies = []
        self.parent = None

    def insert(self, index, value):
        # if currently in a non-leaf node, insert the index in the best fit child node
        if(self.children):
            self.best_fit_child(index).insert(index,value)

        # once a child node was reached, add the index
        else:
            self.indicies.append((index,value))
            # and split the node if it's overflowing
            if(M < len(self.indicies)):
                self.split()

#    # quadratic
#    def split():
#        # if the root node is being split, create a new root and attach n and n' as children
#        if(not self.parent):
#           left, rigth = self. 



    # returns mbr's size: multiply all dimensions of the bounding space (rectangle for 2d, box for 3d, ..)
    def mbr_size(self):
        return ndim_space(self.mbr_lower, self.mbr_upper)

    # find the child node that enlarges the least when encompassing the index
    def best_fit_child(self, index):
        # if there's a tie, pick the smallest in size
        best, *_ = sorted(self.children, key=lambda child: (child.new_mbr(index)[2],child.mbr_size()))
        return best


    # returns the new minimum bounding rectangle (mbr) after encompassing the given index
    def new_mbr(self, index):
        lower = self.mbr_lower.copy()
        upper = self.mbr_upper.copy()

        #TODO refactor np.minimum/maximum?
        # adjust where index is out of bounds (oob)
        lower_oob = (index - lower < 0)
        lower[lower_oob] = index[lower_oob]

        upper_oob = (index - upper > 0)
        upper[upper_oob] = index[upper_oob]

        # new mbr - old one
        enlargement = ndim_space(lower,upper) - self.mbr_size()
        return lower, upper, enlargement

    # check if the mbr of this node encompasses the given index
    def encompasses(self, index):
        _, _, enlargement = self.new_mbr(index)
        return not enlargement


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
