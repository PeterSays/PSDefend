
class Material:
    def __init__(self, name, resource, color_a, color_b,
                 pierce_resist=1.0, bash_resist=1.0, cut_resist=1.0,
                 cold_dam=-100, heat_dam=100, temp_conduct=1.0, temp_resist=1.0):
        self.name = name
        self.resource = resource
        self.color_a = color_a
        self.color_b = color_b
        self.pierce_resist = pierce_resist
        self.bash_resist = bash_resist
        self.cut_resist = cut_resist
        self.temp_resist = temp_resist
        self.cold_dam = cold_dam
        self.heat_dam = heat_dam
        self.temp_conduct = temp_conduct
