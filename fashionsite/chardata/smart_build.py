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

from django.utils.translation import ugettext_lazy
from itertools import product, combinations
import pickle

from chardata.options import get_options, set_options
from fashionistapulp.dofus_constants import DAMAGE_TYPES, STAT_KEY_TO_NAME, MAIN_STATS


ALL_ASPECTS_LIST = ['str', 'int', 'cha', 'agi',
                    'vit', 'res', 'omni', 'wis',
                    'glasscannon', 'dam', 'crit', 'noncrit', 'heal',
                    'aprape', 'mprape',
                    'pvp', 'duel',
                    'trap', 'summon', 'pushback',
                    'pp', 'pods']

ALL_ASPECTS = set(ALL_ASPECTS_LIST)

ASPECT_TO_NAME = {
    'str': ugettext_lazy('Strength'),
    'int': ugettext_lazy('Intelligence'),
    'cha': ugettext_lazy('Chance'),
    'agi': ugettext_lazy('Agility'),
    'vit': ugettext_lazy('Vitality'),
    'res': ugettext_lazy('Resists'),
    'omni': ugettext_lazy('Omni-Elemental'),
    'wis': ugettext_lazy('Leeching'),
    'dam': ugettext_lazy('Linear Damage'),
    'crit': ugettext_lazy('Critical Hits'),
    'noncrit': ugettext_lazy('Avoid Critical Hits'),
    'heal': ugettext_lazy('Linear Heals'),
    'aprape': ugettext_lazy('AP Removal'),
    'mprape': ugettext_lazy('MP Removal'),
    'pvp': ugettext_lazy('Group PVP'),
    'duel': ugettext_lazy('Duel PVP'),
    'trap': ugettext_lazy('Traps'),
    'summon': ugettext_lazy('Summons'),
    'pushback': ugettext_lazy('Pushback'),
    'pp': ugettext_lazy('Prospecting'),
    'pods': ugettext_lazy('Pods'),
    'balanced': ugettext_lazy('Balanced'),
    'glasscannon': ugettext_lazy('Glass-Cannon'),
}

ASPECT_TO_SHORT_NAME = {
    'str': 'Str',
    'int': 'Int',
    'cha': 'Cha',
    'agi': 'Agi',
    'vit': 'Vit',
    'res': 'Res',
    'omni': 'Omni',
    'wis': 'Leecher',
    'dam': 'Dam',
    'crit': 'Crit',
    'noncrit': 'Non-Crit',
    'heal': 'Heals',
    'aprape': 'AP Red',
    'mprape': 'MP Red',
    'pvp': 'PVP',
    'duel': 'Duel',
    'trap': 'Traps',
    'summon': 'Summons',
    'pushback': 'Pushback',
    'pp': 'PP',
    'pods': 'Pods',
    'glasscannon': 'Glass Cannon',
}

