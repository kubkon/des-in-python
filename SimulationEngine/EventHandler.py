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

from abc import ABCMeta, abstractmethod
from .SimulationEngineFactory import *


class EventHandler(metaclass=ABCMeta):
  '''
  Abstract base class for event handlers
  '''
  def __init__(self):
    '''
    Constructs EventHandler object
    '''
    # Get instance of SimulationEngine object
    self._simulation_engine = SimulationEngineFactory.get_instance()
    # Register callback functions:
    # start of the simulation
    self._simulation_engine.register_callback(self._handle_start, SimulationEngine.START_CALLBACK)
    # stop of the simulation
    self._simulation_engine.register_callback(self._handle_stop, SimulationEngine.STOP_CALLBACK)
    # imminent event
    self._simulation_engine.register_callback(self._handle_event, SimulationEngine.EVENT_CALLBACK)
  
  @abstractmethod
  def _handle_start(self):
    '''
    Abstract method for handling start of the simulation
    '''
    pass
  
  @abstractmethod
  def _handle_stop(self):
    '''
    Abstract method for handling stop of the simulation
    '''
    pass
  
  @abstractmethod
  def _handle_event(self, event):
    '''
    Abstract method for handling imminent events
    
    Keyword arguments:
    event -- Event to be handled
    '''
    pass
  
