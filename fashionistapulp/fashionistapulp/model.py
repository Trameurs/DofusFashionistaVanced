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

from dofus_constants import TYPE_NAME_TO_SLOT_NUMBER, STAT_MAXIMUM, SOFT_CAPS
from lpproblem import LpProblem2
from modelresult import ModelResultMinimal
from pulp.solvers import PulpSolverError
from restrictions import Restrictions
from structure import get_structure

from collections import Counter


class Model:
    
    def __init__(self):
        self.create_structure()
        
        self.problem = LpProblem2()
        self.restrictions = Restrictions()
        self.item_count = len(self.items_list)
        
        self.create_variables()
        self.create_constraints()
        
    def create_structure(self):
        self.structure = get_structure()
        self.items_list = self.structure.get_available_items_list()
        self.sets_list = self.structure.get_sets_list()
        self.stats_list = self.structure.get_stats_list()
        self.main_stats_list = self.structure.get_main_stats_list()

    def create_variables(self):
        self.create_item_number_variables()
        self.create_item_presence_variables()
        self.create_set_variables()
        self.create_stat_total_variables()
        self.create_stat_points_variables()
        self.create_light_set_variables()
    
    def create_item_number_variables(self):
        for item in self.items_list:
            max_number = 2 if self.structure.get_type_name_by_id(item.type) == 'Ring' and item.set == None else 1
            self.problem.setup_variable('x', item.id, 0, max_number)    
    
    def create_item_presence_variables(self):
        for item in self.items_list:
            self.problem.setup_variable('p', item.id, 0,  1)
    
    def create_set_variables(self):
        self.set_count = len(self.sets_list)     
     
        for item_set in self.sets_list:
            self.problem.setup_variable('s', item_set.id, 0, 9)
            for slot_number in xrange(0, 10):
                self.problem.setup_variable('ss', '%d_%d' % (item_set.id, slot_number), 0, 1)    

    def create_stat_total_variables(self):
        self.stat_count = len(self.stats_list)
     
        for stat in self.stats_list:
            if stat.name in STAT_MAXIMUM:
                self.problem.setup_variable('stat', stat.id, None, STAT_MAXIMUM[stat.name])
            else:
                self.problem.setup_variable('stat', stat.id, None, None)

    def create_stat_points_variables(self):
        self.stat_count = len(self.stats_list)
        
        for stat in self.main_stats_list:
            for i in xrange(0, 6):
                self.problem.setup_variable('stat_point', 'statpoint_%d_%d' % (i, stat.id), 0, None)  
            for i in xrange(0, 5):  
                self.problem.setup_variable('stat_point_max', 'statpointmax_%d_%d' % (i, stat.id), 0, 1)  
    
    def create_light_set_variables(self):
        self.problem.setup_variable('ytrophy', 1, 0,  1)
        self.problem.setup_variable('ytrophy', 2, 0,  1)
        self.problem.setup_variable('trophies', 1, 0,  1)
        
    def add_weird_item_weights_to_objective_funcion(self, objective_values, level):    
        
        #Adding more weight to Turquoise Dofus equivalent to 5 CH
        #For each Critical Hit inflicted, the final damage is increased by 1% for 3 turns. Can be stacked 10 times.
        turq_dofus_new_stat_weight = objective_values.get('ch', 0) * 5
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Turquoise Dofus').id, 
                               turq_dofus_new_stat_weight)
        
        #Adding more weight to Crimson Dofus equivalent to 40 Power * level / 200
        #For each distance attack suffered, the final damage inflicted is increased by 1% for 1 turns. The effects are stackable 10 times.
        crimson_dofus_new_stat_weight = objective_values.get('pow', 0) * 40.0 * level / 200
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Crimson Dofus').id, 
                               crimson_dofus_new_stat_weight)
        
        #Adding more weight to Ochre Dofus equivalent to 0.1 AP
        #it gives 1 AP if no damage has been received since the preceding turn
        ochre_dofus_new_stat_weight = objective_values.get('ap', 0) * 0.1
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Ochre Dofus').id, 
                               ochre_dofus_new_stat_weight)
        
        #Adding more weight to Emerald Dofus equivalent to
        #At the end of the turn, gives 100% of the owner's level in shield points
        #for each adjacent enemy. Summons are not counted.
        
        #Formula: Multiply by 0.5, since you get the bonus 50% of the time
        # Correct for level
        
        emerald_dofus_new_stat_weight = objective_values.get('hp', 0) * 0.5 * level
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Emerald Dofus').id, 
                               emerald_dofus_new_stat_weight)
        
        #Adding more weight to Vulbis Dofus equivalent to 7 Power
        #damage inflicted is increased by 10% for one turn if no damage has been received since the preceding turn.
        vulbis_dofus_new_stat_weight = objective_values.get('pow', 0) * 40.0 * level / 200
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Vulbis Dofus').id, 
                               vulbis_dofus_new_stat_weight)
         
        #Adding more weight to Abyssal Dofus equivalent to 1/2 AP + 1/2 MP
        #at the start of each turn, if no enemy is in close combat, it gives 1 MP. Otherwise, it gives 1 AP.
        abyssal_dofus_new_stat_weight = objective_values.get('ap', 0) * 0.5 + objective_values.get('mp', 0) * 0.5
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Abyssal Dofus').id, 
                               abyssal_dofus_new_stat_weight)
         
        #Adding more weight to Cawwot Dofus equivalent to 0.25 MP Loss Res + 0.25 AP Loss Res
        # it gives 25 AP Loss Resistance if an MP penalty is received, or 25 MP Loss Resistance if an AP penalty if received. These two effects can not combined.
        cawwot_dofus_new_stat_weight = objective_values.get('apres', 0) * 0.25 + objective_values.get('mpres', 0) * 0.25
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Cawwot Dofus').id, 
                               cawwot_dofus_new_stat_weight)
         
        #Adding more weight to Watchers Dofus equivalent to 10 heals
        #allies in alignment at the beginning of the turn get back 7% of their health points 
        watchers_dofus_new_stat_weight = (objective_values.get('heals', 0) * 10 + 2500) * level / 200.0
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Watchers Dofus').id, 
                               watchers_dofus_new_stat_weight)
        
        #Adding more weight to Thousand-League Boots equivalent to 1 MP
        #The bearer gains 2 MP on odd turns and loses 1 MP on even turns.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Thousand-League Boots').id, 
                               objective_values.get('mp', 0))
        
        #Adding more weight to Silver Dofus equivalent to some HP
        #At the start of the caster's turn, if they have less than 20% of their HP, they are healed by 20% of their HP. This effect can only be played once per fight.
        
        #Formula: expected life at lvl 200: 4500 - get 20% of that. 
        # Multiply by 0.2, since you wont get the bonus too often
        # Correct for level
        silver_dofus_new_stat_weight = objective_values.get('hp', 0) * (4500.0 * 20 / 100) * 0.2 * level / 200
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Silver Dofus').id, 
                               silver_dofus_new_stat_weight)
        
        #Adding more weight to Sparkling Silver Dofus equivalent to some HP
        #At the start of the caster's turn, if they have less than 20% of their HP, 
        #they are healed by they are healed 40% HP and gain 20% final damage for the current turn. 
        #This effect can only be played once per fight.
        
        #Formula: expected life at lvl 200: 4500 - get 40% of that. 
        # Add 30% power to simulate final damage
        # Multiply by 0.2, since you wont get the bonus too often
        # Correct for level
        sparkling_silver_dofus_new_stat_weight_hp = objective_values.get('hp', 0) * (4500.0 * 40 / 100) * 0.2 * level / 200
        sparkling_silver_dofus_new_stat_weight_pow = objective_values.get('power', 0) * (30) * 0.2
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Sparkling Silver Dofus').id, 
                               sparkling_silver_dofus_new_stat_weight_hp)
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Sparkling Silver Dofus').id, 
                               sparkling_silver_dofus_new_stat_weight_pow)
        
        #Adding more weight to Ebony Dofus equivalent to 60 Power * level / 200
        #Generates 1 first charge at the start of the turn, 1 second charge upon inflicting close-combat damage, and 1 third charge upon inflicting ranged damage.
        #Once 5 charges are reached, the next attack consumes the charges and applies a poison to the target for 3 turns.
        #Each charge gives a 2% final damage inflicted bonus.
        #Assuming one has an average of 3 charges, so 6% final damage bonus
        ebony_dofus_new_stat_weight = objective_values.get('pow', 0) * 60.0 * level / 200
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Ebony Dofus').id, 
                               ebony_dofus_new_stat_weight)
        
        
        #Adding more weight to Dorigami equivalent to 20 (avg vit weight) + lvl * 1.25
        #Applies 100% of level as Shield at the start of each turn for the first
        #5 turns. During each of these 5 turns, if the caster kills a summons, the
        #caster gains 100% of their level as Shield for 1 turn (max. 4 times), and
        #300% (max. 2 times) for a monster or player. Shields are only obtained 
        #during the caster's turn.
        dorigami_dofus_new_stat_weight = 20 * level * 1.25
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Dorigami').id, 
                               dorigami_dofus_new_stat_weight)
        
        
        #Adding more weight to Domakuro equivalent to dmg * 16
        #Starting on the 5th turn, the caster gains up to 64 damage for the rest of the fight.
        #This bonus is reduced each time the caster inflicts damage during their turn on an 
        #opponent for each of the first 4 turns of the fight: No attacks: 16 damage 
        #1 attack: 8 damage 2+ attacks: 0 damage.
        domakuro_dofus_new_stat_weight = (objective_values.get('neutdam', 0) + 
                                          objective_values.get('earthdam', 0) + 
                                          objective_values.get('firedam', 0) + 
                                          objective_values.get('airdam', 0) + 
                                          objective_values.get('waterdam', 0)) * 16
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Domakuro').id, 
                               domakuro_dofus_new_stat_weight)
        
        
        #Adding more weight to Rykke Errel's Bravery equivalent to 400 hp and -10% ranged damage
        #For each distance attack suffered, the bearer gains 200 shield and loses 5% ranged damage for 1 turn; stackable up to 5 times maximum.
        
        #Will consider 3 distance attacks each turn
        distance_attacks = 3
        rikke_new_stat_weight = objective_values.get('hp', 0) * 200 * distance_attacks - objective_values.get('perrandam', 0) * 5 * distance_attacks
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Rykke Errel's Bravery").id, 
                               rikke_new_stat_weight)
        
        #Adding more weight to Lady Jhessica's Belt equivalent to 25 Lock
        #At the end of their turn, the bearer removes 50 Dodge from adjacent enemies for 1 turn.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Lady Jhessica's Belt").id, 
                               objective_values.get('lock', 0) * 25)
        
        
        #Adding more weight to Kicked Ass Boots equivalent to 30 Dodge and 50 Pushback Damage
        #At the start of each turn, the wearer pushes entities in close combat back 1 cell.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Kicked Ass Boots").id, 
                               objective_values.get('dodge', 0) * 30 + objective_values.get('pshdam', 0) * 50)
        
        #Adding more weight to Jahash Jurgen's Cloak equivalent to 2.5% resists (1-2 hits on each element)
        #When the bearer suffers damage in an element, they gain 5% resistance in that element for 1 turn, stackable 5 times.
        resists_to_consider = 2.5
        jahash_new_stat_weight = (objective_values.get('neutresper', 0) * resists_to_consider
                                  + objective_values.get('airresper', 0) * resists_to_consider
                                  + objective_values.get('earthresper', 0) * resists_to_consider
                                  + objective_values.get('fireresper', 0) * resists_to_consider
                                  + objective_values.get('waterresper', 0) * resists_to_consider)
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Jahash Jurgen's Cloak").id, 
                               jahash_new_stat_weight)
        
        #Adding more weight to Ganymede's Diadem equivalent to 1 AP
        #The bearer gains 2 AP on even turns and loses 1 AP on odd turns.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Ganymede's Diadem").id, 
                               objective_values.get('ap', 0))
        
        #Adding more weight to Fallanster's Rectitude equivalent to 2% HP
        #The bearer gains a 10% reduction in damage suffered for 1 turn at the start of each turn. The bonus is removed as soon as the caster is moved.
        fallanster_new_stat_weight = objective_values.get('hp', 0) * (4500.0 * 2 / 100) * level / 200
        
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Fallanster's Rectitude").id, 
                               fallanster_new_stat_weight)
        
        #Adding more weight to Dodge's Audacity equivalent to 50 dodge
        #If the bearer suffers a Lock or does not move during their turn, the bearer becomes Unlockable on their next turn for 1 turn.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Dodge's Audacity").id, 
                               objective_values.get('dodge', 0) * 50)
        
        #Adding more weight to Death-Defying equivalent to nothing
        #Damage suffered by the bearer is increased by 15% whenever they have more than 50% HP, but damage suffered is reduced by 20% whenever they have less than 50% HP.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Death-Defying").id, 
                               objective_values.get('hp', 0) * 0)
        
        #Adding more weight to Crocobur equivalent to 200 HP * meleeness
        #The bearer steals health in their best attack element from adjacent enemies at the end of the turn.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Crocobur").id, 
                               objective_values.get('hp', 0) * 200 * objective_values.get('meleeness', 0))
        
        #Adding more weight to Buhorado Feather equivalent to 10 pushback damage
        #Whenever the bearer inflicts Critical Hits, they gain pushback damage for 2 turns, stackable 5 times.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Buhorado Feather").id, 
                               objective_values.get('pshdam', 0) * 10 * objective_values.get('ch', 0) / 100)
        
        #Adding more weight to Bram Worldbeard's Crown equivalent to 25 power
        #Whenever the bearer suffers an AP or MP removal, they gain 50 Power for 1 turn, stackable 10 times.
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name("Bram Worldbeard's Crown").id, 
                               objective_values.get('pow', 0) * 25)
        
        
        #adding random stats to dofusteuse
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Dofusteuse').id, 
                               objective_values.get('agi', 0) * 75)
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Dofusteuse').id, 
                               objective_values.get('cha', 0) * 75)
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Dofusteuse').id, 
                               objective_values.get('int', 0) * 75)
        self.problem.add_to_of('p', 
                               self.structure.get_item_by_name('Dofusteuse').id, 
                               objective_values.get('str', 0) * 75)
        #end
    def write_objective_function(self, objective_values, level):
        self.problem.init_objective_function()

        for stat, value in objective_values.iteritems():
            if stat != 'meleeness':
                stat_obj = self.structure.get_stat_by_key(stat)
                if stat_obj:
                    self.problem.add_to_of('stat', stat_obj.id, value)
                else:
                    print 'Could not find stat %s' % stat
        
        self.add_weird_item_weights_to_objective_funcion(objective_values, level)

        self.problem.finish_objective_function()
    
    #def add_objective_term(self, stat_name, weight):
    #    for item in self.items_list:
    #        for stat_id, value in item.stats:
    #            if self.structure.get_stat_name_by_id(stat_id) == stat_name:
    #                self.problem.add_to_of('x', item.id, value * weight)
    #    
    #    for item_set in self.sets_list:
    #        for num_items, stat_id, value in item_set.bonus:
    #            if self.structure.get_stat_name_by_id(stat_id) == stat_name:
    #                self.problem.add_to_of('ss', '%d_%d' % (set.id, num_items + 1), value * weight)
    
    def create_constraints(self):
        self.create_type_constraints()
        self.create_presence_constraints()
        self.create_level_constraints()
        self.create_set_constraints()
        self.create_stat_total_constraints()
        self.create_condition_contraints()
        self.create_minimum_stat_constraints()
        self.create_advanced_minimum_stat_constraints()
        self.create_locked_equip_constraints()
