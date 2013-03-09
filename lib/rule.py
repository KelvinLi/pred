# Rules can figure out their performance by looking at the game history,
# computing their own weight functions at past points in time, and
# comparing their "predictions" to the givens.

# The `get_weights` methods must produce:
#    (1) the same result upon consecutive calls
#    (2) normalized and non-negative weights

from .util import Vector

class RuleBase:
    def __init__(self, game):
        self._game = game
        self.value = None

    def get_weights(self):
        # should be implemented by the derived classes
        raise NotImplementedError

class RuleNull(RuleBase):
    def get_weights(self):
        s = self._game.space_size
        weights = Vector(s * [1.0/s])
        return weights

class RuleContrarian(RuleBase):
    def get_weights(self):
        s = self._game.space_size
        h = self._game.history
        weights = Vector(s * [1.0])
        for i, (hg, hp) in enumerate(h[-10:]):
            weights = (i+10)/10 * weights
            weights[hg] = (10-i)/10 * weights[hg]

        weights.normalize()
        return weights

class RuleMomentum(RuleBase):
    def get_weights(self):
        s = self._game.space_size
        h = self._game.history
        weights = Vector(s * [1.0])
        for i, (hg, hp) in enumerate(h[-10:]):
            weights[hg] += i

        weights.normalize()
        return weights

class RuleRepetition(RuleBase):
    def find_reps(self, seq, sub):
        '''
        Important: Even if the tail of seq is equal to sub,
                   it will be ignored!
        '''
        for i in range(len(seq)-len(sub)):
            if seq[i:i+len(sub)] == sub:
                yield i

    def get_weights(self):
        s = self._game.space_size
        h = self._game.history
        weights = Vector(s * [1.0])
        if len(h) > 0:
            hg = tuple(zip(*h))[0];
            for size in range(1, len(hg)):
                reps = self.find_reps(hg, hg[-size:])
                for i in reps:
                    weights[hg[i+size]] += size**2

        weights.normalize()
        return weights

rules_all = (RuleMomentum, RuleContrarian, RuleRepetition)