RACE_TO_BUILD_PROFILE = {
    'default': {
        'endgame_mins': (11, 6), # Min AP and MP for level 200.
        'meleeness': 0.5, # Importance of melee attacks (0.0-1.0)
        'neutdam': 0.1, # Neutral damage w. as a fraction of earth damage w.
        'range_importance': 1.0, # Percentage of range required, relative to a highly range
                                 # dependent build.
        'apred_importance': 0.0, # Percentage of importance of AP Reduction.
        'mpred_importance': 0.0, # Percentage of importance of MP Reduction.
        'lock_importance': 0.4, # Percentage of importance of Lock.
        'dodge_importance': 0.4, # Percentage of importance of Dodge.
        'vit_importance': 0.5, # Percentage of importance of Vitality.
        'pshdam_importance': 0.0, # Percentage of importance of Pushback Damage.
        'heals_importance': 0.0, # Percentage of heals importance.
        'summons_are_important': False, # Whether summons weight should scale.
        'min_summons_low_level': 1, # Minimum summons at level 40-149.
        'min_summons_high_level': 1, # Minimum summons at level 150+.
        'pow_power': 1.0, # Percentage of how effective power is.
        'traps_are_important': False, # Whether trap damage matters.
        'earthdam': 0.0, # Importance of earth damage as multiple of Strength.
        'firedam': 0.0, # Importance of fire damage as multiple of Intelligence.
        'waterdam': 0.0, # Importance of water damage as multiple of Chance.
        'airdam': 0.0, # Importance of air damage as multiple of Agility.
        'cridam': 0.45, # Importance of Critical Damage for 1/2 crit chars relative to Damage.
        'fireres': 0.0, # Increase % of Linear Fire Resist
        '%fireres': 0.0, # Increase % of % Fire Resist
    },
    'Cra': {
        # TODO: Aspects
        # - Pushback damage
        # - Field manipulation
        # - Debuffer
        # - Spike damage
        # - Crowd control
        'all': {
            'mpred_importance': 0.6, # Poisoned Arrow, Paralyzing Arrow
            'lock_importance': 0.1,
            'dodge_importance': 0.9,
            'vit_importance': 0.4,
            'pshdam_importance': 0.2, # Lashing Arrow
            'meleeness': 0.0,
        },
        'str': {
            'mpred_importance': 0.8, # Poisoned Arrow
            'earthdam': 1.5,
            'neutdam': 0.4, # Poisoned Arrow
        },
        'int': {
            'apred_importance': 0.6, # Paralyzing Arrow (int)
            'pshdam_importance': 0.4, # Burning Arrow, Repulsive Arrow
            'firedam': 1.7,
        },
        'cha': {
            'apred_importance': 0.3, # Slow Down Arrow
            'mpred_importance': 1.0, # Paralyzing Arrow
            'waterdam': 1.6,
        },
        'agi': {
            'pshdam_importance': 0.4, # Retreat Arrow
            'airdam': 1.7,
        },
    },
    'Ecaflip': {
        # TODO: Aspects
        # - Non-crit
        # - Crit
        'all': {
            'range_importance': 0.5,
            'cridam': 0.4, # Rekop
            'vit_importance': 0.6, # Repercussion, Pussycat
        },
        'str': {
            'meleeness': 0.5,
            'mpred_importance': 0.3, # Fate of Ecaflip, Lapping Up
            'pshdam_importance': 0.2, # Fate of Ecaflip, Ecaflip's Audacity
            'earthdam': 1.4,
        },
        'int': {
            'meleeness': 0.1,
            'range_importance': 1.0, # Topkaj, Rough Tongue
            'heals_importance': 0.1, # Yowling, All or Nothing, Peril
            'pow_power': 0.4, # Yowling, Felintion, All or Nothing
            'firedam': 0.9,
        },
        'cha': {
            'meleeness': 0.3,
            'pshdam_importance': 0.05, # Felintion, Kraps
            'dodge_importance': 0.6, # Felintion, Kraps
            'waterdam': 1.4,
        },
        'agi': {
            'meleeness': 0.5,
            'pshdam_importance': 0.1, # Claw of Ceangal
            'airdam': 1.5,
        },
    },
    'Eniripsa': {
        # TODO: Aspects
        # - Damage dealer
        'all': {
            'apred_importance': 0.1, # Word of Silence
            'mpred_importance': 0.1, # Paralyzing Word, Overwhelming Word
            'lock_importance': 0.1,
            'pshdam_importance': 0.05, # Frightening Word
            'heals_importance': 0.05,
        },
        'str': {
            'meleeness': 0.5,
            'earthdam': 2.0,
        },
        'int': {
            'meleeness': 0.3,
            'heals_importance': 0.5, # Alternative Word
            'pow_power': 0.3,
            'firedam': 1.0,
        },
        'cha': {
            'meleeness': 0.7,
            'apred_importance': 0.4, # Thunderous Word
            'mpred_importance': 0.4, # Overwhelming Word
            'lock_importance': 0.3, # Thunderous Word
            'waterdam': 1.4,
        },
        'agi': {
            'meleeness': 0.2,
            'dodge_importance': 0.6,
            'airdam': 1.4,
            'pshdam_importance': 0.2, # Turbulent Word
        },
    },
    'Enutrof': {
        # TODO: Aspects
        # - Range specialist
        # - Melee specialist
        'all': {
            'apred_importance': 0.1, # Mass Clumsiness, Loafylactic
            'mpred_importance': 1.0, # Clumsiness, Shovel of Judgment, Prime of Life, Spade Kiss
            'dodge_importance': 0.5,
            'min_summons_low_level': 2, # Living Shovel, Living Bag, Living Chest
            'min_summons_high_level': 2,
        },
        'str': {
            'meleeness': 0.4,
            'lock_importance': 0.3,
            'dodge_importance': 0.7,
            'earthdam': 1.9,
        },
        'int': {
            'meleeness': 0.3,
            'lock_importance': 0.5,
            'dodge_importance': 0.5,
            'firedam': 1.7,
        },
        'cha': {
            'meleeness': 0.0,
            'lock_importance': 0.1,
            'dodge_importance': 0.9,
            'waterdam': 1.7,
        },
        'agi': {
            'meleeness': 0.5,
            'lock_importance': 0.5,
            'dodge_importance': 0.5,
            'airdam': 1.9,
            'apred_importance': 0.5, # Loafylactic
            'pshdam_importance': 0.1, # Spade of Judgment
        },
    },
    'Feca': {
        'all': {
            'range_importance': 0.5, # Glyph of Repulsion, Barricade, Bastion
            'neutdam': 1.0, # Blindness, Tetany
            'apred_importance': 0.2, # Blindness, Glyph of Blindness
            'mpred_importance': 0.2, # Paralyzing Glyph
            'lock_importance': 0.6, # Glyph of Repulsion
            'cridam': 0.25, # Glyphs
        },
        'str': {
            'meleeness': 0.8,
            'apred_importance': 0.6, # Blindness, Tetany
            'lock_importance': 0.7, # Dazzling, Tetany
            'earthdam': 1.0,
        },
        'int': {
            'meleeness': 0.1,
            'mpred_importance': 0.7, # Lethargy
            'dodge_importance': 0.6, # Lethargy
            'lock_importance': 0.4,
            'firedam': 1.6,
        },
        'cha': {
            'meleeness': 0.0,
            'range_importance': 1.0,
            'dodge_importance': 0.9, # Bubble, Cloudy Attack
            'apred_importance': 0.7, # Glyph of Blindness
            'lock_importance': 0.4,
            'pshdam_importance': 0.1, # Tension
            'waterdam': 1.6,
        },
        'agi': {
            'meleeness': 0.8,
            'dodge_importance': 0.7, # [!] Boursoufflure, Low range spells
            'lock_importance': 0.7, # Low range spells
            'pshdam_importance': 0.2, # Gust, [!] Boursoufflure
            'airdam': 1.9,
        },
    },
    'Foggernaut': {
        # TODO: Aspects:
        # - Healer
        # - Pushback damage
        'all': {
            'range_importance': 0.5, # Breakwater, Dreadnaut, Harpooner
            'lock_importance': 0.2,
            'dodge_importance': 0.5,
            'vit_importance': 0.7, # Turrets, [!] Blindage
            'heals_importance': 0.15, # First Aid
            'mpred_importance': 0.1, # [!] Nautile, [!] Corrosion
            'cridam': 0.3, # Turrets
        },
        'str': {
            'meleeness': 0.2,
            'pshdam_importance': 0.7, # Backwash, Trident
            'earthdam': 2.0,
        },
        'int': {
            'meleeness': 0.4,
            'heals_importance': 0.25, # First Aid, [!] Sauvetage
            'pow_power': 0.8, # First Aid, [!] Sauvetage
            'firedam': 1.8,
        },
        'cha': {
            'meleeness': 0.1,
            'dodge_importance': 0.7, # Froth, Torrent
            'pshdam_importance': 0.2, # Froth
            'mpred_importance': 0.3, # [!] Nautile
            'waterdam': 1.7,
        },
        'agi': {
            'meleeness': 0.6,
            'pshdam_importance': 0.7, # [!] Harmattan, [!] Torpille
            'mpred_importance': 0.2, # [!] Corrosion
            'airdam': 1.8,
        },
    },
    'Iop': {
        # TODO: Aspects
        # - Pushback damage ([!] Violence, Intimidation, [!] Coup pour Coup)
        # - Shield support ([!] Vertu, [!] Rassemblement, [!] Conquete)
        # - Crowd control ([!] Tannee, [!] Tumulte, [!] Sentence)
        'all': {
            'neutdam': 0.3, # Intimidation
            'range_importance': 0,
            'mpred_importance': 0.1, # Cut
            'lock_importance': 0.6,
        },
        'str': {
            'meleeness': 1.0,
            'pshdam_importance': 0.2, # Intimidation
            'earthdam': 1.3,
        },
        'int': {
            'meleeness': 0.6,
            'range_importance': 1.0, # Cut, Sentence
            'mpred_importance': 0.4, # Cut
            'dodge_importance': 0.6, # Strengthstorm
            'firedam': 1.3,
        },
        'cha': {
            'meleeness': 0.8,
            'waterdam': 1.5,
            'vit_importance': 0.7, # Outpouring, Threat, [!] Fendoir, [!] Endurance
        },
        'agi': {
            'meleeness': 0.5,
            'airdam': 1.5,
            'mpred_importance': 0.6, # [!] Tannee
        },
    },
    'Masqueraider': {
        # TODO: Aspects
        # - Coward
        # - Classic
        # - Psycho
        'all': {
            'meleeness': 0.8,
            'range_importance': 0.5, # Picada, [!] Agular, Tortoruga, [!] Armadur, [!] Atabak, [!] Brincaderia, [!] Ponteira
            'mpred_importance': 0.1, # Apathy
            'dodge_importance': 0.1,
            'vit_importance': 0.8, # Shields
            'pshdam_importance': 0.1, # [!] Comedie
        },
        'str': {
            'mpred_importance': 0.3, # Apathy
            'apred_importance': 0.2, # [!] Atabak
            'earthdam': 1.6,
        },
        'int': {
            'firedam': 1.6,
        },
        'cha': {
            'pshdam_importance': 0.7, # Boliche, Distance
            'waterdam': 1.6,
        },
        'agi': {
            'mpred_importance': 0.2, # Retention
            'airdam': 1.6,
        },
    },
    'Osamodas': {
        'all': {
            'lock_importance': 0.5,
            'dodge_importance': 0.6,
            'vit_importance': 0.6,
            'range_importance': 0.0,
            'summons_are_important': True,
            'min_summons_low_level': 2,
            'min_summons_high_level': 3,
        },
        'str': {
            'meleeness': 0.5,
            'vit_importance': 0.8, # close range
            'lock_importance': 0.8, # close range
            'mpred_importance': 0.2, # Fossil
            'earthdam': 1.8,
        },
        'int': {
            'meleeness': 0.2,
            'vit_importance': 0.5, # long range
            'range_importance': 0.5, # Dragonic, Dragon's Breath
            'heals_importance': 0.2, # Whip
            'dodge_importance': 0.8, # Whip, Dragonic
            'firedam': 1.4,
        },
        'cha': {
            'meleeness': 0.7,
            'waterdam': 1.6,
        },
        'agi': {
            'meleeness': 0.0,
            'range_importance': 1.0, # Duster, Canine, [!] Croc Repulsif, [!] Deplumage
            'min_summons_low_level': 3, # Tofus, Duster
            'min_summons_high_level': 4, # Tofus, Duster
            'airdam': 1.6, # Duster
        },
    },
    'Pandawa': {
        # TODO: Aspects
        # - Drunk
        # - Sober
        'all': {
            'range_importance': 0.5, # Terror, Vulnerability, Stabilization, Pandiniuras, Spirit Bond
            'dodge_importance': 0.3, # Stabilization, Karcham
            'min_summons_high_level': 2, # Spirit Bond, Drunkeness
        },
        'str': {
            'meleeness': 0.6,
            'lock_importance': 0.8,
            'earthdam': 1.5,
        },
        'int': {
            'meleeness': 0.2,
            'range_importance': 0.75, # Blazing Fist, Explosive Flask
            'dodge_importance': 0.5,
            'firedam': 1.6,
        },
        'cha': {
            'meleeness': 0.4,
            'range_importance': 1.0, # Tipple, Melancholy, [!] Gnole
            'waterdam': 1.5,
        },
        'agi': {
            'meleeness': 0.0,
            'range_importance': 1.0, # Alcoholic Breath, [!] Engourdissement, [!] Liqueur, [!] Nausee
            'dodge_importance': 0.6,
            'pshdam_importance': 0.2, # Alcoholic Breath
            'airdam': 1.6,
            'mpred_importance': 0.2, # [!] Engourdissement
        },
    },
    'Rogue': {
        # TODO: Aspects:
        # - Bomber
        # - Direct damage
        'all': {
            'meleeness': 0.0,
            'vit_importance': 0.6, # Bombs
            'range_importance': 0.5, # Detonator, Kickback, Magnet, Dirty Trick, [!] Stratageme, [!] Explobombe Collante, [!] Piege Magnetique, Powder, Overload, Kaboom
            'cridam': 0.25, # Bombs
        },
        'str': {
            'earthdam': 1.0,
        },
        'int': {
            'firedam': 1.0,
        },
        'cha': {
            'meleeness': 0.4, # Blunderbuss, Deception
            'apred_importance': 0.2, # Deception, Water Bomb
            'waterdam': 1.2,
        },
        'agi': {
            'meleeness': 0.0,
            'range_importance': 1.0, # Boomerang Daggers, [!] Cadence, [!] Mitraille
            'mpred_importance': 0.2, # Grenado
            'pshdam_importance': 0.1, # [!] Mitraille
            'dodge_importance': 0.7,
            'airdam': 1.3,
        },
    },
    'Sacrier': {
        'all': {
            'meleeness': 1.0,
            'range_importance': 0.25, # Attraction, Transposition
            'lock_importance': 0.7,
            'vit_importance': 0.7,
        },
        'str' : {
            'meleeness': 0.8,
            'earthdam': 1.6,
        },
        'int': {
            'pshdam_importance': 0.05, # [!] Aversion
            'firedam': 1.6,
        },
        'cha': {
            'lock_importance': 0.9,
            'mpred_importance': 0.1, # [!] Stase
            'waterdam': 2.0,
        },
        'agi': {
            'pshdam_importance': 0.05, # [!] Hostilite
            'airdam': 1.8,
        },
    },
    'Sadida': {
        'all': {
            'range_importance': 0.0,
            'mpred_importance': 0.5, # Soothing Bramble, Wild Grass
            'dodge_importance': 0.6, # No pushback
            'min_summons_low_level': 2,
            'min_summons_high_level': 3,
        },
        'str': {
            'meleeness': 0.1,
            'range_importance': 1.0, # Bramble, Aggressive Bramble, [!] Broussaille Empoisonnee
            'earthdam': 1.8,
        },
        'int': {
            'meleeness': 0.0,
            'range_importance': 1.0, # Paralysing Poison, Wild Grass, Bush Fire
            'mpred_importance': 0.6, # Wild Grass
            'heals_importance': 0.1, # Soothing Bramble, Natural Gift
            'pow_power': 0.7, # Soothing Bramble, Natural Gift
            'firedam': 1.4,
        },
        'cha': {
            'meleeness': 0.5,
            'range_importance': 1.0, # Tear, Bush Fire
            'waterdam': 1.8,
        },
        'agi': {
            'meleeness': 0.0,
            'range_importance': 1.0, # [!] Contagion, [!] Ronce Paralysante
            'mpred_importance': 0.3, # [!] Ronce Paralysante
            'airdam': 1.8,
        },
    },
    'Sram': {
        'all': {
            'range_importance': 1.0,
            'mpred_importance': 0.2, # Paralyzing Trap
            'lock_importance': 0.8, # Double
            'traps_are_important': True,
            'cridam': 0.35, # Traps
        },
        'str': {
            'meleeness': 0.7,
            'earthdam': 1.4,
        },
        'int': {
            'meleeness': 0.7,
            'pshdam_importance': 0.2, # Tricky Blow
            'firedam': 1.8,
        },
        'cha': {
            'meleeness': 0.6,
            'waterdam': 1.6,
        },
        'agi': {
            'meleeness': 0.7,
            'airdam': 2.0,
        },
    },
    'Xelor': {
        'all': {
            'meleeness': 0.4,
            'range_importance': 0.5,
            'apred_importance': 1.0,
            'dodge_importance': 0.5,
        },
        'str': {
            'meleeness': 0.6,
            'apred_importance': 0.2,
            'earthdam': 1.8,
        },
        'int': {
            'meleeness': 0.4,
            'apred_importance': 1.0,
            'range_importance': 1.0, # Hand, Xelor's Sandglass
            'firedam': 1.8,
        },
        'cha': {
            'meleeness': 0.5,
            'range_importance': 1.0,
            'apred_importance': 0.8,
            'waterdam': 1.8,
        },
        'agi': {
            'meleeness': 0.4,
            'apred_importance': 0.2,
            'airdam': 1.7,
        },
    },
    'Eliotrope': {
        'all': {
            'meleeness': 0.1,
            'range_importance': 0.0,
            'dodge_importance': 0.5,
        },
        'str': {
            'range_importance': 0.5,
            'pshdam_importance': 0.05, # Convulsion
            'earthdam': 1.5,
        },
        'int': {
            'range_importance': 0.5,
            'heals_importance': 0.05, # Curative Palm
            'firedam': 1.5,
        },
        'cha': {
            'range_importance': 0.5,
            'pshdam_importance': 0.1, # Lightning Fist
            'waterdam': 1.5,
        },
        'agi': {
            'mpred_importance': 0.1, # Ridicule
            'pshdam_importance': 0.2, # Bullying
            'airdam': 1.5,
            'meleeness': 0.2,
        },
    },
    'Huppermage': {
        'all': {
            'dodge_importance': 0.3,
            'lock_importance': 0.5,
        },
        'str': {
            'meleeness': 0.0,
            'range_importance': 1.0, # Telluric Wave, Striking Meteor
            'mpred_importance': 0.2,
            'pshdam_importance': 0.05,
            'earthdam': 1.3,
        },
        'int': {
            'meleeness': 0.3,
            'range_importance': 0.75, # Flamethrower
            'apred_importance': 0.1,
            'mpred_importance': 0.2,
            'vit_importance': 0.6, # Contibution
            'firedam': 1.3,
        },
        'cha': {
            'meleeness': 0.75,
            'range_importance': 0.0,
            'mpred_importance': 0.2,
            'vit_importance': 0.6,
            'lock_importance': 0.7,
            'waterdam': 1.2,
        },
        'agi': {
            'meleeness': 0.0,
            'range_importance': 0.75, # Astral Blade
            'pshdam_importance': 0.05,
            'apred_importance': 0.1,
            'airdam': 1.3,
        },
        'agi/int': {
            'meleeness': 0.2,
            'apred_importance': 1.3,
        },
        'agi/str': {
            'meleeness': 0.0,
            'pshdam_importance': 0.95,
            'vit_importance': 0.3,
        },
        'cha/int': {
            'meleeness': 0.75,
            'vit_importance': 0.6,
            'lock_importance': 0.8,
        },
        'cha/str': {
            'meleeness': 0.5,
            'mpred_importance': 1.8,
        },
    },
    'Ouginak': {
        'all': {
            'vit_importance': 0.7, # Protective Pelt, Appeasement, close range
            'range_importance': 0.0,
            'dodge_importance': 0.3,
            'lock_importance': 0.6,
            'mpred_importance': 0.3,
        },
        'str': {
            'meleeness': 1.0,
            'earthdam': 1.4,
            'vit_importance': 0.7,
            'lock_importance': 0.7,
        },
        'int': {
            'meleeness': 1.0,
            'firedam': 1.4,
            'mpred_importance': 1.0, # Cutting Down, Tetanisation
            'pshdam_importance': 0.3, # [!] Aboi, [!] Chasse
        },
        'cha': {
            'meleeness': 0.6,
            'waterdam': 1.4,
            'vit_importance': 0.5,
            'range_importance': 1.0,
            'lock_importance': 0.4,
            'dodge_importance': 0.4, # Ulna
            'pshdam_importance': 0.1, # Tibia
        },
        'agi': {
            'meleeness': 0.8,
            'airdam': 1.4,
        },
    },
}

