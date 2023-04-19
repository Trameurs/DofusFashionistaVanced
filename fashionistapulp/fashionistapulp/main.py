# -*- coding: utf-8 -*-

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

from model import Model
from model import ModelInput
import cProfile

base_stats_by_attr = {}
base_stats_by_attr['Power'] = 0
base_stats_by_attr['Damage'] = 0
base_stats_by_attr['Heals'] = 0
base_stats_by_attr['AP'] = 7
base_stats_by_attr['Critical Hits'] = 0
base_stats_by_attr['Agility'] = 0
base_stats_by_attr['Strength'] = 0
base_stats_by_attr['Neutral Damage'] = 0
base_stats_by_attr['Earth Damage'] = 0
base_stats_by_attr['Intelligence'] = 0
base_stats_by_attr['Fire Damage'] = 0
base_stats_by_attr['Air Damage'] = 0
base_stats_by_attr['Chance'] = 330
base_stats_by_attr['Water Damage'] = 0
base_stats_by_attr['Vitality'] = 0
base_stats_by_attr['Initiative'] = 0
base_stats_by_attr['Summon'] = 1
base_stats_by_attr['Neutral Resist'] = 0
base_stats_by_attr['Range'] = 0
base_stats_by_attr['% Neutral Resist'] = 0
base_stats_by_attr['Wisdom'] = 0
base_stats_by_attr['% Water Resist'] = 0
base_stats_by_attr['Water Resist'] = 0
base_stats_by_attr['Air Resist'] = 0
base_stats_by_attr['Fire Resist'] = 0
base_stats_by_attr['Earth Resist'] = 0
base_stats_by_attr['MP'] = 3
base_stats_by_attr['% Air Resist'] = 0
base_stats_by_attr['% Fire Resist'] = 0
base_stats_by_attr['% Earth Resist'] = 0
base_stats_by_attr['Prospecting'] = 100
base_stats_by_attr['Pods'] = 1000
base_stats_by_attr['AP Reduction'] = 0
base_stats_by_attr['MP Reduction'] = 0
base_stats_by_attr['Lock'] = 0
base_stats_by_attr['Dodge'] = 0
base_stats_by_attr['Reflects'] = 0
base_stats_by_attr['Pushback Damage'] = 0
base_stats_by_attr['Trap Damage'] = 0
base_stats_by_attr['% Trap Damage'] = 0
base_stats_by_attr['Critical Resist'] = 0
base_stats_by_attr['Pushback Resist'] = 0
base_stats_by_attr['MP Loss Resist'] = 0
base_stats_by_attr['AP Loss Resist'] = 0
base_stats_by_attr['Critical Damage'] = 0
base_stats_by_attr['Critical Failure'] = 0
base_stats_by_attr['% Damage'] = 0
base_stats_by_attr['MP Reduction Resist'] = 0
base_stats_by_attr['AP Reduction Resist'] = 0

base_stats_by_attr_case2 = {}
base_stats_by_attr_case2['AP'] = 6
base_stats_by_attr_case2['Agility'] = 101
base_stats_by_attr_case2['Strength'] = 174
base_stats_by_attr_case2['Intelligence'] = 200
base_stats_by_attr_case2['Chance'] = 101
base_stats_by_attr_case2['Vitality'] = 101
base_stats_by_attr_case2['Summon'] = 1
base_stats_by_attr_case2['Wisdom'] = 101
base_stats_by_attr_case2['MP'] = 3
base_stats_by_attr_case2['Prospecting'] = 100
base_stats_by_attr_case2['Pods'] = 1000

objective_values = {'vit': 18,
                    'str': 50,
                    'cha': 40,
                    'pow': 80,
                    'dodge': 200}

objective_values_2 = {'vit': 2,
                    'pp': 20,
                    'cha': 10,
                    'waterdam': 20}
objective_values_3 = {'vit': 20,
                      'wis': 40,
                      'str': 0,
                      'int': 0,
                      'cha': 0,
                      'agi': 6,
                      'pow': 0,
                      'ap': 800,
                      'mp': 600,
                      'range': 300,
                      'summon': 20,
                      'ch': 0,
                      'init': 1,
                      'pp': 4,
                      'lock': 20,
                      'dodge': 40,
                      'apred': 20,
                      'mpred': 20,
                      'apres': 20,
                      'mpres': 20,
                      'pshres': 2,
                      'crires': 8,
                      'pod': 0,
                      'ref': 0,
                      'trapdam': 0,
                      'trapdamper': 0,
                      'dam': 600,
                      'neutdam': 100,
                      'earthdam': 100,
                      'firedam': 100,
                      'airdam': 100,
                      'waterdam': 100,
                      'cridam': 0,
                      'pshdam': 0,
                      'heals': 0,
                      'neutres': 40,
                      'earthres': 40,
                      'fireres': 40,
                      'airres': 40,
                      'waterres': 40,
                      'neutresper': 100,
                      'earthresper': 100,
                      'fireresper': 100,
                      'airresper': 100,
                      'waterresper': 100,
#                       'pvpneutres': 0,
#                       'pvpearthres': 0,
#                       'pvpfireres': 0,
#                       'pvpairres': 0,
#                       'pvpwaterres': 0,
#                       'pvpneutresper': 0,
#                       'pvpearthresper': 0,
#                       'pvpfireresper': 0,
#                       'pvpairresper': 0,
#                       'pvpwaterresper': 0
                        }

options = {'ap_exo': False,
           'mp_exo': False}
options_caso2 = {'ap_exo': False,
                 'mp_exo': False,
                 'turq_dofus': True,
                 'turq_dofus_picker': '20'}

def main():
    model = Model()
#    
#    model.setup(155, base_stats_by_attr,
#                {'AP': 10, 'MP': 5, 'Range': 5, 'Agility': 134, 'Critical Hits': 45},
#                {}, set(), objective_values_2, options)
#    model.run()
#    print model.get_result_string()
    
    model.setup(ModelInput(73,
                           base_stats_by_attr_case2,
                           {'AP': 10, 'MP': 4, 'Range': 2, 'Summon': 1},
                           {},
                           set(['Dofusteuse', 'Vulbis Dofus']),
                           {key: 2*value for (key,value) in objective_values_3.iteritems()},
                           options_caso2))
    model.run(1)
    print model.get_result_string()

#    model.setup(120, base_stats_by_attr, {'AP': 8, 'MP': 4, 'Range': 2},
#                {'dofus1': 'Vagabond', 'shield': 'Stasili'}, set(['Dolmanax', 'Ochre Dofus']),
#                objective_values, options)
#    model.run()
#    print model.get_result_string()
#    
#    model.setup(160, base_stats_by_attr, {'AP': 11, 'MP': 5, 'Range': 3},
#                {'dofus1': 'Vagabond', 'shield': 'Stasili'}, set(['Ochre Dofus']),
#                objective_values, options)
#    model.run()
#    print model.get_result_string()
#    
#    model.setup(199, base_stats_by_attr, {'AP': 11, 'MP': 6, 'Range': 3},
#                {'dofus1': 'Vagabond', 'shield': 'Stasili'}, set(), objective_values,
#                options)
#    model.run()
#    print model.get_result_string()

if __name__ == '__main__':
#    cProfile.run('main()', 'prof.prof')
    main()
    