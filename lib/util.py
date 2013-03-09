import random

def echo(*args, **kwds):
    DEBUG = True
    if DEBUG:
        print(*args, **kwds)

def pick_weighted(L):
    '''
    Randomly picks an integer in {0, 1, ... len(L)-1}, where relative
    probabilities are given by L.
    '''
    assert all(x >= 0 for x in L)

    r = random.uniform(0, sum(L))
    c = 0
    for i, x in enumerate(L):
        c += x
        if c >= r: return i

    raise ValueError

class Vector(list):
    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError

        new = Vector()
        for s, o in zip(self, other):
            new.append(s+o)

        assert len(new) == len(self)
        return new

    def __iadd__(self, other):
        raise NotImplementedError

    def __mul__(self, n):
        new = Vector()
        for s in self:
            new.append(s*n)

        assert len(new) == len(self)
        return new

    __rmul__ = __mul__

    def normalize(self):
        '''
        Modifies vector in-place.
        '''
        T = sum(self)
        for i in range(len(self)):
            self[i] = self[i]/T
