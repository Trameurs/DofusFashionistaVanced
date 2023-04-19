# Copyright (C) 2020 The Dofus Fashionista
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from copy import copy


CHARACTER_CLASSES = sorted(['Eniripsa', 'Iop', 'Xelor', 'Osamodas', 'Feca',
                     'Sacrier', 'Ecaflip', 'Enutrof', 'Sram', 'Sadida',
                     'Cra', 'Pandawa', 'Rogue', 'Masqueraider', 'Foggernaut',
                     'Eliotrope', 'Huppermage', 'Ouginak'])

TYPE_NAME_TO_SLOT = {
    'Weapon': 'weapon',
    'Shield': 'shield',
    'Hat': 'hat',
    'Cloak': 'cloak',
    'Amulet': 'amulet',
    'Ring': 'ring',
    'Belt': 'belt',
    'Boots': 'boots',
    'Dofus': 'dofus',
    'Pet': 'pet',
}

SLOT_NAME_TO_TYPE = {
    'weapon': 'Weapon',
    'shield': 'Shield',
    'hat': 'Hat',
    'cloak': 'Cloak',
    'amulet': 'Amulet',
    'ring1': 'Ring',
    'ring2': 'Ring',
    'belt': 'Belt',
    'boots': 'Boots',
    'dofus1': 'Dofus',
    'dofus2': 'Dofus',
    'dofus3': 'Dofus',
    'dofus4': 'Dofus',
    'dofus5': 'Dofus',
    'dofus6': 'Dofus',
    'pet': 'Pet',
}

TYPE_NAME_TO_SLOT_NUMBER = {
    'Weapon': 1,
    'Shield': 1,
    'Hat': 1,
    'Cloak': 1,
    'Amulet': 1,
    'Ring': 2,
    'Belt': 1,
    'Boots': 1,
    'Dofus': 6,
    'Pet': 1,
}

TYPE_NAMES = TYPE_NAME_TO_SLOT.keys()

SLOTS = []
for type_name in TYPE_NAMES:
    slot_number = TYPE_NAME_TO_SLOT_NUMBER[type_name]
    slot_name = TYPE_NAME_TO_SLOT[type_name]
    if slot_number > 1:
        for i in range(1, slot_number + 1):
            SLOTS.append("%s%d" % (slot_name, i))
    else:
        SLOTS.append(slot_name)
        
STAT_NAME_TO_KEY = {
    'Power': 'pow',
    'Damage': 'dam',
    'Heals': 'heals',
    'AP': 'ap',
    'MP': 'mp',
    'Critical Hits': 'ch',
    'Agility': 'agi',
    'Strength': 'str',
    'Neutral Damage': 'neutdam',
    'Earth Damage': 'earthdam',
    'Intelligence': 'int',
    'Fire Damage': 'firedam',
    'Air Damage': 'airdam',
    'Chance': 'cha',
    'Water Damage': 'waterdam',
    'Vitality': 'vit',
    'Initiative': 'init',
    'Summon': 'summon',
    'Range': 'range',
    'Wisdom': 'wis',
    'Neutral Resist': 'neutres',
    'Water Resist': 'waterres',
    'Air Resist': 'airres',
    'Fire Resist': 'fireres',
    'Earth Resist': 'earthres',
    '% Neutral Resist': 'neutresper',
    '% Air Resist': 'airresper',
    '% Fire Resist': 'fireresper',
    '% Water Resist': 'waterresper',
    '% Earth Resist': 'earthresper',
    'Neutral Resist in PVP': 'pvpneutres',
    'Water Resist in PVP': 'pvpwaterres',
    'Air Resist in PVP': 'pvpairres',
    'Fire Resist in PVP': 'pvpfireres',
    'Earth Resist in PVP': 'pvpearthres',
    '% Neutral Resist in PVP': 'pvpneutresper',
    '% Air Resist in PVP': 'pvpairresper',
    '% Fire Resist in PVP': 'pvpfireresper',
    '% Water Resist in PVP': 'pvpwaterresper',
    '% Earth Resist in PVP': 'pvpearthresper',
    'Prospecting': 'pp',
    'Pods': 'pod',
    'AP Reduction': 'apred',
    'MP Reduction': 'mpred',
    'Lock': 'lock',
    'Dodge': 'dodge',
    'Reflects': 'ref',
    'Pushback Damage': 'pshdam',
    'Trap Damage': 'trapdam',
    '% Trap Damage': 'trapdamper',
    'Critical Resist': 'crires',
    'Pushback Resist': 'pshres',
    'MP Loss Resist': 'mpres',
    'AP Loss Resist': 'apres',
    'Critical Damage': 'cridam',
    'Critical Failure': 'cf',
    '% Melee Damage': 'permedam',
    '% Ranged Damage': 'perrandam',
    '% Weapon Damage': 'perweadam',
    '% Spell Damage': 'perspedam',
    '% Melee Resist': 'respermee',
    '% Ranged Resist': 'resperran',
    'HP': 'hp'
}

STAT_ORDER = {
    'hp': 0,
    'vit': 1,
    'str': 2,
    'int': 3,
    'cha': 4,
    'agi': 5,
    'wis': 6,
    'pow': 7,
    
    'ch': 11,
    'ap': 12,
    'mp': 13,
    'range': 14,
    'summon': 15,
    'init': 16,
    'pod': 17,
    'pp': 18,
    
    'dam': 21,
    'neutdam': 22,
    'earthdam': 23,
    'firedam': 24,
    'waterdam': 25,
    'airdam': 26,
    
    'heals': 31,
    
    'neutres': 71,
    'earthres': 72,
    'fireres': 73,
    'waterres': 74,
    'airres': 75,
    'crires': 76,
    'pshres': 77,
    'neutresper': 81,
    'earthresper': 82,
    'fireresper': 83,
    'waterresper': 84,
    'airresper': 85,
    
    'pvpneutres': 133,
    'pvpearthres': 134,
    'pvpfireres': 135,
    'pvpwaterres': 136,
    'pvpairres': 137,
    'pvpneutresper': 138,
    'pvpearthresper': 139,
    'pvpfireresper': 140,
    'pvpwaterresper': 141,
    'pvpairresper': 142,
    
    'lock': 91,
    'dodge': 92,
    'apred': 93,
    'mpred': 94,
    'apres': 95,
    'mpres': 96,
    
    'pshdam': 101,
    'cridam': 102,   
    'trapdam': 103,
    'trapdamper': 104, 
    'cf': 111,
    'ref': 112,
    
    'pvpcrires': 120,
    'pvppshres': 121,
    
    'permedam': 127,
    'perrandam': 128,
    'perweadam': 129,
    'perspedam': 130,
    'respermee': 131,
    'resperran': 132,
}

STAT_MAXIMUM = {
    'AP': 12,
    'MP': 6,
    'Range': 6,
    '% Neutral Resist': 53,
    '% Air Resist': 53,
    '% Fire Resist': 53,
    '% Water Resist': 53,
    '% Earth Resist': 53,
}

STAT_KEY_TO_NAME = {v: k for k, v in STAT_NAME_TO_KEY.iteritems()}

# Stats still in projects (weights, minimums) but not used anymore.
# Adding them here prevents crashes with legacy projects that still have them.
# If a migration is done to remove them from all projects, they can be cleaned
# up from DEPRECATED_STATS.
DEPRECATED_STATS = {
#     'Neutral Resist in PVP': 'pvpneutres',
#     'Water Resist in PVP': 'pvpwaterres',
#     'Air Resist in PVP': 'pvpairres',
#     'Fire Resist in PVP': 'pvpfireres',
#     'Earth Resist in PVP': 'pvpearthres',
#     '% Neutral Resist in PVP': 'pvpneutresper',
#     '% Air Resist in PVP': 'pvpairresper',
#     '% Fire Resist in PVP': 'pvpfireresper',
#     '% Water Resist in PVP': 'pvpwaterresper',
#     '% Earth Resist in PVP': 'pvpearthresper',
#    'pvpneutres',
#    'pvpearthres',
#    'pvpfireres',
#    'pvpwaterres',
#    'pvpairres',
#    'pvpneutresper',
#    'pvpearthresper',
#    'pvpfireresper',
#    'pvpwaterresper',
#    'pvpairresper',
}

AGI_TARGETS = [
    (0, 2),
    (8, 3),
    (42, 4),
    (134, 5),
    (384, 6),
    (1060, 7),
]

MIN_AGI_FOR_BONUS = dict((e[1], e[0]) for e in AGI_TARGETS)

CRIT_TARGETS = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

BASE_STATS = ['vit', 'wis', 'str', 'int', 'cha', 'agi']
MAIN_STATS = ['str', 'int', 'cha', 'agi']

STATS_NAMES = [(STAT_KEY_TO_NAME[stat_key], stat_key) for stat_key in BASE_STATS]

AIR = 'air'
FIRE = 'fire'
WATER = 'water'
NEUTRAL = 'neut'
EARTH = 'earth'
DAMAGE_TYPE_TO_MAIN_STAT = {
    NEUTRAL: 'str',
    EARTH: 'str',
    FIRE: 'int',
    WATER: 'cha',
    AIR: 'agi'
}
DAMAGE_TYPES = [NEUTRAL, EARTH, FIRE, WATER, AIR]
ELEMENT_KEY_TO_NAME = {
    'neut': 'Neutral',
    'earth': 'Earth',
    'fire': 'Fire',
    'water': 'Water',
    'air': 'Air'
}
ELEMENT_NAME_TO_KEY = {v: k for k, v in ELEMENT_KEY_TO_NAME.iteritems()}

WEIRD_CONDITION_FROM_ID = {1: 'light_set'}
WEIRD_CONDITION_TO_ID = {v: k for k, v in WEIRD_CONDITION_FROM_ID.iteritems()}
WEIRD_CONDITIONS = WEIRD_CONDITION_TO_ID.keys() 

class Spell:
    def __init__(self, name, level_req, effects, aggregates=[], 
                 is_linked=None, stacks=1, special=None):
        self.name = name
        self.level_req = level_req
        self.effects = effects
        self.aggregates = aggregates
        self.stacks = stacks
        self.digest = None
        self.is_linked = is_linked
        self.special = special

    def get_effects_digest(self):
        if self.digest is None:
            self.digest = self.build_effects_digest()
        return self.digest
        
    def build_effects_digest(self):
        levels = len(self.level_req)
        e = self.effects
        non_crit = [[] for _ in range(levels)]
        for dam_entry in range(len(e.elements)):
            non_crit_range = (e.non_crit_ranges[dam_entry]
                              if (e.non_crit_ranges is not None
                                  and len(e.non_crit_ranges) > dam_entry)
                              else None)
            if non_crit_range:
                element = e.elements[dam_entry]
                steals = (e.steals[dam_entry] if e.steals is not None else False)
                heals = (e.heals[dam_entry] if e.heals is not None else False)
                for level in range(levels):
                    non_crit[level].append(DamageDigest(non_crit_range[level].min_dam,
                                                        non_crit_range[level].max_dam,
                                                        element,
                                                        steals,
                                                        heals))
        crit = [[] for _ in range(levels)]
        for dam_entry in range(len(e.crit_elements)):
            crit_range = (e.crit_ranges[dam_entry]
                          if (e.crit_ranges is not None
                              and len(e.crit_ranges) > dam_entry)
                          else None)
            if crit_range:
                element = e.crit_elements[dam_entry]
                steals = (e.steals[dam_entry] if e.steals is not None else False)
                heals = (e.heals[dam_entry] if e.heals is not None else False)
                for level in range(levels):
                    crit[level].append(DamageDigest(crit_range[level].min_dam,
                                                  crit_range[level].max_dam,
                                                  element,
                                                  steals,
                                                  heals))
        
        return EffectsDigest(non_crit, crit, self.aggregates)

class Effects:
    def __init__(self, non_crit_ranges, crit_ranges, elements, crit_elements=None, 
                 steals=None, heals=None):
        self.non_crit_ranges = [[Range(r) for r in l] for l in non_crit_ranges]
        self.crit_ranges = ([[Range(r) for r in l] for l in crit_ranges]
                            if crit_ranges is not None
                            else None)
        self.elements = elements
        self.crit_elements = crit_elements if crit_elements else elements
        self.steals = steals
        self.heals = heals

class Range:
    def __init__(self, min_max_dam):
        min_max_dam_string = min_max_dam.split('-')
        if len(min_max_dam_string) == 1:
            self.min_dam = self.max_dam = int(min_max_dam_string[0])
        else:
            self.min_dam = int(min_max_dam_string[0])
            self.max_dam = int(min_max_dam_string[1])

class EffectsDigest:
    def __init__(self, non_crit_dams, crit_dams, aggregates=[]):
        self.hit_number = len(non_crit_dams[0])
        self.non_crit_dams = non_crit_dams
        self.crit_dams = crit_dams
        self.aggregates = aggregates

class BaseDamage:
    def __init__(self, min_dam, max_dam, element, steals=False, heals=False):
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.element = element
        self.steals = steals
        self.heals = heals

    def __repr__(self):
        return '%d-%d (%s)' % (self.min_dam,
                               self.max_dam,
                               self.element)    
        #return '%s%d-%d (%s)' % (('%s ' % self.hit_name) if self.hit_name else '',
        #                           self.min_dam,
        #                           self.max_dam,
        #                           self.element)  
                                            
    def average(self):
        return (self.min_dam + self.max_dam) / 2.0
        
    def copy_with_element(self, element):
        new_instance = copy(self)
        new_instance.element = element
        return new_instance

class DamageDigest(BaseDamage):
    pass

def create_duster_values(base, base_per_tofu, max_tofus):
    spell = []
    for i in range(max_tofus + 1):
        inner_spell = []
        for values in base:
            dam = '%d-%d' % (values[0] + base_per_tofu * i, 
                             values[1] + base_per_tofu * i)
            inner_spell.append(dam)
        spell.append(inner_spell)
    return spell

def create_stacking_values(base, bonus, times):
    spell = []
    for i in range(times):
        inner_spell = []
        for values in base:
            dam = '%d-%d' % (values[0] + bonus * i, 
                             values[1] + bonus * i)
            inner_spell.append(dam)
        spell.append(inner_spell)
    return spell

def create_level_based_stacking_values(base, bonus, times):
    spell = []
    for i in range(times):
        inner_spell = []
        for j in range(len(base)):
            dam = '%d-%d' % (base[j][0] + bonus[j] * i, 
                             base[j][1] + bonus[j] * i)
            inner_spell.append(dam)
        spell.append(inner_spell)
    return spell

CHARGED_LABELS = [
    'Not charged',
    'Charged once',
    'Charged twice',
] + ['Charged %d times' % n for n in range(3, 10)]

