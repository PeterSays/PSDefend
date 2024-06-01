class Skill:
    def __init__(self, name, pow_min, pow_max, kind, targ_type='adjacent', aoe_type='spot', repeats=1, move_cost=1, hp_cost=0, mp_cost=0, pierce=1, bash=0, cut=0,
                 user_anim=None, target_anim=None, passive=False, magic=False):
        self.name = name
        self.power_minimum = pow_min
        self.power_maximum = pow_max
        self.kind = kind  # attack,
        self.magic = magic
        self.targ_type = targ_type
        self.aoe = [(0, 0)]
        self.aoe_type = aoe_type
        self.repeats = repeats
        self.move_cost = move_cost
        self.hp_cost = hp_cost
        self.mp_cost = mp_cost
        self.pierce = pierce
        self.bash = bash
        self.cut = cut

        self.passive = passive

        self.user_anim = user_anim
        self.target_anim = target_anim