#        self.create_two_handed_constraints()
        self.create_forbidden_items_constraints()
        self.create_stats_points_constraints()
        self.create_light_set_constraints()
        
    def setup(self, model_input):
        self.input = model_input.get_old_input()

        self.modify_level_constraints(model_input.char_level)
        self.modify_stat_total_constraints(model_input.base_stats_by_attr,
                                           model_input.options)
        self.modify_minimum_stat_constraints(model_input.minimum_stats, 
                                             model_input.char_level)
        self.modify_locked_equip_constraints(model_input.locked_equips)
        self.modify_forbidden_items_constraints(model_input.forbidden_equips,
                                                model_input.options)
        self.modify_stats_points_constraints(model_input.char_class,
                                             model_input.stat_points_to_distribute)
        
        self.write_objective_function(model_input.objective_values, model_input.char_level)
    
    def create_type_constraints(self):
        types_list = self.structure.get_types_list()
        for item_type in types_list:
            items_of_type = []
            for item in self.items_list:
                if self.structure.get_type_name_by_id(item.type) == item_type:
                    items_of_type.append(item)
            restriction = self.problem.restriction_lt_eq(TYPE_NAME_TO_SLOT_NUMBER[item_type],
                                                        [(1, 'x', item_entry.id) for item_entry in items_of_type])
            self.restrictions.type_constraints[item_type] = restriction
                                              