DAMAGE_SPELLS = {
    'default': [
        Spell('Perfidious Boomerang', [1], Effects(
            [['31-40'] for i in range(4)],
            [['41-50'] for i in range(4)],
            [EARTH, FIRE, WATER, AIR],
            steals=[True for i in range(4)],
        ), aggregates=[("25% chance of", [0]),
                       ("25% chance of", [1]),
                       ("25% chance of", [2]),
                       ("25% chance of", [3])]),
        Spell('Leek Pie', [1], Effects(
            [['8-10']],
            [['11-13']],
            [FIRE]
        )),
        Spell('Moon Hammer', [1], Effects(
            [['38-47']],
            [['49']],
            [AIR]
        )),
        Spell('Lightning Strike', [1], Effects(
            [['26-30']],
            [['31-35']],
            [FIRE]
        )),
        Spell('Weapon Skill', [1], Effects(
            [['300']],
            [['350']],
            ['buff_pow_weapon']
        )),
    ],
    'Cra': [
        Spell('Magic Arrow', [1, 66, 132], Effects(
            [['11-13', '15-17', '19-21']],
            [['13-15', '18-20', '23-25']],
            [AIR]
        ), is_linked=(1, 'Concentration Arrow')),
        Spell('Concentration Arrow', [95, 162], Effects(
            [['18-21', '22-26']],
            [['21-25', '26-31']],
            [AIR]
        ), is_linked=(2, 'Magic Arrow')),
        Spell('Retreat Arrow', [1, 67, 133], Effects(
            [['15-17', '20-22', '25-28']],
            [['18-20', '23-26', '30-34']],
            [AIR]
        ), is_linked=(1, 'Erosive Arrow')),
        Spell('Erosive Arrow', [100, 167], Effects(
            [['20-23', '25-29']],
            [['24-28', '30-35']],
            [EARTH]
        ), is_linked=(2, 'Retreat Arrow')),
        Spell('Frozen Arrow', [3, 69, 136], Effects(
            [['10-12', '13-15', '17-19']],
            [['12-14', '16-18', '20-23']],
            [FIRE]
        ), is_linked=(1, 'Paralysing Arrow')),
        Spell('Paralysing Arrow', [110, 177], Effects(
            [['31-34', '39-42']],
            [['38-40', '47-50']],
            [FIRE]
        ), is_linked=(2, 'Frozen Arrow')),
        Spell('Burning Arrow', [6, 71, 138], Effects(
            [['19-21', '26-28', '33-35']],
            [['23-25', '32-34', '40-42']],
            [FIRE]
        ), is_linked=(1, 'Repulsive Arrow')),
        Spell('Repulsive Arrow', [115, 182], Effects(
            [['24-27', '28-32']],
            [['29-33', '34-38']],
            [FIRE]
        ), is_linked=(2, 'Burning Arrow')),
        Spell('Atonement Arrow', [15, 82, 149], Effects(
            create_level_based_stacking_values(((22, 24), (28, 30), (35, 37)), 
                                               (23, 29, 36), 3),
            create_level_based_stacking_values(((26, 28), (34, 36), (42, 44)), 
                                               (27, 35, 43), 3),
            [WATER, WATER, WATER],
        ), aggregates=[("Not charged", [0]),
                       ("Charged once", [1]),
                       ("Charged twice", [2])],
        is_linked=(1, 'Redemption Arrow')),
        Spell('Redemption Arrow', [125, 192], Effects(
            create_level_based_stacking_values(((17, 19), (19, 22)), 
                                               (10, 12), 2),
            create_level_based_stacking_values(((20, 23), (23, 26)), 
                                               (10, 35), 2),
            [WATER]*2,
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)],
        is_linked=(2, 'Atonement Arrow')),
        Spell("Bat's Eye", [20, 87, 154], Effects(
            [['10-12', '13-15', '16-18']],
            [['12-14', '15-17', '19-22']],
            [WATER]
        ), is_linked=(1, 'Crushing Arrow')),
        Spell('Crushing Arrow', [130, 197], Effects(
            [['30-34', '34-38']],
            [['36-41', '41-46']],
            [FIRE]
        ), is_linked=(2, "Bat's Eye")),
        Spell('Critical Shooting', [25, 92, 159], Effects(
            [['0', '0', '0']],
            [['10', '30', '50']],
            ['buff_pow']
        )),
        Spell('Immobilising Arrow', [30, 97, 164], Effects(
            [['6-7', '8-9', '10-11']],
            [['7-8', '10-11', '12-13']],
            [WATER]
        ), is_linked=(1, 'Assailing Arrow')),
        Spell('Assailing Arrow', [140], Effects(
            [['33-37'],
             ['100']],
            [['40-44'],
             ['100']],
            [WATER, 'buff_pow']
        ), stacks=3, is_linked=(2, 'Immobilising Arrow')),
        Spell('Punitive Arrow', [35, 102, 169], Effects(
            create_level_based_stacking_values(((18, 20), (23, 25), (29, 31)), 
                                               (19, 24, 30), 3),
            create_level_based_stacking_values(((22, 24), (28, 30), (35, 37)), 
                                               (23, 29, 36), 3),
            [EARTH, EARTH, EARTH]
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(3)],
        is_linked=(1, 'Arrow of Judgement')),
        Spell('Arrow of Judgement', [145], Effects(
            [['39-45']],
            [['47-54']],
            [EARTH]
        ), is_linked=('Punitive Arrow')),
        Spell('Powerful Shooting', [40, 107, 174], Effects(
            [['150', '200', '250']],
            [['170', '230', '290']],
            ['buff_pow_spell']
        )),
        Spell('Plaguing Arrow', [45, 112, 179], Effects(
            [['8-10', '11-13', '13-15']],
            [['10-12', '13-15', '16-18']],
            [AIR]
        ), is_linked=(1, 'Slaughtering Arrow')),
        Spell('Slaughtering Arrow', [155], Effects(
            create_stacking_values(((34, 38),), 18, 2),
            create_stacking_values(((41, 46),), 22, 2),
            [AIR]*2,
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)],
        is_linked=(2, 'Plaguing Arrow')),
        Spell('Poisoned Arrow', [50, 117, 184], Effects(
            [['10-11', '14-15', '17-18']],
            [['13-14', '17-18', '20-21']],
            [NEUTRAL]
        )),
        Spell('Tormenting Arrow', [55, 122, 189], Effects(
            [['7-9', '9-11', '11-13'],
             ['7-9', '9-11', '11-13']],
            [['8-10', '12-14', '13-16'],
             ['8-10', '12-14', '13-16']],
            [FIRE, AIR],
        ), aggregates=[('', [0, 1])],
        is_linked=(1, 'Tyrannical Arrow')),
        Spell('Tyrannical Arrow', [165], Effects(
            [['15'],
             ['15']],
            None,
            [FIRE, AIR],
        ), aggregates=[("If the target is pushed", [1]),
                       ("If the target suffers pushback damage", [0])],
        is_linked=(2, 'Tormenting Arrow')),
        Spell('Destructive Arrow', [60, 127, 194], Effects(
            [['21-23', '27-29', '30-32']],
            [['26-28', '32-34', '36-38']],
            [EARTH]
        ), is_linked=(1, 'Barricade Shot')),
        Spell('Barricade Shot', [170], Effects(
            [['29-33']],
            [['35-40']],
            [EARTH]
        ), is_linked=(2, 'Destructive Arrow')),
        Spell('Absorptive Arrow', [65, 131, 198], Effects(
            [['21-23', '26-28', '29-31']],
            [['26-28', '31-33', '35-37']],
            [AIR],
            steals=[True],
        ), is_linked=(1, 'Devouring Arrow')),
        Spell('Devouring Arrow', [175], Effects(
            [['11-13'],
             ['23-27'],
             ['34-38'],
             ['52-56'],
             ['70-74']],
            [['13-15'],
             ['26-30'],
             ['39-43'],
             ['60-64'],
             ['81-85']],
            [AIR, AIR, AIR, AIR, AIR]
        ), is_linked=(2, 'Absorptive Arrow')),
        Spell('Slow Down Arrow', [75, 142], Effects(
            [['29-31', '36-38']],
            [['35-37', '43-46']],
            [WATER]
        ), is_linked=(1, 'Striking Arrow')),
        Spell('Striking Arrow', [185], Effects(
            [['7-10']],
            [['8-12']],
            [WATER]
        ), is_linked=(2, 'Slow Down Arrow')),
        Spell('Conniving Arrow', [80, 147], Effects(
            [['31-34', '38-42']],
            [['37-40', '46-50']],
            [EARTH]
        ), is_linked=(1, 'Abolition Arrow')),
        Spell('Abolition Arrow', [190], Effects(
            [['34-38'],
             ['44-50']],
            [['41-46'],
             ['53-60']],
            [AIR, AIR]
        ), aggregates=[("Summons", [1]),
                       ("Others", [0])], 
        is_linked=(2, 'Conniving Arrow')),
        Spell('Explosive Arrow', [85, 152], Effects(
            [['24-27', '30-34']],
            [['29-33', '36-41']],
            [FIRE]
        ), is_linked=(1, 'Fulminating Arrow')),
        Spell('Fulminating Arrow', [195], Effects(
            [['38-42'],
             ['48-52']],
            None,
            [FIRE, FIRE]
        ), aggregates=[("Regular shot", [0]),
                       ("After bouncing once", [1])], 
        is_linked=(2, 'Explosive Arrow')),
        Spell('Bow Skill', [90, 157], Effects(
            [['40', '60']],
            [['50', '70']],
            ['buff_dam']
        ), is_linked=(1, 'Sentinel')),
        Spell('Sentinel', [200], Effects(
            [['30']],
            None,
            ['buff_pow_spell']
        ), is_linked=(2, 'Bow Skill')),
    ],
    'Ecaflip': [
        Spell('Heads or Tails', [1, 66, 132], Effects(
            [['15-17', '20-23', '26-29'],
             ['10-12', '14-16', '18-20']],
            [['19-21', '24-27', '31-35'],
             ['13-15', '17-19', '22-24']],
            [EARTH, EARTH],
        ), aggregates=[('This turn', [0]),
                       ('Next turn', [1])], 
        is_linked=(1, 'Tails or Heads')),
        Spell('Tails or Heads', [95, 162], Effects(
            [['19-22','6-7']],
            [['0', '100']],
            [EARTH],
            crit_elements=['buff_pow']
        ), is_linked=(2, 'Heads or Tails')),
        Spell('Balling Up', [1, 67, 133], Effects(
            [['17-19', '23-25', '29-32']],
            [['21-23', '27-30', '35-38']],
            [AIR],
        ), 
        is_linked=(1, 'Meowch')),
        Spell('Meowch', [100, 167], Effects(
            [['20-23','25-29'],
             ['0', '0']],
            [['7-8', '9-10'],
             ['100', '150']],
            [FIRE, 'buff_int'],
        ), is_linked=(2, 'Balling Up')),        
        Spell('Bluff', [3, 69, 136], Effects(
            [['17-19', '23-25', '29-32'],
             ['0', '0', '0']],
            [['6-7', '8-9', '10-12'],
             ['50', '100', '150']],
            [WATER, 'buff_cha'],
        ), is_linked=(1, 'Nerve')),
        Spell('Nerve', [110, 177], Effects(
            [['28-31','35-39']],
            [['9-11', '12-14'],
             ['120', '200']],
            [AIR, 'buff_agi'],
        ), is_linked=(2, 'Bluff')),
        Spell('Topkaj', [10, 77, 144], Effects(
            [['16-18', '22-24', '27-30']],
            [['19-21', '26-29', '32-36']],
            [FIRE]
        ), is_linked=(1, 'Yowling')),
        Spell('Yowling', [120, 187], Effects(
            [['26-30','30-34'],
             ['26-30','30-34']],
            [['31-36','36-41'],
             ['31-36','36-41']],
            [FIRE, FIRE],
            heals=[False, True],
        ), aggregates=[('Enemies', [0]),
                       ('Allies', [1])], is_linked=(2, 'Topkaj')),
        Spell('Roar', [130, 197], Effects(
            [['50', '70']],
            None,
            ['buff_pow']
        )),
        Spell('All or Nothing', [25, 92, 159], Effects(
            [['20-29', '34-37', '42-46']] * 4,
            [['32-35', '40-44', '50-55']] * 4,
            [WATER, FIRE, FIRE, WATER],
            heals=[False, True, True, False],
        ), aggregates=[('Enemies (imediately)', [0]),
                       ('Enemies (next turn)', [1]),
                       ('Allies (imediately)', [2]),
                       ('Allies (next turn)', [3])],
        is_linked=(1, 'Peril')),
        Spell('Peril', [135], Effects(
            [['37-41'],
             ['32-36']],
            [['44-49'],
             ['38-43']],
            [WATER, FIRE],
            heals=[False, True],
        ), aggregates=[('Summons', [0]),
                       ('Others', [1])], 
        is_linked=(2, 'All or Nothing')),
        Spell('Rough Tongue', [40, 107, 174], Effects(
            [['19-21', '24-27', '30-33']],
            [['23-25', '29-32', '36-40']],
            [FIRE]
        ), is_linked=(1, 'Lapping Up')),
        Spell('Lapping Up', [150], Effects(
            [['32-36']],
            [['38-43']],
            [EARTH],
        ), is_linked=(2, 'Rough Tongue')),
        Spell('Wheel of Fortune', [45, 112, 179], Effects(
            [['100', '175', '250']],
            [['240', '245', '350']],
            ['buff_pow_spell']
        )),
        Spell('Feline Spirit', [50, 117, 184], Effects(
            [['19-21', '26-29', '31-34']],
            [['23-26', '32-35', '37-41']],
            [EARTH]
        ), is_linked=(1, 'Pawpads')),
        Spell('Pawpads', [160], Effects(
            [['26-30']],
            [['32-36']],
            [FIRE],
        ), is_linked=(2, 'Feline Spirit')),
        Spell('Reflex', [65, 131, 198], Effects(
            [['23-26', '28-31', '31-35']],
            [['28-31', '33-38', '37-42']],
            [AIR]
        ), is_linked=(1, 'Bravado')),
        Spell('Bravado', [175], Effects(
            [['46-50']],
            [['55-60']],
            [AIR],
        ), is_linked=(2, 'Reflex')),
        Spell('Playful Claw', [70, 137], Effects(
            [['27-30', '35-39']],
            None,
            [WATER],
        ), is_linked=(1, 'Misadventure')),
        Spell('Misadventure', [180], Effects(
            [['37-41']],
            [['44-49'],
             ['44-49']],
            [EARTH,EARTH],
            steals=[False, True]
        ), is_linked=(2, 'Playful Claw')),
        Spell('Felintion', [75, 142], Effects(
            [['27-29', '33-36']],
            [['32-35', '40-43']],
            [WATER],
            steals=[True]
        ), is_linked=(1, 'Kraps')),
        Spell('Kraps', [185], Effects(
            [['42-46']],
            [['50-55']],
            [WATER],
        ), is_linked=(2, 'Felintion')),
        Spell('Claw of Ceangal', [80, 147], Effects(
            [['13-15', '17-19']],
            [['16-18', '20-23']],
            [AIR]
        ), is_linked=(1, 'Misfortune')),
        Spell('Misfortune', [190], Effects(
            [['27-30']],
            [['32-36']],
            [WATER],
        ), is_linked=(2, 'Claw of Ceangal')),
        Spell('Rekop', [85, 152], Effects(
            [['15-17', '19-21']] * 4,
            None,
            [FIRE, EARTH, AIR, WATER],
        ),
        is_linked=(1, 'Trickery')),
        Spell('Trickery', [195], Effects(
            [['58-62'],
             ['46-50'],
             ['34-38'],
             ['23-25']],
            [['70-74'],
             ['55-60'],
             ['41-46'],
             ['28-30']],
            [EARTH, AIR, WATER, FIRE],
        ), aggregates=[('5 AP', [0]),
                       ('4 AP', [1]),
                       ('3 AP', [2]),
                       ('2 AP', [3])],
        is_linked=(2, 'Rekop')),
        Spell('Fate of Ecaflip', [90, 157], Effects(
            [['31-34', '38-42']],
            [['37-40', '46-50']],
            [EARTH]
        ), is_linked=(1, "Ecaflip's Audacity")),
        Spell("Ecaflip's Audacity", [200], Effects(
            [['27-30'],
             ['150']],
            [['32-36'],
             ['180']],
            [EARTH, 'buff_pow'],
        ), aggregates=[('', [0]),
                       ('If the target is pushed', [1])], 
        is_linked=(2, 'Fate of Ecaflip')),
    ],
    'Eniripsa': [
        
        Spell('Wounding Word', [1, 68, 134], Effects(
            [['12-14', '15-17', '20-22']],
            [['14-16', '19-21', '24-26']],
            [AIR],
        ), is_linked=(1, 'Slighting Word')),
        Spell('Slighting Word', [105,172], Effects(
            [['39-42','48-52']],
            [['46-50','58-62']],
            [AIR],
        ), is_linked=(2, 'Wounding Word')),
        Spell('Alternative Word', [1, 66, 132], Effects(
            [['14-16', '19-21', '24-27'],
             ['9-11', '13-15', '16-19']],
            [['17-19', '22-25', '29-32'],
             ['11-14', '15-18', '19-23']],
            [FIRE, FIRE],
            heals=[True, False],
        ), aggregates=[('Allies', [0]),
                       ('Enemies', [1])],
        is_linked=(1, 'Striking Word')),
        Spell('Striking Word', [95, 162], Effects(
            [['24-27','30-34']],
            [['29-33','36-41']],
            [FIRE],
        ), is_linked=(2, 'Alternative Word')),
        Spell('Forbidden Word', [3, 69, 136], Effects(
            [['10-12', '13-15', '17-19']],
            [['12-14', '16-18', '20-23']],
            [WATER],
        ), is_linked=(1, 'Taboo Word')),
        Spell('Taboo Word', [110, 177], Effects(
            [['27-31','34-38']],
            [['33-37','41-46']],
            [WATER],
        ), is_linked=(2, 'Forbidden Word')),
        Spell('Seductive Word', [115, 182], Effects(
            [['19-22','22-26']],
            [['22-27','26-31']],
            [EARTH],
        )),
        Spell('Self-Sacrificing Word', [120, 187], Effects(
            [['220', '250']],
            None,
            ['buff_pow']
        )),
        Spell('Brutal Word', [15, 82, 149], Effects(
            [['12-14', '16-18', '20-22']],
            [['15-17', '19-21', '24-26']],
            [EARTH],
        ), is_linked=(1, 'Pernicious Word')),
        Spell('Pernicious Word', [125, 192], Effects(
            [['8-10', '9-11'],
             ['24-28', '28-32']],
            [['9-12', '11-13'],
             ['29-33', '34-38']],
            [EARTH, EARTH],
        ), aggregates=[('Target', [0]),
                       ('Enemies around target', [1])]
        , is_linked=(2, 'Brutal Word')),
        Spell('Defensive Word', [130, 197], Effects(
            [['34-38','38-42']],
            [['41-45','46-50']],
            [EARTH],
        )),
        Spell('Selective Word', [25, 92, 159], Effects(
            [['14-16', '18-20', '23-25'],
             ['9-11', '12-14', '15-17']],
            [['17-19', '22-24', '28-30'],
             ['11-13', '14-16', '18-20']],
            [FIRE, FIRE],
            heals=[True, False],
        ), aggregates=[('Allies', [0]),
                       ('Enemies', [1])],
        is_linked=(1, 'Impartial Word')),
        Spell('Impartial Word', [135], Effects(
            [['38-42'],
             ['46-50']],
            [['46-50'],
             ['55-60']],
            [FIRE, FIRE],
            heals=[False, True],
        ), aggregates=[('Enemy or around ally', [0]),
                       ('Ally or around enemy', [1])],
        is_linked=(2, 'Selective Word')),     
        Spell('Blaring Word', [30, 97, 164], Effects(
            [['17-19', '22-24', '27-30']],
            [['20-23', '26-29', '32-36']],
            [WATER],
        ), is_linked=(1, 'Resounding Word')),
        Spell('Resounding Word', [140], Effects(
            [['23-25']],
            [['28-30']],
            [WATER],
        ), is_linked=(2, 'Blaring Word')),
        Spell('Secret Word', [140], Effects(
            [['8-10','11-13','14-16']],
            [['10-12','13-15','17-19']],
            [EARTH],
        ), is_linked=(1, 'Agonising Word')),
        Spell('Agonising Word', [150], Effects(
            [['7-9'],
             ['22-26']],
            [['8-11'],
             ['26-31']],
            [EARTH, EARTH],
        ), aggregates=[('Target', [0]),
                       ('Enemies around target', [1])]
        , is_linked=(2, 'Secret Word')),
        Spell('Turbulent Word', [45, 112, 179], Effects(
            [['16-18', '21-23', '26-28']],
            [['19-21', '26-28', '31-34']],
            [AIR],
            steals=[True],
        ), is_linked=(1, 'Mischievous Word')),
        Spell('Mischievous Word', [155], Effects(
            [['17-19']],
            [['20-23']],
            [AIR],
        ), is_linked=(2, 'Turbulent Word')),
        Spell('Puzzling Word', [55, 122, 189], Effects(
            [['28-31', '37-41', '42-47'],
             ['20-24', '27-31', '31-36']],
            [['33-37', '44-49', '50-56'],
             ['24-28', '32-38', '37-43']],
            [FIRE, FIRE],
            heals=[True, False],
        ), aggregates=[('Allies', [0]),
                       ('Enemies', [1])],
        is_linked=(1, 'Furious Word')),
        Spell('Furious Word', [165], Effects(
            [['14-16'],
             ['42-48']],
            [['17-19'],
             ['50-58']],
            [EARTH, EARTH],
        ), aggregates=[('Target', [0]),
                       ('Enemies around target', [1])], 
        is_linked=(2, 'Puzzling Word')),  
        Spell('Whirling Word', [60, 127, 194], Effects(
            [['20-22', '24-28', '27-31']],
            [['23-27', '29-33', '32-37']],
            [AIR],
        ), is_linked=(1, 'Whirlwind Word')),
        Spell('Whirlwind Word', [170], Effects(
            [['30-34']],
            [['36-41']],
            [AIR],
            steals=[True],
        ), is_linked=(2, 'Whirling Word')), 
        Spell('Thunderous Word', [65, 131, 198], Effects(
            [['31-35', '38-42', '42-47']],
            [['38-42', '45-51', '50-56']],
            [WATER],
        ), is_linked=(1, 'Overwhelming Word')), 
        Spell('Overwhelming Word', [175], Effects(
            [['36-40']],
            [['43-48']],
            [WATER],
        ), is_linked=(2, 'Thunderous Word')), 
    ],
    'Enutrof': [
        Spell('Coins Throwing', [1, 20, 40], Effects(
            [['7-9', '9-11', '11-13']],
            [['10', '12', '14']],
            [WATER],
        ), is_linked=(1, 'Hard Cash')), 
        Spell('Hard Cash', [101], Effects(
            [['19-23']],
            [['22-26']],
            [WATER],
            steals=[True],
        ), is_linked=(2, 'Coins Throwing')), 
        Spell('Shovel Throwing', [1, 25, 52], Effects(
            [['25-31', '31-37', '37-43']],
            [['30-36', '36-42', '42-48']],
            [EARTH],
        ), is_linked=(1, 'Spade Throw')), 
        Spell('Spade Throw', [105], Effects(
            [['26-30']],
            [['30-34']],
            [EARTH],
        ), is_linked=(2, 'Shovel Throwing')), 
        Spell('Ghostly Shovel', [3, 35, 67], Effects(
            [['16-18', '21-23', '26-28']],
            [['19-21', '24-26', '29-31']],
            [FIRE],
        ), is_linked=(1, 'Ghostly Spade')), 
        Spell('Ghostly Spade', [115], Effects(
            [['30-34']],
            [['35-39']],
            [AIR],
        ), is_linked=(2, 'Ghostly Shovel')), 
        Spell('Mound', [13, 54, 94], Effects(
            [['12-15', '15-18', '18-21']],
            [['18', '21', '24']],
            [EARTH],
        ), is_linked=(1, 'Peat Bog')), 
        Spell('Peat Bog', [130], Effects(
            [['48-54']],
            [['58-64']],
            [EARTH],
        ), is_linked=(2, 'Mound')), 
        Spell('Prime of Life', [22, 65, 108], Effects(
            [['28-32', '33-37', '38-42']],
            [['33-37', '38-42', '43-47']],
            [EARTH],
        ), is_linked=(1, 'Obsolescence')), 
        Spell('Obsolescence', [140], Effects(
            [['19-23']],
            [['22-26']],
            [EARTH],
        ), is_linked=(2, 'Prime of Life')), 
        Spell('Greed', [32, 81, 124], Effects(
            [['50', '100', '150']],
            [['60', '110', '160']],
            ['buff_pow']
        )),
        Spell('Shovel Kiss', [38, 90, 132], Effects(
            [['9-11', '12-14', '15-17']],
            [['13', '16', '19']],
            [FIRE],
        ), is_linked=(1, 'Spade Kiss')), 
        Spell('Spade Kiss', [155], Effects(
            [['14-16']],
            None,
            [FIRE],
        ), is_linked=(2, 'Shovel Kiss')), 
        Spell('Loafylactic', [165], Effects(
            [['17-19']],
            [['19-21']],
            [AIR],
        )), 
        Spell('Fortune', [56, 112, 147], Effects(
            [['100', '200', '300']],
            None,
            ['buff_pow']
        ), is_linked=(1, 'Opportuneness')), 
        Spell('Opportuneness', [170], Effects(
            [['11-13'],
             ['75']],
            [['12-14'],
             ['80']],
            [AIR, 'buff_pow'],
        ), stacks=2, is_linked=(2, 'Fortune')), 
        Spell('Shovel of Judgement', [62, 116, 153], Effects(
            [['18-22', '21-25', '24-28']],
            [['22-26', '25-29', '28-32']],
            [WATER],
        ), is_linked=(1, 'Spade of Judgement')), 
        Spell('Spade of Judgement', [175], Effects(
            [['38-42']],
            [['46-50']],
            [AIR],
        ), is_linked=(2, 'Shovel of Judgement')), 
        Spell('Slaughtering Shovel', [69, 122, 162], Effects(
            [['32-37', '39-44', '46-51']],
            [['39-44', '46-51', '53-58']],
            [WATER],
        ), is_linked=(1, 'Carnivore Spade')), 
        Spell('Carnivore Spade', [180], Effects(
            [['16-18']],
            None,
            [WATER],
            steals=[True],
        ), is_linked=(2, 'Slaughtering Shovel')), 
        Spell('Unsummoning', [92, 141, 187], Effects(
            [['27-30', '33-36', '39-42']] * 3,
            [['32-35', '38-41', '44-47']] * 3,
            [FIRE, FIRE, FIRE],
        ), aggregates=[('Non-summons', [0]),
                       ('Summons', [1, 2])],
        is_linked=(1, 'Correction')), 
        Spell('Correction', [195], Effects(
            [['48-52']],
            [['58-62']],
            [FIRE],
        ), is_linked=(2, 'Unsummoning')), 
    ],
    'Feca': [
        Spell('Natural Attack', [1, 67, 133], Effects(
            [['10-12', '14-16', '18-20'],
             ['20', '40', '60']],
            [['13-15', '17-19', '22-24'],
             ['30', '50', '70']],
            [FIRE, 'buff_int'],
        ), stacks=3,
        is_linked=(1, 'Natural Attraction')), 
        Spell('Natural Attraction', [100, 167], Effects(
            [['24-27', '30-34']],
            [['29-33', '36-41']],
            [FIRE],
        ), is_linked=(2, 'Natural Attack')), 
        Spell('Blindness', [1, 68, 134], Effects(
            [['12-14', '15-17', '20-22']],
            [['14-16', '19-21', '24-26']],
            [NEUTRAL],
        ), is_linked=(1, 'Dazzling')), 
        Spell('Dazzling', [105, 172], Effects(
            [['34-39', '42-48']],
            [['40-46', '50-58']],
            [EARTH],
        ), is_linked=(2, 'Blindness')), 
        Spell('Typhoon', [3, 69, 136], Effects(
            [['13-15', '17-19', '22-24'],
             ['20', '40', '60']],
            [['15-17', '20-22', '26-29'],
             ['30', '50', '70']],
            [AIR, 'buff_agi'],
        ), stacks=3, is_linked=(1, 'Gust')), 
        Spell('Gust', [110, 177], Effects(
            [['21-23', '26-28']],
            [['25-27', '31-34']],
            [AIR],
        ), is_linked=(2, 'Typhoon')), 
        Spell('Bubble', [6, 71, 138], Effects(
            [['9-11', '12-14', '15-17']],
            [['10-12', '14-16', '18-20']],
            [WATER],
        ), is_linked=(1, 'Swelling')), 
        Spell('Swelling', [115, 182], Effects(
            [['32-36', '38-42']],
            [['39-43', '46-50']],
            [AIR],
        ), is_linked=(2, 'Bubble')), 
        #TODO: find out Aggressive Glyph's damages
        Spell('Aggressive Glyph', [15, 82, 149], Effects(
            [['24-26', '28-30', '32-34']],
            None,
            [AIR],
        ), special='glyph', is_linked=(1, 'Fulminating Glyph')), 
        Spell('Fulminating Glyph', [125, 192], Effects(
            [['27-31', '31-35']],
            [['32-37', '37-42']],
            [AIR],
        ), special='glyph', is_linked=(2, 'Aggressive Glyph')), 
        Spell('Lethargy', [20, 87, 154], Effects(
            [['23-25', '29-32', '36-40']],
            [['27-30', '35-39', '43-48']],
            [FIRE],
        ), is_linked=(1, 'Lifelessness')), 
        Spell('Lifelessness', [130, 197], Effects(
            [['34-38', '38-42'],
             ['120', '150']],
            [['41-45', '46-50'],
             ['140', '170']],
            [FIRE, 'buff_int'],
        ), stacks=2, is_linked=(2, 'Lethargy')),
        Spell('Cloudy Attack', [25, 92, 159], Effects(
            [['19-21', '25-27', '31-33'],
             ['40', '60', '80']],
            [['23-25', '30-32', '37-40'],
             ['60', '80', '100']],
            [WATER, 'buff_cha'],
        ), stacks=2, is_linked=(1, 'Stormy Attack')),
        Spell('Stormy Attack', [135], Effects(
            [['38-42']],
            [['46-50']],
            [WATER],
        ), is_linked=(2, 'Cloudy Attack')),
        Spell('Bastion', [30, 97, 164], Effects(
            [['80', '120', '150']],
            None,
            ['buff_pow'],
        ), stacks=2),
        Spell('Backlash', [35, 102, 169], Effects(
            [['18-21', '23-27', '29-33'],
             ['40', '60', '80']],
            [['22-25', '28-32', '35-40'],
             ['60', '80', '100']],
            [EARTH, 'buff_str'],
        ), stacks=2, is_linked=(1, 'Tetany')),
        Spell('Tetany', [145], Effects(
            [['34-38']],
            [['41-46']],
            [NEUTRAL],
        ), is_linked=(2, 'Backlash')),
        #TODO: find out Repulsion Glyph's damages
        Spell('Repulsion Glyph', [45, 112, 179], Effects(
            [['11-12', '16-17', '21-22']] * 4,
            None,
            [FIRE, WATER, EARTH, AIR],
        ), aggregates=[('', [0, 1, 2, 3])], special='glyph',
        is_linked=(1, 'Barrier')),
        Spell('Barrier', [155], Effects(
            [['21-22']] * 4,
            None,
            [FIRE, WATER, EARTH, AIR],
        ), aggregates=[('', [0, 1, 2, 3])], special='glyph',
        is_linked=(2, 'Repulsion Glyph')),
        #TODO: find out Blinding Glyph's damages
        Spell('Blinding Glyph', [55, 122, 189], Effects(
            [['21-24', '26-29', '31-34']],
            None,
            [EARTH],
        ), special='glyph', is_linked=(1, 'Protective Glyph')),
        Spell('Protective Glyph', [165], Effects(
            [['31-35']],
            [['37-42']],
            [EARTH],
        ), special='glyph', is_linked=(2, 'Blinding Glyph')),
        Spell('Shiver', [60, 127, 194], Effects(
            [['22-25', '27-30', '30-34']],
            [['26-30', '32-36', '36-41']],
            [AIR],
        ), is_linked=(1, 'Tension')),
        Spell('Tension', [170], Effects(
            [['38-42']],
            [['46-50']],
            [WATER],
        ), is_linked=(2, 'Shiver')),
        #TODO: find out Paralysing Glyph's damages
        Spell('Paralysing Glyph', [65, 131, 198], Effects(
            [['21-23', '26-28', '31-33']],
            None,
            [WATER],
        ), special='glyph', is_linked=(1, 'Roaming Glyph')),
        Spell('Roaming Glyph', [175], Effects(
            [['30-34']],
            [['36-41']],
            [WATER],
        ), special='glyph', is_linked=(2, 'Paralysing Glyph')),
        Spell('Torpor', [70, 137], Effects(
            [['21-23', '27-30']],
            [['25-28', '32-36']],
            [EARTH],
        ), is_linked=(1, 'Lateral Flame')),
        Spell('Lateral Flame', [180], Effects(
            [['31-35']],
            [['37-42']],
            [FIRE],
        ), is_linked=(2, 'Torpor')),
        Spell('Reinforced Protection', [75, 142], Effects(
            [['120', '200'],
             ['160', '250']],
            None,
            ['buff_pow_nonglyph', 'buff_pow_glyph'],
        )),
        #TODO: find out Burning Glyph's damages
        Spell('Burning Glyph', [85, 152], Effects(
            [['23-27', '28-32']],
            None,
            [FIRE],
        ), special='glyph', is_linked=(1, 'Perception Glyph')),
        Spell('Perception Glyph', [195], Effects(
            [['37-41']],
            [['44-49']],
            [FIRE],
        ), special='glyph', is_linked=(2, 'Burning Glyph')),
    ],
    'Foggernaut': [
        Spell('Anchor', [1, 25, 52], Effects(
            [['12-14', '16-18', '20-22']],
            [['16-18', '20-22', '24-26']],
            [EARTH],
        ), is_linked=(1, 'Mooring')),
        Spell('Mooring', [105], Effects(
            [['17-21']],
            [['21-25']],
            [EARTH],
        ), is_linked=(2, 'Anchor')),
        Spell('Pilfer', [1, 30, 60], Effects(
            [['11-13', '14-16', '17-19']],
            [['14-16', '17-19', '20-22']],
            [FIRE],
            steals=[True],
        ), is_linked=(1, 'Scuttle')),
        Spell('Scuttle', [110], Effects(
            [['47-53']],
            [['52-58']],
            [FIRE],
        ), is_linked=(2, 'Pilfer')),
        Spell('Torrent', [6, 42, 74], Effects(
            [['15-19', '19-23', '23-27']],
            [['18-22', '22-26', '26-30']],
            [WATER],
        ), is_linked=(1, 'Harmattan')),
        Spell('Harmattan', [120], Effects(
            [['28-32']],
            [['34-38']],
            [AIR],
        ), is_linked=(2, 'Torrent')),
        Spell('Scaphander', [13, 54, 94], Effects(
            [['12', '19', '25'],
             ['28', '34', '40']],
            [['16', '23', '30'],
             ['32', '36', '50']],
            ['buff_dam', 'buff_pshdam']
        )),
        Spell('Backwash', [22, 65, 108], Effects(
            [['13-17', '17-21', '21-25']],
            [['16-20', '20-24', '24-28']],
            [EARTH],
        ), is_linked=(1, 'Torpedo')),
        Spell('Torpedo', [140], Effects(
            [['25-29']],
            [['29-33']],
            [AIR],
        ), is_linked=(2, 'Backwash')),
        Spell('Tide', [27, 72, 118], Effects(
            [['20-24', '24-28', '28-32']],
            [['26-30', '30-34', '34-38']],
            [AIR],
        ), is_linked=(1, 'Corrosion')),
        Spell('Corrosion', [145], Effects(
            [['34-38']],
            [['39-43']],
            [AIR],
        ), is_linked=(2, 'Tide')),
        Spell('Vapour', [32, 81, 124], Effects(
            [['23-27', '27-31', '31-35']],
            [['28-32', '32-36', '36-40']],
            [FIRE],
        ), is_linked=(1, 'Valve')),
        Spell('Valve', [150], Effects(
            [['16-18'],
             ['30']],
            [['19-21'],
             ['30']],
            [FIRE, 'buff_heals'],
        ), is_linked=(2, 'Vapour')),
        Spell('Periscope 1', [50, 103, 143], Effects(
            [['21-25', '26-30', '31-35']],
            [['25-29', '30-34', '35-39']],
            [WATER],
        ), is_linked=(1, 'Periscope 2')),
        Spell('Periscope 2', [165], Effects(
            [['30-34']],
            [['36-40']],
            [WATER],
        ), is_linked=(2, 'Periscope 1')),
        Spell('First Aid', [56, 112, 147], Effects(
            [['19-23', '24-28', '29-33']],
            [['25-29', '30-34', '35-39']],
            [FIRE],
            heals=[True]
        ), is_linked=(1, 'Rescue')),
        Spell('Rescue', [170], Effects(
            [['19-21']],
            [['23-25']],
            [FIRE],
            heals=[True]
        ), is_linked=(2, 'First Aid')),
        Spell('Surge', [62, 116, 153], Effects(
            [['20-24', '25-29', '30-34']],
            [['25-29', '30-34', '35-39']],
            [FIRE],
        ), is_linked=(1, 'Short-Circuit')),
        Spell('Short-Circuit', [175], Effects(
            [['38-42']],
            None,
            [AIR],
        ), is_linked=(2, 'Surge')),
        Spell('Ambush ', [69, 122, 162], Effects(
            [['8-10', '11-13', '14-16']] * 4,
            [['11-13', '14-16', '17-19']] * 4,
            [FIRE, WATER, EARTH, AIR],
         ), aggregates=[('', [0, 1, 2, 3])]),
        Spell('Froth', [84, 134, 178], Effects(
            [['28-32', '33-37', '38-42']],
            [['33-37', '38-42', '43-47']],
            [WATER],
        ), is_linked=(1, 'Nautilus')),
        Spell('Nautilus', [190], Effects(
            [['23-27']],
            [['28-32']],
            [WATER],
        ), is_linked=(2, 'Froth')),
        Spell('Trident', [92, 141, 187], Effects(
            [['21-25', '26-30', '31-35'],
             ['7-8', '9-10', '11-12']],
            [['26-30', '31-35', '36-40'],
             ['7-8', '9-10', '11-12']],
            [EARTH, EARTH],
         ), aggregates=[('Hit', [0]),
                        ('Pushback Poison', [1])],
        is_linked=(1, 'Seizing')),
        Spell('Seizing', [195], Effects(
            [['30-34']],
            [['35-39']],
            [EARTH],
        ), is_linked=(2, 'Trident')),
    ],
    'Iop': [
        Spell('Intimidation', [1, 67, 133], Effects(
            [['6-8', '8-10', '11-13']],
            [['8-10', '10-12', '13-16']],
            [NEUTRAL],
        )),
        Spell('Pressure', [1, 68, 134], Effects(
            [['14-18', '19-22', '24-28']],
            [['17-20', '22-26', '29-34']],
            [EARTH],
        ), is_linked=(1, 'Pounding')),
        Spell('Pounding', [105, 172], Effects(
            [['24-27','30-34']],
            [['29-33','36-41']],
            [AIR],
        ), is_linked=(2, 'Pressure')),
        Spell('Outpouring', [3, 39, 136], Effects(
            [['23-25', '30-33', '38-42']],
            [['27-30', '36-39', '46-50']],
            [WATER],
        ), is_linked=(1, 'Threat')),
        Spell('Threat', [110, 177], Effects(
            [['21-23', '26-28']],
            [['25-27', '31-34']],
            [WATER],
        ), is_linked=(2, 'Outpouring')),
        Spell('Divine Sword', [6, 71, 138], Effects(
            [['12-14', '17-19', '21-23'],
             ['10', '15', '20']],
            [['15-17', '20-22', '25-28'],
             ['13', '18', '23']],
            [AIR, 'buff_dam'],
        ), is_linked=(1, 'Cleaver')),
        Spell('Cleaver', [115, 182], Effects(
            [['40-45', '47-53']],
            [['48-54', '56-54']],
            [WATER],
        ), is_linked=(2, 'Divine Sword')),
        Spell('Destructive Sword', [10, 77, 144], Effects(
            [['19-22', '26-29', '32-36']],
            [['23-26', '31-35', '38-43']],
            [FIRE],
        ), is_linked=(1, 'Destructive Ring')),
        Spell('Destructive Ring', [120, 187], Effects(
            [['23-26', '26-30']],
            [['27-31', '31-36']],
            [AIR],
        ), is_linked=(2, 'Destructive Sword')),
        Spell('Concentration', [25, 92, 159], Effects(
            [['19-21', '24-27', '30-34'],
             ['13-15', '16-19', '20-24']],
            [['23-26', '29-33', '36-41'],
             ['15-18', '19-23', '24-29']],
            [EARTH, EARTH],
        ), aggregates=[('Summons', [0]),
                        ('Others', [1])],
        is_linked=(1, 'Accumulation')),
        Spell('Accumulation', [135], Effects(
            create_stacking_values(((22, 26),), 20, 2),
            create_stacking_values(((26, 31),), 24, 2),
            [EARTH]*2,
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)],
        is_linked=(2, 'Concentration')),
        Spell('Chopper', [30, 97, 164], Effects(
            [['11-14', '14-18', '18-22']],
            [['14-17', '17-21', '22-26']],
            [FIRE],
        ), is_linked=(1, 'Fracture')),
        Spell('Fracture', [140], Effects(
            [['34-38']],
            [['41-46']],
            [AIR],
        ), is_linked=(2, 'Chopper')),
        Spell('Sword of Judgement', [45, 112, 179], Effects(
            [['12-14', '16-18', '19-21'],
             ['12-14', '16-18', '19-21']],
            [['14-16', '19-21', '23-25'],
             ['14-16', '19-21', '23-25']],
            [AIR, FIRE],
        ), aggregates=[('', [0, 1])],
        is_linked=(1, 'Condemnation')),
        Spell('Condemnation', [155], Effects(
            [['25-29'],
             ['25-29'],
             ['41-45']],
            None,
            [AIR, FIRE, FIRE],
        ), aggregates=[('', [0]),
                       ('When it is cast on another target', [1]),
                       ('If cast a second time on the first target', [2])],
        is_linked=(2, 'Sword of Judgement')),
        Spell('Power', [50, 117, 184], Effects(
            [['100', '200', '300']],
            [['120', '240', '350']],
            ['buff_pow']
        ), is_linked=(1, 'Virtue')),
        Spell('Virtue', [160], Effects(
            [['150']],
            None,
            ['buff_depow']
        ), is_linked=(2, 'Power')),
        Spell('Strengthstorm', [60, 127, 194], Effects(
            [['24-28', '30-34', '34-38']],
            [['30-33', '36-41', '41-46']],
            [FIRE],
        ), is_linked=(1, 'Tumult')),
        Spell('Tumult', [170], Effects(
            [['19-21']],
            [['23-25']],
            [FIRE],
        ), is_linked=(2, 'Strengthstorm')),
        Spell('Celestial Sword', [65, 131, 198], Effects(
            [['28-31', '31-35', '36-40']],
            [['34-37', '38-42', '43-48']],
            [AIR],
        ), is_linked=(1, 'Zenith')),
        Spell('Zenith', [175], Effects(
            [['86-94']],
            [['103-113']],
            [AIR],
        ), is_linked=(2, 'Celestial Sword')),
        Spell('Fervour', [70, 137], Effects(
            [['19-21','24-27']],
            [['22-25','29-32']],
            [WATER],
        ), is_linked=(1, 'Endurance')),
        Spell('Endurance', [180], Effects(
            [['34-38']],
            [['41-46']],
            [WATER],
        ), is_linked=(2, 'Fervour')),
        Spell('Sword of Iop', [80, 147], Effects(
            [['30-33', '37-41']],
            [['36-39', '44-49']],
            [EARTH],
        ), is_linked=(1, 'Pygmachia')),
        Spell('Pygmachia', [190], Effects(
            create_stacking_values(((9, 11),), 15, 2),
            create_stacking_values(((11, 13),), 18, 2),
            [EARTH]*2,
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)],
        is_linked=(2, 'Sword of Iop')),
        Spell('Sword of Fate', [85, 152], Effects(
            [['31-34', '38-42'],
             ['61-64', '78-82']],
            [['37-40', '46-50'],
             ['72-75', '91-95']],
            [FIRE, FIRE],
         ), aggregates=[('Not Charged', [0]),
                        ('Charged', [1])],
        is_linked=(1, 'Sentence')),
        Spell('Sentence', [195], Effects(
            [['13-16'],
             ['28-32']],
            [['16-19'],
             ['28-32']],
            [FIRE, FIRE],
        ), aggregates=[('Target', [0]),
                        ('Enemies near target', [1])]
        , is_linked=(2, 'Sword of Fate')),
        Spell('Iop\'s Wrath', [90, 157], Effects(
            [['65-80', '81-100'],
             ['155-170', '191-210']],
            [['78-96', '97-120'],
             ['178-196', '217-230']],
            [EARTH, EARTH],
        ), aggregates=[('Not Charged', [0]),
                        ('Charged', [1])],
        is_linked=(1, 'Fit of Rage')),
        Spell('Fit of Rage', [200], Effects(
            [['28-32'],
             ['58-62']],
            [['34-38'],
             ['70-74']],
            [EARTH, EARTH],
        ), aggregates=[('Not Charged', [0]),
                        ('Charged', [1])],
        is_linked=(2, 'Iop\'s Wrath')),
    ],
    'Masqueraider': [
        Spell('Picada', [1, 25, 52], Effects(
            [['13-15', '16-18', '20-22']],
            [['18-20', '21-23', '24-26']],
            [AIR],
        ), is_linked=(1, 'Agular')),
        Spell('Agular', [105], Effects(
            [['30-34']],
            [['36-40']],
            [AIR],
        ), is_linked=(2, 'Picada')),
        Spell('Martelo', [1, 30, 60], Effects(
            [['16-18', '19-21', '22-24']],
            [['18-20', '21-23', '24-26']],
            [EARTH],
            steals=[True],
        ), is_linked=(1, 'Parafuso')),
        Spell('Parafuso', [110], Effects(
            [['22-26']],
            [['26-30']],
            [FIRE],
            steals=[True],
        ), is_linked=(2, 'Martelo')),
        Spell('Reinforcement', [6, 42, 74], Effects(
            [['6-7', '7-8', '8-9']] * 4,
            [['8-9', '9-10', '10-11']] * 4,
            [AIR, WATER, EARTH, FIRE],
         ), aggregates=[('', [0, 1, 2, 3])]),
        Spell('Retention', [17, 58, 102], Effects(
            [['16-18', '19-21', '22-24']],
            [['20-22', '23-25', '26-28']],
            [AIR],
            steals=[True],
        ), is_linked=(1, 'Estrelia')),
        Spell('Estrelia', [135], Effects(
            [['38-42']],
            [['44-48']],
            [WATER],
            steals=[True],
        ), is_linked=(2, 'Retention')),
        Spell('Furia', [27, 72, 118], Effects(
            [['27-31', '31-35', '35-39'],
             ['20', '30', '40']],
            [['29-33', '33-37', '37-41'],
             ['22', '33', '44']],
            [EARTH, 'buff_dam'],
        ), is_linked=(1, 'Cavalcade')),
        Spell('Cavalcade', [145], Effects(
            [['38-42']],
            [['44-48']],
            [AIR],
        ), is_linked=(2, 'Furia')),
        Spell('Distance', [32, 81, 124], Effects(
            [['15-17', '19-21', '23-25']],
            [['19-21', '23-25', '27-29']],
            [WATER],
        ), is_linked=(1, 'Atabak')),
        Spell('Atabak', [150], Effects(
            [['33-37']],
            [['37-41']],
            [EARTH],
        ), is_linked=(2, 'Distance')),
        Spell('Ginga', [155], Effects(
            [['250']],
            None,
            ['buff_pow'],
        )),
        Spell('Neurosis', [160], Effects(
            [['150']],
            None,
            ['buff_pow'],
        )),
        Spell('Capering', [56, 112, 147], Effects(
            [['22-26', '25-29', '28-32']],
            [['25-29', '28-32', '31-35']],
            [AIR],
        ), is_linked=(1, 'Bocciara')),
        Spell('Bocciara', [170], Effects(
            [['14-16'],
             ['80']],
            [['16-18'],
             ['80']],
            [WATER, 'buff_pshdam'],
        ), is_linked=(2, 'Capering')),
        Spell('Decoy', [62, 116, 153], Effects(
            [['14-18', '18-22', '22-26']],
            [['19-23', '23-27', '27-31']],
            [WATER],
            steals=[True],
        ), is_linked=(1, 'Catalepsy')),
        Spell('Catalepsy', [175], Effects(
            [['23-25']],
            [['26-28']],
            [EARTH],
            steals=[True],
        ), is_linked=(2, 'Decoy')),
        Spell('Apostasy', [77, 128, 172], Effects(
            [['16-20', '19-23', '22-26']],
            [['19-23', '22-26', '25-29']],
            [FIRE],
        ), is_linked=(1, 'Brincaderia')),
        Spell('Brincaderia', [185], Effects(
            [['13-15']],
            [['16-18']],
            [FIRE],
        ), is_linked=(2, 'Apostasy')),
        Spell('Apathy', [84, 134, 178], Effects(
            [['17-21', '21-25', '25-29']],
            [['20-24', '24-28', '28-32']],
            [EARTH],
        ), is_linked=(1, 'Ponteira')),
        Spell('Ponteira', [190], Effects(
            [['17-19']],
            [['20-22']],
            [WATER],
        ), is_linked=(2, 'Apathy')),
        Spell('Boliche', [92, 141, 187], Effects(
            [['17-19', '20-22', '26-28']],
            [['20-22', '23-25', '29-31']],
            [WATER],
        ), is_linked=(1, 'Inferno')),
        Spell('Inferno', [195], Effects(
            [['38-42'],
             ['200']],
            [['42-46'],
             ['220']],
            [FIRE, 'buff_pow'],
        ), is_linked=(2, 'Boliche')),
    ],
    'Osamodas': [
        Spell('Canine', [1, 25, 52], Effects(
            [['14-17', '17-20', '20-23']],
            [['17-20', '20-23', '23-26']],
            [AIR],
        ), is_linked=(1, 'Repulsive Fang')),
        Spell('Repulsive Fang', [105], Effects(
            [['38-42']],
            [['46-50']],
            [AIR],
        ), is_linked=(2, 'Canine')),
        Spell('Dragonic', [1, 30, 60], Effects(
            [['15-17', '19-21', '23-25']],
            [['20-22', '24-26', '26-30']],
            [FIRE],
        ), is_linked=(1, 'Aquatic Wave')),
        Spell('Aquatic Wave', [110], Effects(
            [['28-32']],
            [['31-35']],
            [WATER],
        ), is_linked=(2, 'Dragonic')),
        Spell('Fossil', [6, 42, 74], Effects(
            [['16-20', '19-23', '22-26']],
            [['21-25', '24-28', '27-31']],
            [EARTH],
        ), is_linked=(1, 'Sedimentation')),
        Spell('Sedimentation', [120], Effects(
            [['38-42']],
            [['44-48']],
            [EARTH],
        ), is_linked=(2, 'Aquatic Wave')),
        Spell('Takeoff', [135], Effects(
            [['30']],
            None,
            [AIR],
        )),
        Spell('Whip', [22, 65, 108], Effects(
            ([['7-8', '9-10', '11-12']] * 4
             + [['11', '18', '25']]),
            ([['9-10', '11-12', '13-14']] * 4
             + [['12', '20', '28']]),
            [AIR, EARTH, WATER, FIRE, FIRE],
            heals=[False, False, False, False, True],
        ), aggregates=[('Tofu', [0]),
                       ('Gobball', [1]),
                       ('Toad', [2]),
                       ('Wyrmling (enemies)', [3]),
                       ('Wyrmling (allies)', [4])]
        ),
        Spell('Duster', [27, 72, 118], Effects(
            create_duster_values(((17, 19), (22, 24), (27, 29)), 6, 5),
            create_duster_values(((22, 24), (27, 29), (32, 34)), 6, 5),
            [AIR, AIR, AIR, AIR, AIR, AIR]
        ), aggregates=[('No Tofus', [0]),
                       ('One Tofu', [1]),
                       ('Two Tofus', [2]),
                       ('Three Tofus', [3]),
                       ('Four Tofus', [4]),
                       ('Five Tofus', [5])],
        is_linked=(1, 'Plucking')),
        Spell('Plucking', [145], Effects(
            [['38-42']],
            None,
            [AIR],
        ), is_linked=(2, 'Duster')),
        Spell('Dragon\'s Breath', [44, 97, 137], Effects(
            [['15-18', '21-24', '27-30']],
            [['20-23', '26-29', '32-35']],
            [FIRE],
        )),
        Spell('Crackler Punch', [56, 112, 147], Effects(
            [['23-27', '28-32', '33-37']],
            [['30-34', '35-39', '40-44']],
            [EARTH],
        ), is_linked=(1, 'Constriction')),
        Spell('Constriction', [170], Effects(
            [['25-29']],
            [['28-32']],
            [EARTH],
            steals=[True],
        ), is_linked=(2, 'Crackler Punch')),
        Spell('Geyser', [62, 116, 153], Effects(
            [['17-19', '20-22', '23-35'],
             ['70', '110', '150']],
            [['22-24', '25-27', '28-30'],
             ['70', '110', '150']],
            [WATER, 'buff_pow'],
        )),
        Spell('Whirlwind', [180], Effects(
            [['38-42']],
            [['44-48']],
            [WATER],
        )),
    ],
    'Pandawa': [
        Spell('Blazing Fist', [1, 25, 52], Effects(
            [['16-21', '19-24', '22-27']],
            [['21-26', '24-29', '27-32']],
            [FIRE],
        ), is_linked=(1, 'Burning Circle')),
        Spell('Burning Circle', [105], Effects(
            [['34-38']],
            [['39-43']],
            [FIRE],
        ), is_linked=(2, 'Blazing Fist')),
        Spell('Debauchery', [1, 30, 60], Effects(
            [['16-20', '19-23', '22-26']],
            [['19-23', '22-26', '25-29']],
            [EARTH],
        ), is_linked=(1, 'Hangover')),
        Spell('Hangover', [110], Effects(
            create_stacking_values(((24, 28),), 5, 6),
            create_stacking_values(((29, 33),), 5, 6),
            [EARTH]*6,
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(6)],
        is_linked=(2, 'Debauchery')),
        Spell('Alcoholic Breath', [6, 42, 74], Effects(
            [['16-17', '20-21', '24-25']],
            [['20-21', '24-25', '28-29']],
            [AIR],
        ), is_linked=(1, 'Numbness')),
        Spell('Numbness', [120], Effects(
            [['38-42']],
            [['42-46']],
            [AIR],
        ), is_linked=(2, 'Alcoholic Breath')),
        Spell('Schnaps', [13, 54, 94], Effects(
            [['23-25', '29-31', '35-37']],
            [['27-29', '33-35', '39-41']],
            [AIR],
        ), is_linked=(1, 'Liqueur')),
        Spell('Liqueur', [130], Effects(
            [['19-23']],
            [['23-27']],
            [AIR],
            steals=[True],
        ), is_linked=(2, 'Schnaps')),
        Spell('Propulsion', [17, 58, 102], Effects(
            [['27-33', '37-43', '47-53']],
            [['32-38', '42-48', '52-58']],
            [FIRE],
        )),
        Spell('Eviction', [32, 81, 124], Effects(
            [['12-16', '15-19', '18-22']],
            [['15-19', '18-22', '21-25']],
            [EARTH],
        ), is_linked=(1, 'Nausea')),
        Spell('Nausea', [150], Effects(
            [['7-9']],
            [['9-11']],
            [AIR],
        ), is_linked=(2, 'Eviction')),
        Spell('Tipple', [38, 90, 132], Effects(
            [['16-20', '19-23', '22-26']],
            [['20-24', '23-27', '26-30']],
            [WATER],
        ), is_linked=(1, 'Distillation')),
        Spell('Distillation', [155], Effects(
            [['38-42']],
            [['42-46']],
            [WATER],
        ), is_linked=(2, 'Tipple')),
        Spell('Melancholy', [56, 112, 147], Effects(
            [['31-33', '36-38', '41-43']],
            [['37-39', '42-44', '47-49']],
            [WATER],
        ), is_linked=(1, 'Hooch')),
        Spell('Hooch', [170], Effects(
            [['53-57']],
            [['61-65']],
            [WATER],
        ), is_linked=(2, 'Melancholy')),
        Spell("Zatoishwan's Wrath", [62, 116, 153], Effects(
            [['100', '150', '200'],
             ['5', '10', '15']],
            None,
            ['buff_pow', 'buff_dam']
        )),
        Spell('Explosive Flask', [69, 122, 162], Effects(
            [['24-28', '29-33', '34-38']],
            [['29-33', '34-38', '39-43']],
            [FIRE],
        ), is_linked=(1, 'Absinthe')),
        Spell('Absinthe', [180], Effects(
            [['25-29']],
            [['30-34']],
            [FIRE],
        ), is_linked=(2, 'Explosive Flask')),
        Spell('Pandatak', [84, 134, 178], Effects(
            [['36-40', '42-46', '48-52']],
            [['43-47', '49-53', '55-59']],
            [EARTH],
        ), is_linked=(1, 'Filthipint')),
        Spell('Filthipint', [190], Effects(
            [['38-42']],
            [['42-46']],
            [EARTH],
            steals=[True],
        ), is_linked=(2, 'Pandatak')),
    ],
    'Rogue': [
        Spell('Explobomb', [1, 25, 52], Effects(
            [['12-13', '16-17', '20-22']],
            None,
            [FIRE],
        )),
        Spell('Extraction', [1, 30, 60], Effects(
            [['16-18', '21-23', '26-28']],
            [['19-21', '24-26', '29-31']],
            [FIRE],
            steals=[True],
        ), is_linked=(1, 'Obliteration')),
        Spell('Obliteration', [110], Effects(
            [['37-43']],
            [['41-47']],
            [FIRE],
        ), is_linked=(2, 'Extraction')),
        Spell('Musket', [120], Effects(
            [['19-21']],
            [['23-25']],
            [EARTH],
        )),
        Spell('Grenado', [9, 47, 87], Effects(
            [['9-10', '13-14', '17-19']],
            None,
            [AIR],
        )),
        Spell('Boomerang Daggers', [17, 58, 102], Effects(
            [['15-17', '19-21', '23-25']],
            [['7-9', '9-11', '11-13']] * 2,
            [AIR, AIR],
        ), aggregates=[('', [0, 1])],
        is_linked=(1, 'Cadence')),
        Spell('Cadence', [135], Effects(
            [['17-19']],
            [['21-23']],
            [AIR],
        ), is_linked=(2, 'Boomerang Daggers')),
        Spell('Deception', [27, 72, 118], Effects(
            [['25-29', '30-34', '35-39']],
            [['29-33', '34-38', '39-43']],
            [WATER],
        ), is_linked=(1, 'Stolen Goods')),
        Spell('Stolen Goods', [145], Effects(
            [['22-26']],
            [['27-31']],
            [WATER],
        ), is_linked=(2, 'Deception')),
        Spell('Water Bomb', [32, 81, 124], Effects(
            [['9-10', '13-14', '17-19']],
            None,
            [WATER],
        )),
        Spell('Pulsar', [38, 90, 132], Effects(
            [['38-42', '47-51', '56-60']],
            [['44-48', '55-59', '66-70']],
            [FIRE],
        ), is_linked=(1, 'Gluing Explobomb')),
        Spell('Gluing Explobomb', [155], Effects(
            [['30-34']],
            None,
            [FIRE],
        ), is_linked=(2, 'Pulsar')),
        Spell('Arquebus', [165], Effects(
            [['43-47']],
            [['46-50']],
            [EARTH],
        )),
        Spell('Carbine', [56, 112, 147], Effects(
            [['17-19', '22-24', '27-29']],
            [['21-23', '26-28', '31-33']],
            [AIR],
        ), is_linked=(1, 'Machine Gun')),
        Spell('Machine Gun', [170], Effects(
            [['43-47']],
            [['48-52']],
            [AIR],
        ), is_linked=(2, 'Carbine')),
        Spell('Last Breath', [62, 116, 153], Effects(
            [['70', '110', '150']],
            [['90', '130', '170']],
            ['buff_pow']
        )),
        Spell('Seismobomb', [69, 122, 162], Effects(
            [['9-10', '13-14', '17-18']],
            None,
            [EARTH],
        )),
        Spell('Blunderbuss', [92, 141, 187], Effects(
            [['31-35', '35-39', '39-43']],
            [['35-39', '39-43', '43-47']],
            [WATER],
        ), is_linked=(1, 'Weigh Down')),
        Spell('Weigh Down', [195], Effects(
            [['48']],
            None,
            [EARTH],
        ), is_linked=(2, 'Blunderbuss'))
    ],
    'Sacrier': [
        Spell('Hemorrhage', [1, 66, 132], Effects(
            [['14-17', '19-22', '24-28']],
            [['17-20', '22-26', '29-34']],
            [AIR],
            steals=[True],
        ), is_linked=(1, 'Desolation')),
        Spell('Desolation', [95, 162], Effects(
            [['23-26', '28-32']],
            [['27-31', '34-38']],
            [AIR],
            steals=[True],
        ), is_linked=(2, 'Hemorrhage')), 
        Spell('Nervousness', [1, 67, 133], Effects(
            create_level_based_stacking_values(((13, 15), (16, 20), (21, 25)), 
                                               (15, 15, 15), 2),
            create_level_based_stacking_values(((15, 18), (20, 23), (55, 30)), 
                                               (15, 15, 15), 2),
            [[WATER]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)],
        is_linked=(1, 'Clobbering')),
        Spell('Clobbering', [100, 167], Effects(
            create_level_based_stacking_values(((26, 29), (32, 36)), 
                                               (20, 20), 2),
            create_level_based_stacking_values(((31, 35), (38, 43)), 
                                               (20, 20), 2),
            [[WATER]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(2, 'Nervousness')),
        Spell('Blood Bath', [3, 69, 136], Effects(
            [['17-20', '23-27', '29-34']],
            [['21-24', '27-32', '34-41']],
            [EARTH],
            steals=[True],
        ), is_linked=(1, 'Torture')),
        Spell('Torture', [110, 177], Effects(
            [['18-21', '22-26']],
            [['21-25', '26-31']],
            [EARTH],
            steals=[True],
        ), is_linked=(2, 'Blood Bath')),
        Spell('Excruciating Pain', [6, 71, 138], Effects(
            create_level_based_stacking_values(((13, 15), (17, 20), (21, 25)), 
                                               (15, 15, 15), 2),
            create_level_based_stacking_values(((15, 18), (20, 24), (25, 30)), 
                                               (15, 15, 15), 2),
            [[FIRE]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(1, 'Immolation')),
        Spell('Immolation', [115, 182], Effects(
            create_level_based_stacking_values(((28, 32), (33, 37)), 
                                               (20, 20), 2),
            create_level_based_stacking_values(((34, 38), (40, 44)), 
                                               (20, 20), 2),
            [[FIRE]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(2, 'Excruciating Pain')),   
        Spell('Mutilation', [10, 77, 144], Effects(
            [['50', '100', '150']],
            None,
            ['buff_pow']
        )),
        Spell('Ravages', [20, 87, 154], Effects(
            [['16-19', '21-24', '26-30']],
            [['20-23', '25-29', '31-36']],
            [EARTH]
        ), is_linked=(1, 'Light Speed')),
        Spell('Light Speed', [130, 197], Effects(
            [['21-24', '23-27']],
            [['25-29', '28-32']],
            [AIR],
        ), is_linked=(2, 'Ravages')),
        Spell('Assault', [25, 92, 159], Effects(
            [['9-10', '12-14', '15-18']],
            [['11-14', '14-17', '18-22']],
            [AIR]
        ), is_linked=(1, 'Aversion')),
        Spell('Aversion', [135], Effects(
            [['12-15']],
            [['15-18']],
            [FIRE],
        ), is_linked=(2, 'Assault')),
        Spell('Condensation', [32, 81, 124], Effects(
            [['13-16', '17-20', '21-25']],
            [['16-19', '20-24', '25-30']],
            [WATER]
        ), is_linked=(1, 'Influx')),
        Spell('Influx', [145], Effects(
            [['12-15']],
            [['15-18']],
            [EARTH],
        ), is_linked=(2, 'Condensation')),
        Spell('Hostility', [40, 107, 174], Effects(
            [['7-9', '10-12', '14-17']],
            [['10-12', '14-16', '18-21']],
            [FIRE]
        ), is_linked=(1, 'Projection')),
        Spell('Projection', [150], Effects(
            [['15-18']],
            [['18-22']],
            [WATER],
        ), is_linked=(2, 'Hostility')),
        Spell('Absorption', [69, 122, 162], Effects(
            [['14-17', '19-22', '22-26']] * 2,
            [['17-20', '23-28', '26-31']] * 2,
            [FIRE, FIRE],
            steals=[True, False],
            heals=[False, True],
            
        ), aggregates=[('Enemies', [0]),
                       ('Allies', [1])],
        is_linked=(1, 'Slaughter')),
        Spell('Slaughter', [165], Effects(
            [['29-33'],
             ['150']],
            [['35-40'],
             ['150']],
            [FIRE, 'buff_pow'],
            steals=[True, False],
        ), is_linked=(2, 'Absorption')),
        Spell('Decimation', [92, 141, 187], Effects(
            create_level_based_stacking_values(((17, 20), (22, 25), (24, 28)), 
                                               (20, 20, 20), 2),
            create_level_based_stacking_values(((21, 25), (26, 30), (29, 34)), 
                                               (20, 20, 20), 2),
            [[EARTH]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(1, 'Gash')),
        Spell('Gash', [195], Effects(
            create_stacking_values(((35, 39),), 30, 2),
            create_stacking_values(((42, 47),), 30, 2),
            [[EARTH]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(2, 'Decimation')),
        Spell('Fury', [70, 137], Effects(
            create_level_based_stacking_values(((19, 22), (24, 28)), 
                                               (20, 20), 2),
            create_level_based_stacking_values(((22, 26), (29, 34)), 
                                               (20, 20), 2),
            [[AIR]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(1, 'Carnage')),
        Spell('Carnage', [180], Effects(
            create_stacking_values(((35, 39),), 30, 2),
            create_stacking_values(((42, 47),), 30, 2),
            [[EARTH]] * 2
        ), aggregates=[(CHARGED_LABELS[n], [n]) for n in range(2)]
        , is_linked=(2, 'Fury')),
        Spell('Stase', [75, 142], Effects(
            [['19-23', '23-27']],
            [['22-26', '26-31']],
            [WATER],
            steals=[True]
        ), is_linked=(1, 'Dissolution')),
        Spell('Dissolution', [185], Effects(
            [['29-33']],
            [['35-40']],
            [WATER],
            steals=[True]
        ), is_linked=(2, 'Stase')),
        #TODO: Figure out how much Power Berserk gives
        Spell('Berserk', [195], Effects(
            [['50'],
             ['100'],
             ['150']],
            None,
            ['buff_pow','buff_pow','buff_pow']
        ), aggregates=[('Option 1', [0]),
                       ('Option 2', [1]),
                       ('Option 3', [2])]), 
        #TODO: The following spells should only display the best element
        Spell('Retribution', [90, 157], Effects(
            [['26-30', '31-35']] * 4,
            [['31-35', '36-40']] * 4,
            [EARTH, FIRE, WATER, AIR],
        ), is_linked=(1, 'Bloodthirsty Madness')),
        Spell('Bloodthirsty Madness', [200], Effects(
            [['24-28']] * 4,
            None,
            [EARTH, FIRE, WATER, AIR],
        ), is_linked=(2, 'Retribution')),
    ],
    'Sadida': [
        Spell('Bramble', [1, 25, 52], Effects(
            [['13-16', '17-20', '21-24']],
            [['18-21', '22-25', '26-29']],
            [EARTH],
        ), is_linked=(1, 'Poisoned Undergrowth')),
        Spell('Poisoned Undergrowth', [105], Effects(
            [['23-27']],
            [['28-32']],
            [EARTH],
        ), is_linked=(2, 'Bramble')),
        Spell('Paralysing Poison', [3, 35, 67], Effects(
            [['13', '19', '25']],
            None,
            [FIRE],
        )),
        Spell('Tear', [6, 42, 74], Effects(
            [['14-17', '18-21', '22-25']],
            [['18-21', '22-25', '26-29']],
            [WATER],
        ), is_linked=(1, 'Rise of Sap')),
        Spell('Rise of Sap', [120], Effects(
            [['29-32']],
            [['33-36']],
            [WATER],
            steals=[True],
        ), is_linked=(2, 'Tear')),
        Spell('Soothing Bramble', [13, 54, 94], Effects(
            [['46-50', '61-65', '76-80']],
            None,
            [FIRE],
            heals=[True],
         )),
        Spell('Earthquake', [27, 72, 118], Effects(
            [['21', '28', '35']],
            None,
            [FIRE],
        ), is_linked=(1, 'Shake')),
        Spell('Shake', [145], Effects(
            [['34-38']],
            None,
            [AIR],
        ), is_linked=(2, 'Earthquake')),
        Spell('Natural Gift', [32, 81, 124], Effects(
            [['30', '40', '50']],
            None,
            [FIRE],
            heals=[True],
        ), is_linked=(1, 'Inoculation')),
        Spell('Inoculation', [150], Effects(
            [['38-42']],
            None,
            [AIR],
        ), is_linked=(2, 'Natural Gift')),
        Spell('Manifold Bramble', [38, 90, 132], Effects(
            [['17-19', '22-24', '27-29']],
            [['21-23', '26-28', '31-33']],
            [EARTH],
        ), is_linked=(1, 'Force of Nature')),
        Spell('Force of Nature', [155], Effects(
            [['11-17']],
            [['21-27']],
            [EARTH],
        ), is_linked=(2, 'Manifold Bramble')),
        Spell('Dolly Sacrifice', [44, 97, 137], Effects(
            [['31-35', '37-41', '43-47']] * 2,
            [['38-42', '44-48', '50-54']] * 2,
            [WATER, WATER],
            steals=[False, True],
        ), aggregates=[('Enemies', [0]),
                       ('Allies/Summons', [1])],
        is_linked=(1, 'Bane')),
        Spell('Bane', [160], Effects(
            [['31-35']],
            [['34-38']],
            [WATER],
        ), is_linked=(2, 'Dolly Sacrifice')),
        Spell('Aggressive Bramble', [62, 116, 153], Effects(
            [['35-40', '42-47', '49-54']],
            [['42-47', '49-54', '56-61']],
            [EARTH],
        ), is_linked=(1, 'Plaguing Bramble')),
        Spell('Plaguing Bramble', [175], Effects(
            [['28-32']],
            None,
            [EARTH],
        ), is_linked=(2, 'Aggressive Bramble')),
        Spell('Wild Grass', [69, 122, 162], Effects(
            [['16-20', '21-25', '26-30']],
            [['22', '27', '32']],
            [FIRE],
        ), is_linked=(1, 'Contagion')),
        Spell('Contagion', [180], Effects(
            [['38-42']],
            [['46-50']],
            [AIR],
        ), is_linked=(2, 'Wild Grass')),
        Spell('Bush Fire', [84, 134, 178], Effects(
            [['8-11', '11-14', '14-17']] * 2,
            [['13', '16', '19']] * 2,
            [FIRE, WATER],
        ), aggregates=[('', [0, 1])],
        is_linked=(1, 'Voodoo Curse')),
        Spell('Voodoo Curse', [190], Effects(
            [['11-13'],
            ['11-13']],
            None,
            [FIRE, WATER],
        ), aggregates=[('If the target loses MP', [0]),
                       ('If the target loses AP', [1])],
        is_linked=(2, 'Bush Fire')),
        Spell('Paralysing Bramble', [195], Effects(
            [['18-20']],
            [['21-25']],
            [AIR],
         )),
    ],
    'Sram': [
        Spell('Tricky Trap', [1, 30, 60], Effects(
            [['18-20', '22-24', '26-28']],
            None,
            [FIRE],
        ), special='trap'),
        Spell('Deviousness', [1, 25, 52], Effects(
            [['14-16', '17-19', '20-22']],
            [['18-20', '21-23', '24-26']],
            [EARTH],
        ), is_linked=(1, 'Pitfall')),
        Spell('Pitfall', [110], Effects(
            [['30-34']],
            [['34-38']],
            [EARTH],
        ), is_linked=(2, 'Deviousness')),
        Spell('Insidious Poison', [3, 35, 67], Effects(
            [['6-7', '8-9', '10-11']],
            [['8-9', '10-11', '12-13']],
            [AIR],
        ), is_linked=(1, 'Toxines')),
        Spell('Toxines', [115], Effects(
            [['9-11']],
            None,
            [AIR],
        ), is_linked=(2, 'Insidious Poison')),
        Spell('Mistake', [6, 42, 74], Effects(
            [['11-14', '14-17', '17-20']] * 2
            + [['30', '40', '50']] * 2,
            [['15-18', '18-21', '21-24']] * 2
            + [['40', '50', '60']] * 2,
            [AIR, EARTH, 'buff_agi', 'buff_str'],
        ), aggregates=[('', [0, 1]),
                       ('', [2]),
                       ('', [3])], stacks=2,
        is_linked=(1, 'Raiding')),
        Spell('Raiding', [120], Effects(
            [['34-38']],
            [['40-44']],
            [WATER],
        ), is_linked=(2, 'Mistake')),
        Spell('Tricky Blow', [9, 47, 87], Effects(
            [['18-21', '22-25', '26-29']],
            [['22-25', '26-29', '31-34']],
            [FIRE],
        ), is_linked=(1, 'Cut-Throat')),
        Spell('Cut-Throat', [125], Effects(
            [['34-38'],
             ['250']],
            [['40-44'],
             ['250']],
            [FIRE, 'buff_pow_traps'],
        ), aggregates=[('', [0,]),
                       ('', [1])], stacks=1, 
        is_linked=(2, 'Tricky Blow')),
        Spell('Miry Trap', [17, 58, 102], Effects(
            [['21-25', '27-31', '33-37']],
            None,
            [WATER],
        ), 
        is_linked=(1, 'Larceny'),
        special='trap'),
        Spell('Larceny', [135], Effects(
            [['40-44'],
             ['80']],
            [['44-48'],
             ['100']],
            [WATER, 'buff_cha'],
        ), aggregates=[('', [0]),
                       ('', [1])], stacks=2, 
        is_linked=(2, 'Miry Trap')),
        Spell('Mass Trap', [22, 65, 108], Effects(
            [['24-28', '29-33', '34-38']],
            None,
            [EARTH],
        ), is_linked=(1, 'Trapster'),
        special='trap'),
        Spell('Trapster', [140], Effects(
            [['30-34']],
            [['33-37']],
            [EARTH],
        ), is_linked=(2, 'Mass Trap')),
        Spell('Cruelty', [27, 72, 118], Effects(
            [['12-14', '15-17', '18-20']],
            [['16-18', '19-21', '22-24']],
            [WATER],
        ), is_linked=(1, 'Ambush')),
        Spell('Ambush', [145], Effects(
            [['30-34']],
            [['34-38']],
            [FIRE],
        ), is_linked=(2, 'Cruelty')),
        Spell('Poisoned Trap', [32, 81, 124], Effects(
            [['6', '8', '10']],
            None,
            [AIR],
        ), is_linked=(1, 'Toxic Injection'),
        special='trap'),
        Spell('Toxic Injection', [150], Effects(
            [['28-32']],
            [['34-38']],
            [AIR],
        ), is_linked=(2, 'Poisoned Trap')),
        Spell('Chakra Concentration', [38, 90, 132], Effects(
            [['15', '15', '15',]],
            None,
            [FIRE],
            steals=[True],
        ), is_linked=(1, 'Fragmentation Trap')),
        Spell('Fragmentation Trap', [155], Effects(
            [['18-22'],
             ['33-37'],
             ['43-47'],
             ['58-62']],
            None,
            [FIRE, FIRE, FIRE, FIRE],
        ), aggregates=[('At the center', [0]),
                       ('One tile away from the center', [1]),
                       ('Two tiles away from the center', [2]),
                       ('Three tiles away from the center', [3])],
        is_linked=(2, 'Chakra Concentration'),
        special='trap'),
        Spell('Insidious Trap', [50, 103, 143], Effects(
            [['34-38', '41-45', '48-52']],
            None,
            [AIR],
        ), is_linked=(1, 'Epidemic'),
        special='trap'),
        Spell('Epidemic', [165], Effects(
            [['38-42']],
            [['46-50']],
            [AIR],
        ), is_linked=(2, 'Insidious Trap')),
        Spell('Repelling Trap', [56, 112, 147], Effects(
            [['8', '10', '12']],
            None,
            [AIR],
        ), special='trap'),
        Spell('Con', [69, 122, 162], Effects(
            [['25-29', '29-33', '33-37']],
            [['32', '36', '40']],
            [AIR],
        ), is_linked=(1, 'Proximity Trap')),
        Spell('Proximity Trap', [165], Effects(
            [['43-47']],
            None,
            [AIR],
        ), is_linked=(2, 'Con'), 
        special='trap'),
        Spell('Jinx', [77, 128, 172], Effects(
            [['22-26', '25-29', '28-32']],
            [['27-31', '30-34', '33-37']],
            [WATER],
            steals=[True],
        ), is_linked=(1, 'Calamity')),
        Spell('Calamity', [185], Effects(
            [['38-42']],
            None,
            [WATER],
            steals=[True],
        ), is_linked=(2, 'Jinx'),
        special='trap'),
        Spell('Furrow', [84, 134, 178], Effects(
            [['30-34', '35-39', '40-44'],
             ['40', '60', '80']],
            [['36-40', '41-45', '46-50'],
             ['60', '80', '100']],
            [FIRE, 'buff_int'],
        ), aggregates=[('', [0]),
                       ('', [1])], stacks=2,
        is_linked=(1, 'Perquisition')),
        Spell('Perquisition', [190], Effects(
            [['19-23']],
            [['23-27']],
            [WATER],
        ), is_linked=(2, 'Furrow')),
        Spell('Lethal Attack', [92, 141, 187], Effects(
            [['39-43', '46-50', '53-57']],
            [['49-53', '56-60', '63-67']],
            [EARTH],
        ), is_linked=(1, 'Malevolent Trap')),
        Spell('Malevolent Trap', [195], Effects(
            [['28-32']],
            None,
            [EARTH],
        ), is_linked=(2, 'Lethal Attack'),
        special='trap'),
        Spell('Lethal Trap', [100, 147, 197], Effects(
            [['37-41', '45-49', '53-57']],
            None,
            [EARTH],
        ), is_linked=(1, 'Perfidy'),
        special='trap'),
        Spell('Perfidy', [200], Effects(
            [['58-62']],
            [['64-68']],
            [EARTH],
        ), is_linked=(2, 'Lethal Trap')),
    ],
    'Xelor': [
        Spell('Slow Down', [1, 25, 52], Effects(
            [['4-5', '6-7', '8-9']],
            [['7-8', '9-10', '11-12']],
            [WATER],
        ), is_linked=(1, 'Souvenir')),
        Spell('Souvenir', [105], Effects(
            [['26-30']],
            [['30-34']],
            [EARTH],
        ), is_linked=(2, 'Slow Down')),
        Spell('Hand', [1, 30, 60], Effects(
            [['14-18', '18-22', '22-26']],
            [['20', '24', '28']],
            [FIRE],
        ), is_linked=(1, 'Cog')),
        Spell('Cog', [110], Effects(
            [['12-14']],
            [['15-17']],
            [WATER],
        ), is_linked=(2, 'Hand')),
        Spell('Shriveling', [3, 35, 67], Effects(
            [['16-19', '21-24', '26-29']],
            [['21-24', '26-29', '31-34']],
            [AIR],
        ), is_linked=(1, 'Drying Up')),
        Spell('Drying Up', [115], Effects(
            [['38-42']],
            [['44-48']],
            [AIR],
        ), is_linked=(2, 'Shriveling')),
        Spell("Xelor's Punch", [9, 47, 87], Effects(
            [['15-19', '19-23', '23-27']],
            [['21-25', '25-29', '29-33']],
            [EARTH],
        ), is_linked=(1, 'Gear')),
        Spell('Gear', [125], Effects(
            [['31-35']],
            [['34-38']],
            [EARTH],
        ), is_linked=(2, "Xelor's Punch")),
        Spell('Frostbite', [17, 58, 102], Effects(
            [['5-7', '8-10', '11-13']],
            [['11', '14', '17']],
            [AIR],
        ), is_linked=(1, 'Disruption')),
        Spell('Disruption', [135], Effects(
            [['9-11']],
            [['11-13']],
            [FIRE],
        ), is_linked=(2, 'Frostbite')),
        Spell("Xelor's Sandglass", [22, 65, 108], Effects(
            [['9-11', '12-14', '15-17']],
            [['13-15', '16-18', '19-21']],
            [FIRE],
        ), is_linked=(1, 'Temporal Distortion')),
        Spell('Temporal Distortion', [140], Effects(
            [['34-38']],
            [['38-42']],
            [AIR],
        ), is_linked=(2, "Xelor's Sandglass")),
        Spell('Time Theft', [27, 72, 118], Effects(
            [['20-24', '25-29', '30-34']],
            [['25-29', '30-34', '35-39']],
            [WATER],
        ), is_linked=(1, 'Petrification')),
        Spell('Petrification', [145], Effects(
            [['34-38']],
            [['38-42']],
            [WATER],
        ), is_linked=(2, 'Time Theft')),
        Spell('Temporal Dust', [38, 90, 132], Effects(
            [['22-25', '28-31', '34-37']],
            [['26-29', '32-35', '38-41']],
            [FIRE],
        ), is_linked=(1, 'Temporal Suspension')),
        Spell('Temporal Suspension', [155], Effects(
            [['25-29']],
            [['29-33']],
            [FIRE],
        ), is_linked=(2, 'Temporal Dust')),
        Spell('Loss of Motivation', [50, 103, 143], Effects(
            [['17-20', '20-23', '23-26']],
            [['22-25', '25-28', '28-31']],
            [EARTH],
        ), is_linked=(1, 'Pendulum')),
        Spell('Pendulum', [165], Effects(
            [['38-42']],
            [['46-50']],
            [AIR],
        ), is_linked=(2, 'Loss of Motivation')),
        Spell('Clock', [84, 134, 178], Effects(
            [['28-31', '32-35', '36-39']],
            [['32-35', '36-39', '40-43']],
            [WATER],
        ), is_linked=(1, 'Water Clock')),
        Spell('Water Clock', [190], Effects(
            [['30-34']],
            [['36-40']],
            [WATER],
        ), is_linked=(2, 'Clock')),
        Spell('Dark Ray', [92, 141, 187], Effects(
            [['27-31', '30-34', '33-37']],
            [['34-38', '37-41', '40-44']],
            [EARTH],
        ), is_linked=(1, 'Shadowy Beam')),
        Spell('Shadowy Beam', [195], Effects(
            [['19-23']],
            [['23-27']],
            [EARTH],
        ), is_linked=(2, 'Dark Ray')),
        Spell('Knell', [200], Effects(
            [['4']] * 4,
            None,
            [AIR, WATER, EARTH, FIRE],
        ), aggregates=[('', [0, 1, 2, 3])]),
    ],
    'Eliotrope': [
        Spell('Affliction', [1, 25, 52], Effects(
            [['14-16', '17-19', '20-22']],
            [['18-20', '21-23', '24-26']],
            [WATER],
        ), is_linked=(1, 'Tribulation')),
        Spell('Tribulation', [105], Effects(
            [['22-26']],
            [['25-29']],
            [WATER],
        ), is_linked=(2, 'Affliction')),
        Spell('Insult', [1, 30, 60], Effects(
            [['20-22', '23-25', '26-28']],
            [['25-27', '28-30', '31-33']],
            [AIR],
        ), is_linked=(1, 'Contempt')),
        Spell('Contempt', [110], Effects(
            [['30-34']],
            [['33-37']],
            [AIR],
        ), is_linked=(2, 'Insult')),
        Spell('Shock', [3, 35, 67], Effects(
            [['19-21', '24-26', '29-31']],
            [['22-24', '27-29', '32-34']],
            [EARTH],
        ), is_linked=(1, 'Convulsion')),
        Spell('Convulsion', [115], Effects(
            [['20-22']],
            [['23-25']],
            [EARTH],
        ), is_linked=(2, 'Shock')),
        Spell('Wakfu Ray', [6, 42, 74], Effects(
            [['16-18', '21-23', '26-28']] * 2,
            [['19-21', '24-26', '29-31']] * 2,
            [FIRE, FIRE],
            heals=[False, True],
        ), aggregates=[('Enemies', [0]),
                       ('Allies', [1])],
        is_linked=(1, 'Lazybeam')),
        Spell('Lazybeam', [120], Effects(
            [['27-31']] * 2,
            [['31-35']] * 2,
            [FIRE, FIRE],
            steals=[False, True],
        ), aggregates=[('Directly', [0]),
                       ('Through a portal', [1])],
        is_linked=(2, 'Wakfu Ray')),
        Spell('Offence', [13, 54, 94], Effects(
            [['16-20', '21-25', '26-30']],
            [['20-24', '25-29', '30-34']],
            [FIRE],
        ), is_linked=(1, 'Affront')),
        Spell('Affront', [130], Effects(
            [['25-29']],
            [['28-32']],
            [FIRE],
        ), is_linked=(2, 'Offence')),
        Spell('Therapy', [22, 65, 108], Effects(
            [['15-17', '19-21', '23-25']],
            [['19-21', '23-25', '28-30']],
            [EARTH],
        ), is_linked=(1, 'Sinecure')),
        Spell('Sinecure', [140], Effects(
            [['43-47']],
            [['52-56']],
            [WATER],
        ), is_linked=(2, 'Therapy')),
        Spell('Bullying', [38, 90, 132], Effects(
            [['15-17', '19-21', '23-25']],
            [['19-21', '23-25', '27-29']],
            [AIR],
        ), is_linked=(1, 'Correction ')),
        Spell('Correction ', [155], Effects(
            [['34-38']],
            [['38-42']],
            [AIR],
        ), is_linked=(2, 'Bullying')),
        Spell('Lightning Fist', [50, 103, 143], Effects(
            [['15-17', '19-21', '23-25']],
            [['19-21', '23-25', '27-29']],
            [WATER],
        )),
        Spell('Snub', [62, 116, 153], Effects(
            [['20-24', '23-27', '26-30']],
            [['24-28', '27-31', '30-34']],
            [EARTH],
        )),
        Spell('Audacious', [69, 122, 162], Effects(
            [['22-26', '25-29', '28-32']],
            [['25-29', '28-32', '31-35']],
            [WATER],
        ), is_linked=(1, 'Composure')),
        Spell('Composure', [180], Effects(
            [['32-36']],
            [['39-43']],
            [WATER],
        ), is_linked=(2, 'Audacious')),
        Spell('Focus', [77, 128, 172], Effects(
            [['50', '75', '100'],
             ['100', '150', '200']],
            None,
            ['buff_pow', 'buff_pow'],
        ), aggregates=[('Directly', [0]),
                       ('Through a portal', [1])]),
        Spell('Parasite', [84, 134, 178], Effects(
            [['23-27', '28-32', '33-37']],
            [['26-30', '31-35', '36-40']],
            [FIRE],
        ), is_linked=(1, 'Virus')),
        Spell('Virus', [190], Effects(
            [['34-38']],
            [['41-45']],
            [FIRE],
        ), is_linked=(2, 'Parasite')),
        Spell('Ridicule', [92, 141, 187], Effects(
            [['22-26', '26-30', '30-34']],
            [['26-30', '30-34', '34-38']],
            [AIR],
        ), is_linked=(1, 'Persiflage')),
        Spell('Persiflage', [195], Effects(
            [['25-29']],
            [['30-34']],
            [EARTH],
        ), is_linked=(2, 'Ridicule')),
    ],
    'Huppermage': [
        Spell('Ether', [1, 20, 40], Effects(
            [['12-14', '16-18', '20-22']],
            [['15-17', '19-21', '23-25']],
            [AIR],
        ), is_linked=(1, 'Stinger')),
        Spell('Stinger', [101], Effects(
            [['18-22'],
             ['18-22']],
            [['22-26'],
             ['22-26']],
            [WATER, EARTH],
        ), is_linked=(2, 'Ether')),
        Spell('Telluric Wave', [1, 25, 52], Effects(
            [['15-19', '20-24', '25-29']],
            [['20-24', '25-29', '30-34']],
            [EARTH],
        ), is_linked=(1, 'Celestial Wave')),
        Spell('Celestial Wave', [105], Effects(
            [['20-24'],
             ['20-24']],
            [['25-29'],
             ['25-29']],
            [EARTH, AIR],
        ), is_linked=(2, 'Telluric Wave')),
        Spell('Flamethrower', [3, 35, 67], Effects(
            [['12-14', '16-18', '20-22']],
            [['16-18', '20-22', '24-26']],
            [FIRE],
        ), is_linked=(1, 'Cataract')),
        Spell('Cataract', [115], Effects(
            [['26-30'],
             ['26-30']],
            [['31-35'],
             ['31-35']],
            [FIRE, WATER],
        ), is_linked=(2, 'Flamethrower')),
        Spell('Stalagmite', [6, 42, 74], Effects(
            [['18-21', '23-26', '28-31']],
            [['24-27', '29-32', '34-37']],
            [WATER],
        ), is_linked=(1, 'Ember')),
        Spell('Ember', [120], Effects(
            [['23-27'],
             ['23-27']],
            [['28-32'],
             ['28-32']],
            [AIR, FIRE],
        ), is_linked=(2, 'Stalagmite')),
        Spell('Elemental Drain', [9, 47, 87], Effects(
            [['15-19', '19-23', '23-27']] * 4
            + [['100', '150', '200']] * 4,
            [['19-23', '23-27', '27-31']] * 4
            + [['130', '180', '230']] * 4,
            [AIR, WATER, FIRE, EARTH,
             'buff_agi', 'buff_cha', 'buff_int', 'buff_str'], 
        ), aggregates=[('Target in air state', [0]),
                       ('', [4]),
                       ('Target in water state', [1]),
                       ('', [5]),
                       ('Target in fire state', [2]),
                       ('', [6]),
                       ('Target in earth state', [3]),
                       ('', [7])], stacks=2,
        is_linked=(1, 'Morph')),
        Spell('Morph', [125], Effects(
            [['28-32']] * 4,
            [['33-37']] * 4,
            [AIR, WATER, FIRE, EARTH], 
        ), aggregates=[('Target in air state', [0]),
                       ('Target in water state', [1]),
                       ('Target in fire state', [2]),
                       ('Target in earth state', [3])],
        is_linked=(2, 'Elemental Drain')),
        Spell('Storm', [13, 54, 94], Effects(
            [['24-28', '29-33', '34-38']],
            [['29-33', '34-38', '39-43']],
            [EARTH],
            steals=[True]
        ), is_linked=(1, 'Tectonic Breach')),
        Spell('Tectonic Breach', [130], Effects(
            [['13-15']],
            [['15-17']],
            [EARTH],
            steals=[True]
        ), is_linked=(2, 'Storm')),
        Spell('Astral Blade', [17, 58, 102], Effects(
            [['22-25', '27-30', '32-35']],
            [['26-29', '31-34', '36-39']],
            [AIR],
        ), is_linked=(1, 'Telluric Blade')),
        Spell('Telluric Blade', [135], Effects(
            [['34-38']],
            [['39-43']],
            [EARTH],
        ), is_linked=(2, 'Astral Blade')),
        Spell('Burning Stroke', [27, 72, 118], Effects(
            [['23-27', '28-32', '33-37']],
            [['28-32', '33-37', '38-42']],
            [FIRE],
            steals=[True]
        ), is_linked=(1, 'Volcano')),
        Spell('Volcano', [145], Effects(
            [['19-21']],
            [['21-23']],
            [FIRE]
        ), is_linked=(2, 'Burning Stroke')),
        Spell('Glacier', [32, 81, 124], Effects(
            [['22-26', '28-32', '34-38']],
            [['26-30', '32-36', '38-42']],
            [WATER],
            steals=[True]
        ), is_linked=(1, 'Stalactite')),
        Spell('Stalactite', [150], Effects(
            [['23-25']],
            [['26-28']],
            [WATER],
        ), is_linked=(2, 'Glacier')),
        Spell('Journey', [38, 90, 132], Effects(
            [['15-24', '23-32', '31-40']] * 4,
            None,
            [AIR, WATER, FIRE, EARTH], 
        ), aggregates=[('Target in air state', [0]),
                       ('Target in water state', [1]),
                       ('Target in fire state', [2]),
                       ('Target in earth state', [3])]),
        Spell('Deflagration', [50, 103, 143], Effects(
            [['22-26', '26-30', '30-34']],
            [['26-30', '30-34', '34-38']],
            [FIRE],
        ), is_linked=(1, 'Flood')),
        Spell('Flood', [165], Effects(
            [['26-30']],
            [['30-34']],
            [WATER],
        ), is_linked=(2, 'Deflagration')),
        Spell('Contribution', [56, 112, 147], Effects(
            [['150'] * 3],
            None,
            ['buff_pow']
        ), aggregates=[('Target in water state', [0])], stacks=2),
        Spell('Icy Shards', [62, 81, 124], Effects(
            [['24-28', '29-33', '34-38']],
            [['28-32', '33-37', '38-42']],
            [WATER],
        ), is_linked=(1, 'Sun Lance')),
        Spell('Sun Lance', [175], Effects(
            [['34-38']],
            [['39-43']],
            [FIRE],
        ), is_linked=(2, 'Icy Shards')),
        Spell('Transfixing Gust', [84, 134, 178], Effects(
            [['23-27', '27-31', '31-35']],
            [['27-31', '31-35', '35-39']],
            [AIR],
            steals=[True]
        ), is_linked=(1, 'Hurricane')),
        Spell('Hurricane', [190], Effects(
            [['17-19']],
            [['19-21']],
            [AIR]
        ), is_linked=(2, 'Transfixing Gust')),
        Spell('Striking Meteor', [92, 141, 187], Effects(
            [['20-24', '25-29', '30-34']],
            [['23-27', '28-32', '33-37']],
            [EARTH],
        ), is_linked=(1, 'Comet')),
        Spell('Comet', [195], Effects(
            [['28-32']],
            [['32-36']],
            [AIR],
        ), is_linked=(2, 'Striking Meteor')),
    ],
    'Ouginak': [
        Spell('Watchdog', [1, 25, 52], Effects(
            [['21-25', '26-30', '31-35']],
            [['25-29', '30-34', '35-39']],
            [EARTH],
        ), is_linked=(1, 'Jaw')),
        Spell('Jaw', [105], Effects(
            [['28-32']],
            [['34-38']],
            [FIRE],
        ), is_linked=(2, 'Watchdog')),
        Spell('Ulna', [1, 30, 60], Effects(
            [['14-16', '19-21', '24-26']],
            [['19-21', '24-26', '29-31']],
            [WATER],
        ), is_linked=(1, 'Calcaneus')),
        Spell('Calcaneus', [110], Effects(
            [['13-15']],
            [['16-18']],
            [WATER],
        ), is_linked=(2, 'Ulna')),
        Spell('Carcass', [3, 35, 67], Effects(
            create_level_based_stacking_values(((7, 9), (8, 10), (9, 11)), 
                                               (2, 3, 4), 6),
            create_level_based_stacking_values(((9, 11), (10, 12), (11, 13)), 
                                               (2, 3, 4), 6),
            [[AIR]] * 6,
        ), aggregates=[('', [0]),
                       ('After hitting a Prey once', [1]),
                       ('After hitting a Prey twice', [2]),
                       ('After hitting a Prey 3x', [3]),
                       ('After hitting a Prey 4x', [4]),
                       ('After hitting a Prey 5x', [5])],
        is_linked=(1, 'Stripping')),
        Spell('Stripping', [115], Effects(
            [['28-32']],
            [['34-38']],
            [AIR],
        ), is_linked=(2, 'Carcass')),
        Spell('Cutting Down', [6, 42, 74], Effects(
            [['19-21', '24-26', '29-31']],
            [['25-27', '30-32', '35-37']],
            [FIRE],
        ), is_linked=(1, 'Woof')),
        Spell('Woof', [120], Effects(
            [['19-21']],
            [['23-25']],
            [FIRE],
            steals=[True],
        ), is_linked=(2, 'Cutting Down')),
        Spell('Mastiff', [17, 58, 102], Effects(
            [['10-11', '13-14', '16-17']] * 2,
            [['12-13', '15-16', '18-19']] * 2,
            [EARTH,EARTH],
            steals=(False, True)
        ), aggregates=[('', [0]),
                       ('If the target is Prey', [1])],
        is_linked=(1, 'Muzzle')),
        Spell('Muzzle', [135], Effects(
            [['53-57']],
            [['59-63']],
            [EARTH],
        ), is_linked=(2, 'Mastiff')),
        Spell('Tibia', [22, 65, 108], Effects(
            [['29-33', '36-40', '43-47']],
            [['34-38', '41-45', '48-52']],
            [WATER],
        ), is_linked=(1, 'Humerous')),
        Spell('Humerous', [140], Effects(
            [['43-47']],
            [['48-52']],
            [EARTH],
        ), is_linked=(2, 'Tibia')),
        Spell('Tracking', [27, 72, 118], Effects(
            [['22-24', '28-30', '34-36']],
            [['27-29', '33-35', '39-41']],
            [FIRE],
        ), is_linked=(1, 'Hunt')),
        Spell('Hunt', [145], Effects(
            [['38-42']],
            [['44-48']],
            [FIRE],
        ), is_linked=(2, 'Tracking')),
        Spell('Bloodhound', [32, 81, 124], Effects(
            [['16-18', '21-23', '26-28'],
             ['70', '110', '150']],
            [['20-22', '25-27', '30-32'],
             ['70', '110', '150']],
            [AIR, 'buff_pow'],
        ), aggregates=[('', [0]),
                       ('If the target is Prey', [1])],
        is_linked=(1, 'Beaten')),
        Spell('Beaten', [150], Effects(
            [['26-30']],
            [['30-34']],
            [AIR],
        ), is_linked=(2, 'Bloodhound')),
        Spell('R-Canine', [38, 90, 132], Effects(
            [['100', '150', '200']],
            None,
            ['buff_pow'],
        )),
        Spell('Carrion', [50, 103, 143], Effects(
            [['23-27', '28-32', '33-37']],
            [['28-32', '33-37', '38-42']],
            [AIR],
        ), is_linked=(1, 'Radius')),
        Spell('Radius', [165], Effects(
            [['34-38']],
            [['38-42']],
            [WATER],
        ), is_linked=(2, 'Carrion')),
        Spell('Marrow Bone', [56, 112, 147], Effects(
            create_level_based_stacking_values(((21, 23), (25, 27), (29, 31)), 
                                               (5, 6, 7), 6),
            create_level_based_stacking_values(((26, 28), (30, 32), (34, 36)), 
                                               (5, 6, 7), 6),
            [[WATER]] * 6,
        ), aggregates=[('', [0]),
                       ('After hitting a Prey once', [1]),
                       ('After hitting a Prey twice', [2]),
                       ('After hitting a Prey 3x', [3]),
                       ('After hitting a Prey 4x', [4]),
                       ('After hitting a Prey 5x', [5])],
        is_linked=(1, 'Vertebra')),
        Spell('Vertebra', [170], Effects(
            [['28-32']],
            [['34-38']],
            [WATER],
        ), is_linked=(2, 'Marrow Bone')),
        Spell('Cerberus', [69, 122, 162], Effects(
            [['37-41', '40-44', '43-47']],
            [['44-48', '47-51', '50-54']],
            [EARTH],
        ), is_linked=(1, 'Amarok')),
        Spell('Amarok', [180], Effects(
            [['25-29']],
            [['29-33']],
            [EARTH],
        ), is_linked=(2, 'Cerberus')),
        Spell('Tetanisation', [92, 141, 187], Effects(
            [['29-33', '36-40', '43-47']],
            [['35-39', '42-46', '49-53']],
            [FIRE],
        ), is_linked=(1, 'Carving Up')),
        Spell('Carving Up', [195], Effects(
            [['31-35']],
            [['35-39']],
            [AIR],
        ), is_linked=(2, 'Tetanisation')),
    ]
}

DEFAULT_SOFT_CAPS = {
    'vit': [0, None, 0, 0, 0, 0],
    'wis': [0, 0, 0, None, 0, 0],
    'str': [0, 100, 200, 300, None, 0],
    'int': [0, 100, 200, 300, None, 0],
    'cha': [0, 100, 200, 300, None, 0],
    'agi': [0, 100, 200, 300, None, 0]
}
SOFT_CAPS = {'Cra' : DEFAULT_SOFT_CAPS,
             'Ecaflip' : DEFAULT_SOFT_CAPS,
             'Eniripsa' : DEFAULT_SOFT_CAPS,
             'Enutrof' : DEFAULT_SOFT_CAPS,
             'Feca' : DEFAULT_SOFT_CAPS,
             'Iop' : DEFAULT_SOFT_CAPS,
             'Osamodas' : DEFAULT_SOFT_CAPS,
             'Pandawa' : DEFAULT_SOFT_CAPS,
             'Foggernaut' : DEFAULT_SOFT_CAPS,
             'Rogue' : DEFAULT_SOFT_CAPS,
             'Sacrier' : DEFAULT_SOFT_CAPS,
             'Sadida' : DEFAULT_SOFT_CAPS,
             'Sram' : DEFAULT_SOFT_CAPS,
             'Xelor' : DEFAULT_SOFT_CAPS,
             'Eliotrope' : DEFAULT_SOFT_CAPS,
             'Masqueraider' : DEFAULT_SOFT_CAPS,
             'Huppermage' : DEFAULT_SOFT_CAPS,
             'Ouginak' : DEFAULT_SOFT_CAPS}

def calculate_damage(base_damage, char_stats, critical_hit, is_spell):
    damage_instances = []
    for dam in base_damage:
        element_val = max(char_stats[DAMAGE_TYPE_TO_MAIN_STAT[dam.element]], 0)
        if not dam.heals:
            element_val = element_val + max(char_stats['pow'], 0)
            element_dam = char_stats[dam.element.lower() + "dam"]
            element_dam = element_dam + char_stats['dam']
            if critical_hit:
                element_dam += char_stats['cridam']
        else:
            element_dam = char_stats['heals']
        minimum_damage = (max(int((1 + element_val / 100.0) * dam.min_dam)
                                               + element_dam, 0))
        maximum_damage = (max(int((1 + element_val / 100.0) * dam.max_dam)
                                               + element_dam, 0))
        if is_spell:
            minimum_damage = minimum_damage * (100 + char_stats['perspedam'])/100
            maximum_damage = maximum_damage * (100 + char_stats['perspedam'])/100
        else:
            minimum_damage = minimum_damage * (100 + char_stats['perweadam'])/100
            maximum_damage = maximum_damage * (100 + char_stats['perweadam'])/100
        damage = CalculatedDamage(min_dam=minimum_damage,
                                  max_dam=maximum_damage,
                                  element=dam.element,
                                  steals=dam.steals,
                                  heals=dam.heals)
        
        damage_instances.append(damage)
    return damage_instances

class CalculatedDamage(BaseDamage):
    pass

class BuffEffect(BaseDamage):
    pass