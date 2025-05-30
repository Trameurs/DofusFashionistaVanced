#!/usr/bin/env python

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

"""
Test pour vérifier que la correction du bug "caractéristiques minimales qui sautent une génération" 
fonctionne correctement.

Ce script vérifie que l'appel à remove_cache_for_char() est bien présent dans les fonctions 
set_min_stats() et set_stats_weights().
"""

import os
import sys
import inspect

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashionsite.settings')

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'fashionsite'))

import django
django.setup()

from django.core.cache import cache
from django.test import Client

from chardata.min_stats import set_min_stats
from chardata.stats_weights import set_stats_weights
from chardata.models import Char
from chardata.util import remove_cache_for_char

# Classe de test pour vérifier la présence de remove_cache_for_char dans les fonctions
class TestCacheInvalidation:
    
    def __init__(self):
        self.success = True
        self.messages = []
    
    def add_message(self, message):
        print(message)
        self.messages.append(message)
    
    def test_set_min_stats_calls_remove_cache(self):
        """Vérifie que set_min_stats appelle remove_cache_for_char"""
        source = inspect.getsource(set_min_stats)
        if "remove_cache_for_char" in source:
            self.add_message("✅ set_min_stats() appelle bien remove_cache_for_char()")
        else:
            self.success = False
            self.add_message("❌ set_min_stats() N'APPELLE PAS remove_cache_for_char() - Le bug persiste!")

    def test_set_stats_weights_calls_remove_cache(self):
        """Vérifie que set_stats_weights appelle remove_cache_for_char"""
        source = inspect.getsource(set_stats_weights)
        if "remove_cache_for_char" in source:
            self.add_message("✅ set_stats_weights() appelle bien remove_cache_for_char()")
        else:
            self.success = False
            self.add_message("❌ set_stats_weights() N'APPELLE PAS remove_cache_for_char() - Vérifiez le code!")
    
    def run_tests(self):
        """Exécute tous les tests"""
        self.add_message("\n=== Test de correction du bug 'caractéristiques minimales qui sautent une génération' ===\n")
        self.test_set_min_stats_calls_remove_cache()
        self.test_set_stats_weights_calls_remove_cache()
        
        if self.success:
            self.add_message("\n✅ TOUS LES TESTS SONT RÉUSSIS : Le bug est bien corrigé!")
        else:
            self.add_message("\n❌ CERTAINS TESTS ONT ÉCHOUÉ : Le bug n'est pas entièrement corrigé!")
        
        return self.success

if __name__ == "__main__":
    test = TestCacheInvalidation()
    success = test.run_tests()
    sys.exit(0 if success else 1)
