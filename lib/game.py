from .util import echo, pick_weighted, Vector
from .rule import rules_all

class Player:
    def __init__(self, game):
        self._game = game
        self.rules = tuple(rule_class(game) for rule_class in rules_all)

        for rule in self.rules:
            rule.value = 1.0 / len(self.rules)

    def new_rule_value(self, rule_value, weight_at_given):
        new = rule_value * weight_at_given
        if new < 10**(-5):
            new = 10**(-5)
        return new

    def pick(self):
        '''
        This function is randomized but does not modify internal state
        '''
        total_weights = Vector(self._game.space_size*[0.0])
        total_weights = sum( ( rule.value * rule.get_weights()
                               for rule in self.rules ),
                             total_weights )

        return pick_weighted(total_weights)

    def collect(self, given):
        weights_at_given = Vector( rule.get_weights()[given]
                                   for rule in self.rules )

        # `weights_at_given` is not necessarily normalized!
        #weights_at_given.normalize()

        new_values = Vector( self.new_rule_value(rule.value, w)
                             for rule, w in zip(self.rules, weights_at_given) )

        new_values.normalize()

        for rule, new_value in zip(self.rules, new_values):
            rule.value = new_value

class Game:
    def __init__(self, size):
        self.space_size = size        # tokens are 0, 1, ..., (size - 1)
        self.history = []             # list of (human, computer) choice pairs
        self.player = Player(self)
        self.player_last_picked = None

    def player_pick(self):
        self.player_last_picked = self.player.pick()
        return self.player_last_picked

    def player_collect(self, given):
        self.player.collect(given)
        self.history.append((given, self.player_last_picked))
