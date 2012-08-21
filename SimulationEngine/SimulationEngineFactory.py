#!/usr/bin/env python
# encoding: utf-8
"""
SimulationEngineFactory.py

Created by Jakub Konka on 2012-08-21.
Copyright (c) 2012 Jakub Konka.

This library is free software; you can redistribute it and/or
modify under the terms of the GNU General Public License as
published by the Free Software Foundation; version 3.0.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this library; if not, visit
http://www.gnu.org/licenses/gpl-3.0.html
"""

from .SimulationEngine import *


class SimulationEngineFactory(object):
  '''
  Factory class for creating SimulationEngine objects;
  mimicks singleton design pattern
  '''
  # Stored instance of SimulationEngine class
  _INSTANCE = None
  
  @classmethod
  def get_instance(cls):
    '''
    Returns an instance of SimulationEngine object
    '''
    if SimulationEngineFactory._INSTANCE is None:
      SimulationEngineFactory._INSTANCE = SimulationEngine()
    return SimulationEngineFactory._INSTANCE
  

class SimulationEngineFactoryTests(unittest.TestCase):
  def setUp(self):
    self.sim = SimulationEngineFactory.get_instance()
  
  def test_singleton_like_behaviour(self):
    sim = SimulationEngineFactory.get_instance()
    self.assertEqual(self.sim, sim)
  

if __name__ == '__main__':
  unittest.main()