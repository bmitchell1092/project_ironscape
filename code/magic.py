# magic.py
import pygame
from random import randint
from settings import *
from support import get_asset_path, import_folder
import time

class SpellEffect(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(*groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.15
        self.z_index = 3

    def update(self, *args, **kwargs):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


class MagicPlayer:
    def __init__(self, manager):
        self.manager = manager
        self.sounds = {
            'heal':  pygame.mixer.Sound(get_asset_path('audio', 'heal.wav')),
            'flame': pygame.mixer.Sound(get_asset_path('audio', 'Fire.wav')),
            'charge':pygame.mixer.Sound(get_asset_path('audio', 'charge.wav'))
        }

    def heal(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['heal']:
                self.sounds['heal'].play()
            player.health = min(player.max_health, player.health + potency)
            player.mana -= cost
            frames_aura = self.manager.spell_frames.get('aura', [])
            frames_heal = self.manager.spell_frames.get('heal', [])
            if frames_aura: SpellEffect(player.rect.center, frames_aura, [groups])
            if frames_heal: SpellEffect(player.rect.center, frames_heal, [groups])

    def flame(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['flame']:
                self.sounds['flame'].play()
            player.mana -= cost
            direction = self.get_direction_vector(player.status)
            frames_flame = self.manager.spell_frames.get('flame', [])
            for i in range(1, 6):
                offset = direction * i * TILESIZE
                x = player.rect.centerx + offset.x + randint(-TILESIZE//3, TILESIZE//3)
                y = player.rect.centery + offset.y + randint(-TILESIZE//3, TILESIZE//3)
                if frames_flame:
                    SpellEffect((x, y), frames_flame, groups)

    def charge(self, player, potency, cost, groups):
        if player.mana >= cost:
            if self.sounds['charge']:
                self.sounds['charge'].play()
            player.mana -= cost
            frames_charge = self.manager.spell_frames.get('charge', [])
            if frames_charge:
                SpellEffect(player.rect.center, frames_charge, [groups])

    def get_direction_vector(self, status):
        direction = status.split('_')[0]
        return {
            'right': pygame.Vector2(1, 0),
            'left':  pygame.Vector2(-1, 0),
            'up':    pygame.Vector2(0, -1),
            'down':  pygame.Vector2(0, 1)
        }.get(direction, pygame.Vector2(0, 0))


class MagicManager:
    def __init__(self):
        self.magic_data = {
            'flame':  {'type': 'damage', 'cost': 20, 'potency': 30, 'cooldown': 1000},
            'heal':   {'type': 'heal',   'cost': 10, 'potency': 20, 'cooldown': 500},
            'charge': {'type': 'utility','cost': 15, 'potency': 0,  'cooldown': 300}
        }
        self.selected_spells = {'damage': None, 'heal': None, 'utility': None}
        self.cooldowns = {}
        self.spell_frames = {}
        self.magic_player = MagicPlayer(self)

    def load_assets(self):
        self.spell_frames['aura']  = import_folder(get_asset_path('graphics', 'particles', 'aura','frames'))
        self.spell_frames['heal']  = import_folder(get_asset_path('graphics', 'particles', 'heal','frames'))
        self.spell_frames['flame'] = import_folder(get_asset_path('graphics', 'particles', 'flame','frames'))
        self.spell_frames['charge']= import_folder(get_asset_path('graphics', 'particles', 'aura','frames'))

    def select_spell(self, spell_name):
        spell = self.magic_data.get(spell_name)
        if spell:
            self.selected_spells[spell['type']] = spell_name

    def get_selected_spell(self, spell_type):
        return self.selected_spells.get(spell_type, None)

    def get_spell_data(self, spell_name):
        return self.magic_data.get(spell_name, {})

    def cast(self, player, groups, key):
        print(f"Attempting to cast: {key}")
        key_map = {'E': 'damage', 'Q': 'heal', 'LCTRL': 'utility'}
        spell_type = key_map.get(key)
        if not spell_type:
            return

        spell_name = self.get_selected_spell(spell_type)
        spell = self.magic_data.get(spell_name)
        if not spell:
            return

        now = pygame.time.get_ticks()
        cooldown = spell.get("cooldown", 500)
        last_cast = self.cooldowns.get(spell_name, 0)
        if now - last_cast < cooldown:
            return

        self.cooldowns[spell_name] = now
        if spell_type == 'heal':
            self.magic_player.heal(player, spell['potency'], spell['cost'], groups)
        elif spell_type == 'damage':
            self.magic_player.flame(player, spell['potency'], spell['cost'], groups)
        elif spell_type == 'utility':
            self.magic_player.charge(player, spell['potency'], spell['cost'], groups)





