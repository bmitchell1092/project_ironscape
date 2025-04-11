# magic.py
import pygame
from random import randint
from settings import *
from support import get_asset_path

magic_data = {
    'flame': {
        'type': 'damage',
        'cost': 20,
        'graphic': get_asset_path('graphics', 'particles', 'flame', 'fire.png'),
        'potency': 30
    },
    'heal': {
        'type': 'heal',
        'cost': 10,
        'graphic': get_asset_path('graphics', 'particles', 'heal', 'heal.png'),
        'potency': 20
    },
    'charge': {
        'type': 'utility',
        'cost': 15,
        'graphic': get_asset_path('graphics', 'particles', 'aura', 'aura.png'),
        'potency': 0  # Optional: define utility effects later
    }
}

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound(get_asset_path('audio', 'heal.wav')),
            'flame': pygame.mixer.Sound(get_asset_path('audio', 'Fire.wav')),
            'charge': pygame.mixer.Sound(get_asset_path('audio', 'charge.wav'))
        }

    def heal(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['heal']: self.sounds['heal'].play()
            player.health += potency
            player.mana -= cost
            if player.health > player.max_health:
                player.health = player.max_health
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['flame']: self.sounds['flame'].play()
            player.mana -= cost
            direction = self.get_direction_vector(player.status)
            for i in range(1, 6):
                offset = direction * i * TILESIZE
                x = player.rect.centerx + offset.x + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset.y + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('flame', (x, y), groups)

    def charge(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['charge']: self.sounds['charge'].play()
            player.mana -= cost
            self.animation_player.create_particles('aura', player.rect.center, groups)

    def get_direction_vector(self, status):
        direction = status.split('_')[0]
        return {
            'right': pygame.Vector2(1, 0),
            'left': pygame.Vector2(-1, 0),
            'up': pygame.Vector2(0, -1),
            'down': pygame.Vector2(0, 1)
        }.get(direction, pygame.Vector2(0, 0))


class MagicManager:
    def __init__(self):
        self.selected_spells = {
            'damage': None,
            'heal': None,
            'utility': None
        }

    def select_spell(self, spell_name):
        spell = magic_data.get(spell_name)
        if spell:
            self.selected_spells[spell['type']] = spell_name

    def get_selected_spell(self, spell_type):
        return self.selected_spells.get(spell_type, None)

    def cast(self, player, animation_player, groups, key):
        print(f"Casting spell for key: {key}")
        key_map = {'E': 'damage', 'Q': 'heal', 'LCTRL': 'utility'}
        
        spell_type = key_map.get(key)
        if not spell_type:
            return

        spell_name = self.get_selected_spell(spell_type)
        spell = magic_data.get(spell_name)
        if not spell:
            return

        magic_player = MagicPlayer(animation_player)

        if spell_type == 'heal':
            magic_player.heal(player, spell['potency'], spell['cost'], groups)
        elif spell_type == 'damage':
            magic_player.flame(player, spell['potency'], spell['cost'], groups)
        elif spell_type == 'utility':
            magic_player.charge(player, spell['potency'], spell['cost'], groups)