RACES_WITH_HYBRID_PROFILES = ['Huppermage']

def param_for_build(race, elements, param, policy='max'):
    if len(elements) == 0:
        return _param_for_race(race, param)
    elif len(elements) == 1:
        return _param_for_profile_element(race, elements[0], param, is_combination=False)
    else:
        values = []

        if race in RACES_WITH_HYBRID_PROFILES:
            for element_combination in combinations(elements, 2):
                combination = '/'.join(sorted(element_combination))
                param_for_element = _param_for_profile_element(race, combination, param,
                                                               is_combination=True)
                if param_for_element is not None:
                    # Weight 2 for combinations.
                    for _ in  range(2):
                        values.append(param_for_element)

        for element in elements:
            param_for_element = _param_for_profile_element(race, element, param,
                                                           is_combination=False)
            # Weight 1 for single elements.
            values.append(param_for_element)

        if policy == 'max':
            return max(values)
        elif policy == 'float_avg':
            return sum(values) / float(len(values))
        else:
            print 'Policy unknown'

def _param_for_profile_element(race, element, param, is_combination):
    profile = RACE_TO_BUILD_PROFILE[race]
    element_profile = profile.get(element, None)
    if element_profile is not None:
        val = element_profile.get(param, None)
        if val is not None:
            return val

    if is_combination:
        return None
    else:
        return _param_for_race(race, param)

