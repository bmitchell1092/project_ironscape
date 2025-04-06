class Combat:
    def __init__(self, player):
        self.player = player

    def calculate_player_damage(self):
        base_damage = self.player.damage
        # additional combat calculations could go here
        return base_damage

    def calculate_player_defense(self):
        base_defense = self.player.defense
        # additional defense calculations could go here
        return base_defense

    def apply_damage(self, enemy):
        damage_dealt = self.calculate_player_damage() - enemy.defense
        damage_dealt = max(0, damage_dealt)
        enemy.health -= damage_dealt