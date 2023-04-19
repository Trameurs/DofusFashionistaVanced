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
from threading import Lock

from Queue import Queue

MAX_MODELS = 2
lock = Lock()
model_queue = Queue()
models_created = 0

def create_model():
    #print 'create_model start'
    global models_created
    with lock:
        models_created += 1
    new_model = Model()
    model_queue.put(new_model)
    #print 'create_model end'

def borrow_model():
    #print 'borrow_model'
    if model_queue.empty() and models_created < MAX_MODELS:
        create_model()

    #print '%d models are created' % models_created

    return model_queue.get()
    
def return_model(borrowed_model):
    #print 'return_model'
    model_queue.put(borrowed_model)