def _param_for_race(race, param):
    profile = RACE_TO_BUILD_PROFILE[race]
    val = profile['all'].get(param, None)
    if val is not None:
        return val
    return RACE_TO_BUILD_PROFILE['default'][param]

def _set_minimums(char, aspects):
    race = char.char_class
    level = char.level
    elements = get_elements(aspects)
    
    mins = {}
    
    # AP/MP/Range/Summons
    if level < 60:
        mins['ap'], mins['mp'] = 6, 3
        mins['range'] = 0
    elif level < 120:
        mins['ap'], mins['mp'] = 8, 4
        mins['range'] = 2
    elif level < 160:
        mins['ap'], mins['mp'] = 9, 5
        mins['range'] = 3
    elif level < 199:
        mins['ap'], mins['mp'] = 10, 5
        mins['range'] = 4
    elif level < 200:
        mins['ap'], mins['mp'] = 11, 5
        mins['range'] = 4
    else:
        mins['ap'], mins['mp'] = param_for_build(race, elements, 'endgame_mins')
        mins['range'] = 4
    
    mins['range'] = round(mins['range']
                          * param_for_build(race, elements, 'range_importance', 'float_avg'))
    
    if level < 40:
        mins['summon'] = 1
    elif level < 180:
        mins['summon'] = param_for_build(race, elements, 'min_summons_low_level')
    else:
        mins['summon'] = param_for_build(race, elements, 'min_summons_high_level')

    if 'summon' in aspects:
        mins['summon'] += 1
 
    # Options
    options = get_options(char)
    # TODO: Implement soft mode and hard mode. In soft mode, avoid switching options.
    # if level == 200:
    #    options['ap_exo'] = (level == 200)
    #    options['mp_exo'] = True if level == 200 else 'gelano' if level >= 120 else False
    #    options['turq_dofus'] = (level >= 190)
    #options['shields'] = ('duel' in aspects)
    options['dofus'] = 'cawwot' if ('wis' in aspects) else True
    set_options(char, options)
    
    # Convert mins keys
    mins_by_name = {}
    for k, v in mins.iteritems():
        mins_by_name[STAT_KEY_TO_NAME[k]] = int(v)
    
    # Set result in char
    char.minimum_stats = pickle.dumps(mins_by_name)

