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

from fashionista_config import get_fashionista_path
from pulp import LpVariable, LpInteger, LpProblem, LpMaximize, LpStatus, value
from pulp.solvers import COIN_CMD

import os
import uuid


SOLVER = COIN_CMD(path=get_fashionista_path() + '/fashionistapulp/fashionistapulp/cbc',
                  maxSeconds=90,
                  keepFiles=True)

class LpProblem2:
    
    def __init__(self):
        self.pulp_vars = {}
        #self.model_output = open('model.txt', 'w')
        self.pulp_lp = LpProblem("The Whiskas Problem", LpMaximize)
        
    def run(self):
        problem_name = '/tmp/problem_%s' % str(uuid.uuid4())
        self.pulp_lp.name = problem_name
        self.pulp_lp.solve(SOLVER)
        print 'Status: %s, Z = %g' % (LpStatus[self.pulp_lp.status], value(self.pulp_lp.objective))
        
        tmpMps = os.path.join('%s-pulp.mps' % problem_name)
        tmpSol = os.path.join('%s-pulp.sol' % problem_name)
        try: os.remove(tmpMps)
        except: print 'could not remove file %s' % tmpMps
        try: os.remove(tmpSol)
        except: print 'could not remove file %s' % tmpSol

    def get_result(self):
        return {v.name: v.varValue for v in self.pulp_lp.variables()}

    def setup_variable(self, category, id, min_bound, max_bound):
        name = '%s_%s' % (category, str(id))
        pulpVar = LpVariable(name, min_bound, max_bound, LpInteger)
        
        self.pulp_vars[name] = pulpVar

    def init_objective_function(self):
        self.obj_vars = {}

    def add_to_of(self, category, id, weight):
        var_name = '%s_%s' % (category, str(id))
        if self.obj_vars.get(var_name) == None:
            self.obj_vars[var_name] = weight
        else:
            self.obj_vars[var_name] += weight

    def finish_objective_function(self):
        self.pulp_lp += sum([value * self.pulp_vars[key] for key, value in
                             self.obj_vars.iteritems()])
        
    def restriction_lt_eq(self, max_bound, parcels):
        restriction = sum([parcel[0] * self.pulp_vars['%s_%s' % (parcel[1], str(parcel[2]))] 
                            for parcel in parcels]) <= max_bound
        self.pulp_lp += restriction
        return restriction
        

    def restriction_eq(self, max_bound, parcels):
        restriction = sum([parcel[0] * self.pulp_vars['%s_%s' % (parcel[1], str(parcel[2]))] 
                            for parcel in parcels]) == max_bound
        self.pulp_lp += restriction
        return restriction
        
    def get_status(self):
        return LpStatus[self.pulp_lp.status]
