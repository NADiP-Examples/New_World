from Whizbang import Whizbang

class Spell():
    def __init__(self, name, type, manna_cost, ap_cost, distance, effect=None):
        self.name = name
        self.manna = manna_cost
        self.action_points = ap_cost
        self.distance = distance
        self.type = type
        if self.type == "Attacking": # effect - кол-во урона
            self.damage = effect[0]
            self.whizbang = effect[1]

    def apply(self, target, cor, lst):
        if self.type == "Attacking":
            target.hurt(self.damage)
            lst.append(Whizbang(cor, target.cor, self.whizbang))


fireball = Spell("Огненный шар", "Attacking", 1, 4, 4, effect=(3, "Flying_fireball.png"))