def get_standard_weights(char):
    w = _set_weights(char, get_char_aspects(char), apply=False)
    return w

def _set_weights(char, aspects, apply=True):
    race = char.char_class
    level = char.level
    level_pct = level / 200.0
    elements = get_elements(aspects)
    element_count = len(elements)
    
    w = {}
    
    # Weights
    b = 20

    w['ap'] = (20 + 100 * level_pct) * b
    w['mp'] = (20 + 100 * level_pct) * b
    range_importance = param_for_build(race, elements, 'range_importance', 'float_avg')
    w['range'] = (16 + 80 * level_pct) * range_importance * b
    
    attack_factor = {0: 0, 1: 3.5, 2: 3, 3: 2, 4: 1.5}[element_count]
    if 'glasscannon' in aspects:
        attack_factor *= 1.4
    dam_mult = 2 if 'dam' in aspects else 1
    res_per_factor = 2 + (10 * level_pct * level_pct)
    w['lock'] = param_for_build(race, elements, 'lock_importance', 'float_avg') * 10 * b
    w['dodge'] = param_for_build(race, elements, 'dodge_importance', 'float_avg') * 10 * b
    if 'vit' in aspects:
        w['vit'] = 1.5  * b
    else:
        w['vit'] = (param_for_build(race, elements, 'vit_importance', 'float_avg') + 0.5) * b
    w['hp'] = w['vit']

    w['wis'] = (25 if 'wis' in aspects else 2) * b
    w['str'] = attack_factor * b if 'str' in elements else 0
    w['int'] = attack_factor * b if 'int' in elements else 0
    w['agi'] = attack_factor * b if 'agi' in elements else 0
    w['cha'] = attack_factor * b if 'cha' in elements else 0
    w['agi'] = max(w['agi'], (w['dodge'] + w['lock']) / 10)
    w['pow'] = {0: 0, 1: 3.2, 2: 5, 3: 5.2, 4: 5.5}[element_count] * b
    if 'glasscannon' in aspects:
        w['pow'] *= 1.5
    w['pow'] *= param_for_build(race, elements, 'pow_power', 'float_avg')
    
    w['earthdam'] = w['str'] * param_for_build(race, elements, 'earthdam') * dam_mult
    w['firedam'] = w['int'] * param_for_build(race, elements, 'firedam') * dam_mult
    w['airdam'] = w['agi'] * param_for_build(race, elements, 'airdam') * dam_mult
    w['waterdam'] = w['cha'] * param_for_build(race, elements, 'waterdam') * dam_mult
    w['neutdam'] = param_for_build(race, elements, 'neutdam') * w['earthdam']
    w['dam'] = w['neutdam'] + w['earthdam'] + w['firedam'] + w['airdam'] + w['waterdam']
    res_w = ((1.5 if 'res' in aspects else 1)
             * (0.5 if 'glasscannon' in aspects else 1)
             * b)
    resper_w = res_per_factor * res_w
    for damage_type in DAMAGE_TYPES:
        w['%sres' % damage_type] = res_w
        w['%sresper' % damage_type] = resper_w
    
    linear_res_bonus_factor = (0.5 * level_pct + 0.5)
    w['fireres'] *= (1 + param_for_build(race, elements, 'fireres', 'float_avg') * linear_res_bonus_factor)
    w['fireresper'] *= (1 + param_for_build(race, elements, '%fireres', 'float_avg'))
    
    w['apred'] = param_for_build(race, elements, 'apred_importance', 'float_avg') * 12 * b
    w['mpred'] = param_for_build(race, elements, 'mpred_importance', 'float_avg') * 12 * b
    w['apres'] = 5 * b if 'pvp' in aspects else 1 * b
    w['mpres'] = 2 * b if 'pvp' in aspects else 1 * b
    
    minimum_red = 20 * b if len(elements) == 0 else 5 * b
    if 'aprape' in aspects:
        w['apred'] = max(2.5 * w['apred'], minimum_red)
    if 'mprape' in aspects:
        w['mpred'] = max(2.5 * w['mpred'], minimum_red)
    w['wis'] = max(w['wis'], (w['apred'] + w['mpred'] + w['apres'] + w['mpres']) / 10.0)
    
    if 'dam' in aspects:
        w['dam'] = max(w['dam'], 30 * b)

    w['heals'] = param_for_build(race, elements, 'heals_importance', 'float_avg') * 8 * b
    if 'heal' in aspects:
        w['heals'] = 4 * b + w['heals'] * 1.5
        int_per_heals_factor = 5 # TODO: Depend on class
        w['int'] = max(w['int'], w['heals'] / int_per_heals_factor)

    if param_for_build(race, elements, 'traps_are_important'):
        if 'trap' in aspects:
            w['trapdam'] = 10 * b
            w['trapdamper'] = 3 * b
        else:
            w['trapdam'] = 3 * b
            w['trapdamper'] = 1 * b

    w['pp'] = 10 * b if 'pp' in aspects else 0.2 * b if 'pvp' not in aspects else 0
    w['cha'] = max(w['cha'], w['pp'] / 10.0)

    w['init'] =  0.3 * b if 'duel' in aspects else 0.1 * b if 'pvp' in aspects else 0.05 * b

    if 'pods' in aspects:
        w['pod'] = 10 * b
        w['str'] = max(w['str'], w['pod'] / 5.0)

    if 'pushback' in aspects:
        w['pshdam'] = 10 * b
    else:
        w['pshdam'] = param_for_build(race, elements, 'pshdam_importance', 'float_avg') * 10 * b

    if param_for_build(race, elements, 'summons_are_important'):
        w['summon'] = 40 * b if 'summon' in aspects else 10 * b
    else:
        w['summon'] = 20 * b if 'summon' in aspects else 1 * b

    w['pshres'] = 0.1 * b
    w['crires'] = 2 * res_w if 'pvp' in aspects else 0.2 * res_w