#     def create_two_handed_constraints(self):
#         one_handed_items = []
#         for item in self.items_list:
#             if item.is_one_handed:
#                 one_handed_items.append(item)
#         for item in self.items_list:
#             if self.structure.get_type_name_by_id(item.type) == 'Shield':
#                 restriction = self.problem.restriction_lt_eq(0, [(-1, 'p', item_entry.id) for item_entry in one_handed_items] + [(1, 'p', item.id)])
#                 self.restrictions.two_handed_constraints[item.id] = restriction
    
    def create_presence_constraints(self):
        for item in self.items_list:
            restriction1 = self.problem.restriction_lt_eq(0, [(1, 'p', item.id),
                                                              (-1, 'x', item.id)])
            restriction2 = self.problem.restriction_lt_eq(0, [(-2, 'p', item.id),
                                                              (1, 'x', item.id)])
            self.restrictions.first_presence_constraints[item.id] = restriction1
            self.restrictions.second_presence_constraints[item.id] = restriction2
            

    def create_level_constraints(self):
        for item in self.items_list:
            restriction = self.problem.restriction_lt_eq(0, [(1, 'p', item.id)])
            self.restrictions.level_constraints[item.id] = restriction
    
    def modify_level_constraints(self, char_level):
        for item in self.items_list:
            restriction = self.restrictions.level_constraints.get(item.id, None)
            restriction.changeRHS(0 if char_level < item.level else 1)
    
    def create_forbidden_items_constraints(self):
        for item in self.items_list:
            restriction = self.problem.restriction_lt_eq(0, [(1, 'p', item.id)])  
            self.restrictions.forbidden_items_constraints[item.id] = restriction
    
    def create_stats_points_constraints(self):
        for stat in self.main_stats_list:
            self.restrictions.first_stats_points_constraints[stat.key] = {}
            self.restrictions.second_stats_points_constraints[stat.key] = {}
            self.restrictions.third_stats_points_constraints[stat.key] = {}
            for i in xrange(1, 6):
                restriction = self.problem.restriction_lt_eq(1990, [(-1, 'stat_point', 'statpoint_%d_%d' % (i, stat.id)),
                                                                    (1990, 'stat_point_max', 'statpointmax_%d_%d' % (i-1, stat.id))])  
                self.restrictions.first_stats_points_constraints[stat.key][i] = restriction
            for i in xrange(0, 6):
                restriction = self.problem.restriction_lt_eq(0, [(1, 'stat_point', 'statpoint_%d_%d' % (i, stat.id))])  
                self.restrictions.second_stats_points_constraints[stat.key][i] = restriction
            for i in xrange(0, 5):
                restriction = self.problem.restriction_lt_eq(0, [(-1, 'stat_point', 'statpoint_%d_%d' % (i, stat.id)),
                                                              (-2000, 'stat_point_max', 'statpointmax_%d_%d' % (i, stat.id))]) 
                self.restrictions.third_stats_points_constraints[stat.key][i] = restriction 
        matrix = []
        for stat in self.main_stats_list:
            matrix.extend([(0.5, 'stat_point', 'statpoint_0_%d' % stat.id),
                           (1, 'stat_point', 'statpoint_1_%d' % stat.id),
                           (2, 'stat_point', 'statpoint_2_%d' % stat.id),
                           (3, 'stat_point', 'statpoint_3_%d' % stat.id),
                           (4, 'stat_point', 'statpoint_4_%d' % stat.id),
                           (5, 'stat_point', 'statpoint_5_%d' % stat.id)])
        restriction = self.problem.restriction_lt_eq(0, matrix)
        self.restrictions.fourth_stats_points_constraint = restriction 

    def modify_stats_points_constraints(self, char_class, stat_points):
        for stat in SOFT_CAPS[char_class]:
            for i in xrange(0, 6):
                restrictions = self.restrictions.second_stats_points_constraints.get(stat, None)
                restriction = restrictions.get(i, None)
                if i >= 1 and (SOFT_CAPS[char_class][stat][i-1] is not None) and (SOFT_CAPS[char_class][stat][i] is not None):
                    max_cap = (SOFT_CAPS[char_class][stat][i] - SOFT_CAPS[char_class][stat][i-1])
                else: 
                    max_cap = SOFT_CAPS[char_class][stat][i]
                restriction.changeRHS(max_cap if max_cap is not None else 1991)
              
            for i in xrange(0, 5):  
                restrictions = self.restrictions.third_stats_points_constraints.get(stat, None)
                restriction = restrictions.get(i, None)
                if i >= 1 and (SOFT_CAPS[char_class][stat][i-1] is not None) and (SOFT_CAPS[char_class][stat][i] is not None):
                    max_cap = (SOFT_CAPS[char_class][stat][i] - SOFT_CAPS[char_class][stat][i-1])
                else: 
                    max_cap = SOFT_CAPS[char_class][stat][i]
                restriction.changeRHS(-max_cap if max_cap is not None else -1991)
              
        restriction = self.restrictions.fourth_stats_points_constraint
        restriction.changeRHS(stat_points)    
    
    def modify_forbidden_items_constraints(self, forbidden_equips, options):
        new_forbid_list = forbidden_equips
        
        or_items = self.structure.get_available_or_items()
        for _, or_item_items in or_items.iteritems():
            for item in or_item_items:
                if item.id in forbidden_equips:
                    for or_item in or_item_items:
                        new_forbid_list.add(or_item.id)

        for item in self.items_list:
            restriction = self.restrictions.forbidden_items_constraints.get(item.id, None)
            if ((item.id in new_forbid_list) 
                #or (options['shields'] == False and item.type == self.structure.get_type_id_by_name('Shield'))
                or (options['dofus'] == 'lightset' 
                    and item.type == self.structure.get_type_id_by_name('Dofus')
                    and item.weird_conditions['light_set']) 
                or (options['dofus'] == False 
                    and item.type == self.structure.get_type_id_by_name('Dofus'))
                or (options['dofus'] == 'cawwot' 
                    and item.type == self.structure.get_type_id_by_name('Dofus'))
                    and item.id != self.structure.get_item_by_name('Cawwot Dofus').id
                or ((not options['dragoturkey'])
                    and item.type == self.structure.get_type_id_by_name('Pet'))
                    and 'Dragoturkey' in item.name
                or ((not options['seemyool'])
                    and item.type == self.structure.get_type_id_by_name('Pet'))
                    and 'Seemyool' in item.name
                or ((not options['rhineetle'])
                    and item.type == self.structure.get_type_id_by_name('Pet'))
                    and 'Rhineetle' in item.name):
                restriction.changeRHS(0)
            else:
                restriction.changeRHS(1)
        gelano1 = self.structure.get_item_by_name('Gelano (#1)')
        gelano2 = self.structure.get_item_by_name('Gelano (#2)')
        restriction = self.restrictions.forbidden_items_constraints.get(gelano2.id, None)
        restriction.changeRHS(0 if options['mp_exo'] == 'gelano' else 1)
        restriction = self.restrictions.forbidden_items_constraints.get(gelano1.id, None)
        restriction.changeRHS(1 if options['mp_exo'] == 'gelano' else 0)
    
    def create_locked_equip_constraints(self):
        for item in self.items_list:
            restriction = self.problem.restriction_lt_eq(-1, [(-1, 'x', item.id)])
            self.restrictions.locked_equip_constraints[item.id] = restriction
        or_items = self.structure.get_available_or_items()
        for item_name in or_items:
            restriction2 = self.problem.restriction_lt_eq(-1, [(-1, 'x', item.id) for item in or_items[item_name]])
            self.restrictions.locked_equip_constraints[item_name] = restriction2

    def modify_locked_equip_constraints(self, locked_equips):
        locked_equip_values = []
        for item in locked_equips.values():
                locked_equip_values.append(item)
        locked_dic = Counter(locked_equip_values)
        locked_dic_names = Counter(locked_equips.values())
        or_items = self.structure.get_available_or_items()
        for item_id, occurrences in locked_dic.iteritems():
            if occurrences > 1 and item_id != '':
                item = self.structure.get_item_by_id(item_id)
                locked_dic[item_id] = 2 if self.structure.get_type_name_by_id(item.type) == 'Ring' and item.set == None else 1
        for item_name, occurrences in locked_dic_names.iteritems():
            if occurrences > 1 and item_name != '':
                if item_name in or_items:
                    item = or_items[item_name].get(0)
                    locked_dic_names[item_name] = 2 if self.structure.get_type_name_by_id(item.type) == 'Ring' and item.set == None else 1
        
        
        for item in self.items_list:
            restriction = self.restrictions.locked_equip_constraints[item.id]
            restriction.changeRHS(-locked_dic[item.id] if item.id in locked_equip_values else 0)
        for item_name in or_items:
            restriction = self.restrictions.locked_equip_constraints[item_name]
            restriction.changeRHS(-locked_dic_names[item_name] if item_name in locked_equips.values() else 0)
            
    def create_set_constraints(self):
        for item_set in self.sets_list:
            
            valid_items_in_set = []
            s = get_structure()
            for item in item_set.items:
                if not s.get_item_by_id(item).removed:
                    valid_items_in_set.append(item)
            restriction = self.problem.restriction_eq(0, [(1, 'x', item) for item in valid_items_in_set]
                                                            + [(-1, 's', item_set.id)])
            self.restrictions.first_set_constraints[item_set.name] = restriction
        
        for item_set in self.sets_list:
            restrictions_list = []
            for slot in xrange (1, 9):
                restriction = self.problem.restriction_lt_eq(0, [(slot, 'ss', '%d_%d' % (item_set.id, slot + 1)), (-1, 's', item_set.id)])   
                restrictions_list.append(restriction)
            self.restrictions.second_presence_constraints[item_set.name] = restrictions_list

        for item_set in self.sets_list:
            restriction = self.problem.restriction_eq(1, [(1, 'ss', '%d_%d' % (item_set.id, slot + 1)) for slot in xrange (0, 9)]) 
            self.restrictions.third_set_constraints[item_set.name] = restriction
        
        for item_set in self.sets_list:
            restrictions_list = []
            for slot in xrange (0, 9):
                restriction = self.problem.restriction_lt_eq(8 + slot,
                                                             [(8, 'ss', '%d_%d' % (item_set.id, slot + 1)),
                                                              (1, 's', item_set.id)])
                restrictions_list.append(restriction)
            self.restrictions.fourth_set_constraints[item_set.name] = restrictions_list
    
    def create_light_set_constraints(self):
        MAX_SETS_ONE_CAN_EQUIP = len(self.sets_list)
        matrix = [(1, 'ss', '%d_%d' % (item_set.id, 2 + 1)) for item_set in self.sets_list]
        matrix.append((-MAX_SETS_ONE_CAN_EQUIP, 'ytrophy', 1))
        restriction = self.problem.restriction_lt_eq(1, matrix) 
        self.restrictions.first_light_set_constraint = restriction
        
        restriction = self.problem.restriction_lt_eq(MAX_SETS_ONE_CAN_EQUIP, [(MAX_SETS_ONE_CAN_EQUIP, 'ytrophy', 1), 
                                                                              (1, 'trophies', 1)]) 
        self.restrictions.second_light_set_constraint = restriction
        
        plist = []
        for slot in xrange(3, 9):
            plist.extend([(1, 'ss', '%d_%d' % (item_set.id, slot + 1)) for item_set in self.sets_list])
        plist.append((-MAX_SETS_ONE_CAN_EQUIP, 'ytrophy', 2))
        restriction = self.problem.restriction_lt_eq(0, plist)
        self.restrictions.third_light_set_constraint = restriction
        
        restriction = self.problem.restriction_lt_eq(MAX_SETS_ONE_CAN_EQUIP, [(MAX_SETS_ONE_CAN_EQUIP, 'ytrophy', 2), 
                                                                              (1, 'trophies', 1)]) 
        self.restrictions.fourth_light_set_constraint = restriction
    
        plist = []
        for item in self.items_list:
            if item.weird_conditions['light_set']:
                plist.append((1, 'x', item.id))
        #This will only work while all the items with this condition are trophies
        MAXIMUM_TROPHIES = 6
        plist.append((-MAXIMUM_TROPHIES, 'trophies', 1))

        restriction = self.problem.restriction_lt_eq(0, plist) 
        self.restrictions.fifth_light_set_constraint = restriction
        
    def create_condition_contraints(self):
        for item in self.items_list:
            for stat, value in item.min_stats_to_equip:
                restriction = self.problem.restriction_lt_eq(10000,
                                                            [(value + 10000, 'p', item.id),
                                                             (-1, 'stat', stat)])
                self.restrictions.min_condition_contraints[(item.id, stat)] = restriction 
            
        for item in self.items_list:
            for stat, value in item.max_stats_to_equip:
                restriction = self.problem.restriction_lt_eq(100000 + value,
                                                             [(100000, 'p', item.id),
                                                              (1, 'stat', stat)])
                
                self.restrictions.max_condition_contraints[(item.id, stat)] = restriction                     

    def create_stat_total_constraints(self):
        for stat in self.stats_list:
            matrix = [(-1, 'stat', stat.id)]
            for item in self.items_list:
                for stat_id, value in item.stats:
                    if stat_id == stat.id:
                        matrix.append((value, 'x', item.id))
            for item_set in self.sets_list:
                for num_items, stat_id, value in item_set.bonus:
                    if stat_id == stat.id:
                        matrix.append((value, 'ss', '%d_%d' % (item_set.id, num_items + 1)))
            if stat in self.main_stats_list:
                for i in xrange(0, 6):
                    matrix.append((1, 'stat_point', 'statpoint_%d_%d' % (i, stat.id)))
            restriction = self.problem.restriction_eq(0, matrix)
            self.restrictions.stat_total_constraints[stat.name] = restriction

    def modify_stat_total_constraints(self, base_stats_by_attr, options):
        for stat in self.stats_list:
            restriction = self.restrictions.stat_total_constraints[stat.name]
            value = base_stats_by_attr.get(stat.name, 0)
            if stat.key == 'ap' and options['ap_exo']:
                value += 1
            elif stat.key == 'range' and options['range_exo']:
                value += 1
            elif stat.key == 'mp' and options['mp_exo'] == True:
                value += 1
            restriction.changeRHS(-value)

    def create_minimum_stat_constraints(self):
        dependencies = {'Dodge': [['Agility'],[0.1]],
                        'Lock': [['Agility'],[0.1]],
                        'AP Reduction': [['Wisdom'],[0.1]],
                        'MP Reduction': [['Wisdom'],[0.1]],
                        'AP Loss Resist': [['Wisdom'],[0.1]],
                        'MP Loss Resist': [['Wisdom'],[0.1]],
                        'Initiative': [['Agility', 'Intelligence', 'Strength', 'Chance'],
                                       [1, 1, 1, 1]],
                        'Prospecting': [['Chance'],[0.1]],
                        'Pods': [['Strength'],[5]],
                        'HP': [['Vitality'],[1]]}

        for stat in self.stats_list:
            if stat.name in dependencies:
                sec_stats = dependencies[stat.name][0]
                sec_stats_multipliers = dependencies[stat.name][1]
                matrix = []
                matrix.append((-1, 'stat', stat.id))
                for (i, sec_stat) in enumerate(sec_stats):
                    matrix.append((-sec_stats_multipliers[i], 
                                    'stat', 
                                    self.structure.get_stat_by_name(sec_stat).id))
                restriction = self.problem.restriction_lt_eq(-10000, matrix) 
            else:
                restriction = self.problem.restriction_lt_eq(-10000, [(-1, 'stat', stat.id)])  
            self.restrictions.minimum_stat_constraints[stat.name] = restriction
    
    def create_advanced_minimum_stat_constraints(self):
        adv_mins = self.structure.get_adv_mins()        
        
        for stat in adv_mins:
            matrix = []
            for stat_name in stat['stats']:
                matrix.append((-1, 'stat', self.structure.get_stat_by_name(stat_name).id))
            restriction = self.problem.restriction_lt_eq(-10000, matrix)   
            self.restrictions.advanced_minimum_stat_constraints[stat['key']] = restriction

    def modify_minimum_stat_constraints(self, minimum_stats, level):
        for stat in self.stats_list:
            if stat.name == 'HP':
                restriction = self.restrictions.minimum_stat_constraints[stat.name]
                restriction.changeRHS(-minimum_stats.get(stat.name, -10000) + 55 + 5*(level-1))
            else:
                restriction = self.restrictions.minimum_stat_constraints[stat.name]
                restriction.changeRHS(-minimum_stats.get(stat.name, -10000))
        self.modify_advanced_minimum_stat_constraints(minimum_stats.get('adv_mins', {}))
    
    def modify_advanced_minimum_stat_constraints(self, minimum_stats):
        adv_min_stats = self.structure.get_adv_mins()
        for stat in adv_min_stats:
            restriction = self.restrictions.advanced_minimum_stat_constraints[stat['key']]
            restriction.changeRHS(-minimum_stats.get(stat['name'], -10000))
    
    def run(self, retries=0, change_of=False):
        if change_of:
            self.input['objective_values']['vit'] += 1
            self.write_objective_function(self.input['objective_values'], self.input['char_level'])
        try:
            self.problem.run()
        except PulpSolverError:
            if retries > 0:            
                self.run(retries-1, True)
            else:
                raise
                
    def get_result_string(self):
        if self.problem.get_status() == 'Infeasible':
            return 'Infeasible'
        
        result = ''
        
        lp_vars = self.problem.get_result()
        grouped_vars = {}
        for k, v in lp_vars.iteritems():
            prefix, suffix = k.split('_', 1)
            group = grouped_vars.setdefault(prefix, {})
            group[suffix] = v
                
        result += ', '.join(grouped_vars) + '\n\n'
        
        result += 'Sets:\n'
        for k, v in grouped_vars['ss'].iteritems():
            if v > 0:
                set_id, number_of_pieces = k.rsplit('_', 1)
                set_id = int(set_id)
                number_of_pieces = int(number_of_pieces) - 1
                if number_of_pieces > 1:
                    result += ('%s (%d pieces)\n' % (self.structure.get_set_by_id(set_id).name, number_of_pieces))
        result += '\nStats:\n'
        for stat in self.stats_list:
            result += '%s: %d\n' % (stat.name, grouped_vars['stat'][str(stat.id)])

        result += '\nGear:\n'
        for k, v in grouped_vars['x'].iteritems():
            for _ in range(int(v)):
                result += self.structure.get_item_by_id(int(k)).name + '\n'
        return result
        
    def get_stats(self):
        lp_vars = self.problem.get_result()
        
        stats = {}
        for stat in self.main_stats_list: 
            stats[stat.key] = 0
            for i in xrange(0,6):
                stats[stat.key] += int(lp_vars['stat_point_statpoint_%d_%d' % (i, stat.id)])
                #print '%s: tier %d - %d' % (stat.name, i, lp_vars['stat_point_statpoint_%d_%d' % (i, stat.id)])
                #if i < 5:                
                #    print 'y %s: tier %d - %d' % (stat.name, i, lp_vars['stat_point_max_statpointmax_%d_%d' % (i, stat.id)])
        return stats
        
    def get_result_minimal(self):
        item_id_list = []
   
        lp_vars = self.problem.get_result()
        grouped_vars = {}
        for k, v in lp_vars.iteritems():
            prefix, suffix = k.split('_', 1)
            group = grouped_vars.setdefault(prefix, {})
            group[suffix] = v
        
        for k, v in grouped_vars['x'].iteritems():
            for _ in range(int(v)):
                item = int(k)
                item_id_list.append(item)
                
        result = ModelResultMinimal.from_item_id_list(item_id_list, self.input, self.get_stats())
        return result

    def get_solved_status(self):
        return self.problem.get_status()


