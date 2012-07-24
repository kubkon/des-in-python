#!/usr/bin/env python
# encoding: utf-8
"""
EventHandler.py

Created by Jakub Konka on 2012-07-23.
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

import sys
import os


class EventHandler(object):
  '''
  Abstract base class for event handlers
  '''
  def __init__(self, simulation_engine):
    '''
    Constructs EventHandler object
    '''
    self._simulation_engine = simulation_engine
  
  def generate_event(self, simulation_time):
    '''
    Abstract method for generating events
    
    Keyword arguments:
    simulation_time -- Current simulation time
    '''
    raise NotImplementedError("Method generate_event needs to be implemented")
  
  def handle_event(self, event):
    '''
    Abstract method for handling events
    
    Keyword arguments:
    event -- Event to be handled
    '''
    raise NotImplementedError("Method generate_event needs to be implemented")
  