#     if 'duel' in aspects:
#         for res_type in product(['neut', 'earth', 'fire', 'water', 'air'],
#                                 ['', 'per']):
#             w['pvp%sres%s' % res_type] = w['%sres%s' % res_type]
            
    # Crits
    if 'crit' in aspects:
        w['ch'] = 25 * b
        w['cridam'] = 2 * w['dam'] * param_for_build(race, elements, 'cridam', 'float_avg')
    elif 'noncrit' in aspects:
        w['ch'] = -4 * b
        w['cridam'] = 0
    else:
        w['ch'] = 12 * b
        w['cridam'] = w['dam'] * param_for_build(race, elements, 'cridam', 'float_avg')

    marginal_final_damage_effect = _lerp(2, 12, level_pct)
    marginal_final_damage_w = w['pow'] * marginal_final_damage_effect
    meleeness = param_for_build(race, elements, 'meleeness', 'float_avg')

    # Melee vs ranged % final damage
    chance_of_melee_atk_for_cras = 0.1
    chance_of_melee_atk_for_sacs = 0.7
    chance_of_melee_atk = _lerp(chance_of_melee_atk_for_cras,
                                chance_of_melee_atk_for_sacs,
                                meleeness)
    w['permedam'] = chance_of_melee_atk * marginal_final_damage_w
    w['perrandam'] = (1.0 - chance_of_melee_atk) * marginal_final_damage_w
    
    # Weapon vs spell % final damage
    chance_of_weapon = _lerp(0.0, 0.25, level_pct)
    w['perweadam'] = chance_of_weapon * marginal_final_damage_w
    w['perspedam'] = (1.0 - chance_of_weapon) * marginal_final_damage_w

    # Melee vs ranged % final damage taken
    chance_of_melee_def_for_cras = 0.2
    chance_of_melee_def_for_sacs = 0.4
    chance_of_melee_def = _lerp(chance_of_melee_def_for_cras,
                                chance_of_melee_def_for_sacs,
                                meleeness)
    w['respermee'] = chance_of_melee_def * resper_w * 5
    w['resperran'] = (1.0 - chance_of_melee_def) * resper_w * 5
    
    w['meleeness'] = meleeness

    # Discretize w
    for k in w:
        w[k] = int(round(w[k]))
        
    # Set result in char
    if apply:
        char.stats_weight = pickle.dumps(w)
    else:
        return w

