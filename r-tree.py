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

class Node(object):
    def __init__(self, index_ranges, children):
        self.index_ranges = index_ranges
        self.children = children

    def split():
        return

    # return the enlargement needed in each dimension of the MBR if this node was to encompass the given index
    def enlargement(self, index):
        import pdb
        pdb.set_trace()
        dims = []
        for idx, (dim_min, dim_max) in enumerate(self.index_ranges):
            if index[idx] < dim_min:
                dims.append(dim_min - index[idx])
            elif dim_max < index[idx]:
                dims.append(index[idx] - dim_max)
            else:
                dims.append(0)
        return dims

    # check if the mbr of this node encompasses the given index
    def contains(self, index):
        for idx, (dim_min, dim_max) in enumerate(self.index_ranges):
            if index[idx] < dim_min or dim_max < index[idx]:
                return False
        return True


n = Node([(22,55),(11,18),(44,88)],[])
print(n.contains([33, 15, 66]))
print(n.enlargement([11, 5, 66]))