class ModelInput(object):

    def __init__(self, char_level, base_stats_by_attr, minimum_stats, locked_equips,
                 forbidden_equips, objective_values, options, char_class,
                 stat_points_to_distribute):
        self.char_level = char_level
        self.base_stats_by_attr = base_stats_by_attr
        self.minimum_stats = minimum_stats
        self.locked_equips = locked_equips
        self.forbidden_equips = forbidden_equips
        self.objective_values = objective_values
        self.options = options
        self.char_class = char_class
        self.stat_points_to_distribute = stat_points_to_distribute

    def get_old_input(self):
        return {'char_level': self.char_level,
                'base_stats_by_attr': self.base_stats_by_attr,
                'minimum_stats': self.minimum_stats,
                'locked_equips': self.locked_equips,
                'forbidden_equips': self.forbidden_equips,
                'objective_values': self.objective_values,
                'options': self.options,
                'origin': 'generated'}

    def __hash__(self, *args, **kwargs):
        return (self.char_level,
                freeze(self.base_stats_by_attr),
                frozenset([p for p in self.minimum_stats.items() if p[0] != 'adv_mins']),
                freeze(self.minimum_stats.get('adv_mins')),
                freeze(self.locked_equips),
                frozenset(self.forbidden_equips),
                freeze(self.objective_values),
                freeze(self.options),
                self.char_class,
                self.stat_points_to_distribute).__hash__()

def freeze(d):
    if d is None:
        return None
    else:
        return frozenset(d.items())