def _lerp(a, b, t):
    return a * (1.0 - t) + b * t

def _apply_aspects(char, aspects, set_minimums):
    if set_minimums:
        _set_minimums(char, aspects)
    _set_weights(char, aspects)
    
def reapply_weights(char):
    _set_weights(char, get_char_aspects(char))
   
def get_elements(aspects):
    elements = []
    if 'omni' in aspects:
        elements.extend(MAIN_STATS)
    else:
        for el in MAIN_STATS:
            if el in aspects:
                elements.append(el)
    return elements

def get_char_aspects(char):
    aspects = set()
    if char.aspects:
        aspects = pickle.loads(char.aspects)
    return aspects
    
def set_char_aspects(char, aspects, reset, set_minimums=True):
    char.aspects = pickle.dumps(aspects)
    if reset:
        _apply_aspects(char, aspects, set_minimums)
    char.char_build = _generate_build_line(aspects)
    char.save()

def char_has_aspect(char, aspect):
    return aspect in get_char_aspects(char)

def _generate_build_line(aspects):
    sections = [[] for _ in range(3)]
    for aspect in aspects:
        if aspect in MAIN_STATS:
            sections[0].append(aspect)
        elif aspect in ['crit', 'noncrit']:
            sections[1].append(aspect)
        elif aspect != 'omni':
            sections[2].append(aspect)

    if 'omni' in aspects:
        sections[0] = ['omni']

    sections = filter(bool, sections)
    for section in sections:
        section.sort(key=lambda x: ALL_ASPECTS_LIST.index(x))
        
    return ' '.join(['/'.join([ASPECT_TO_SHORT_NAME[a] for a in section])
        for section in sections])
