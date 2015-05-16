from Whizbang import Whizbang

class Spell():
    def __init__(self, name, type, manna_cost, ap_cost, distance, effect=None):
        self.name = name
        self.manna = manna_cost
        self.action_points = ap_cost
        self.distance = distance
        self.type = type
        if self.type == "Attacking":  # effect - кол-во урона
            self.damage = effect[0]
            self.whizbang = effect[1]
        elif self.type == "Defence":
            self.armor_improve = effect[0]
            self.healf_improve = effect[1]

    def apply(self, exorcist, target, cor, lst):
        if exorcist.manna - self.manna < 0:
            return
        else:
            exorcist.manna -= self.manna
        if self.type == "Attacking":
            target.hurt(self.damage)
            lst.append(Whizbang(cor, target.cor, self.whizbang))
        elif self.type == "Defence":

            target.armor += self.armor_improve
            koof = target.max_healf/target.healf
            target.max_healf += self.healf_improve
            target.healf += target.healf*koof
            target.healf = int(target.healf)


fireball = Spell("Огненный шар", "Attacking", 1, 4, 4, effect=(3, "Flying_fireball.png"))
improve_aah = Spell("Божественная помощь!", "Defence", 1, 4, 4, effect=(10, 30))