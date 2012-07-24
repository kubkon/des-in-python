#!/usr/bin/env python
# encoding: utf-8
"""
SimulationEngine.py

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
import unittest
import random

from Clock import *
from Event import *
from EventHandler import *


class SimulationEngine(object):
  '''
  Represents the main engine of a DES simulation platform
  '''
  def __init__(self):
    '''
    Constructs SimulationEngine instance
    '''
    # Create empty event list
    self._event_list = []
    # Create clock
    self._clock = Clock()
    # Initialize finish time
    self._finish_time = 0
    # Flag representing finishing event
    self._finish_event_exists = False
    # Initialize event handler
    self._event_handler = None
  
  @property
  def event_handler(self):
    '''
    Returns registered event handler
    '''
    return self._event_handler
  
  @event_handler.setter
  def event_handler(self, event_handler):
    '''
    Registers event handler
    
    Keyword arguments:
    event_handler -- Event handler to be used
    '''
    self._event_handler = event_handler
  
  def start(self):
    '''
    Starts simulation
    '''
    # Schedule first event
    self._event_handler.generate_event(self._clock.simulation_time)
    # Traverse the event list
    while len(self._event_list) > 0:
      # Remove the imminent event from the event list
      imminent = self._event_list.pop()
      # Advance clock to the imminent event
      self._clock.simulation_time = imminent.time
      # Pass the imminent event to the event handler
      self._event_handler.handle_event(imminent)
      # Schedule any additional events
      self._event_handler.generate_event(self._clock.simulation_time)
  
  def stop(self, finish_time):
    '''
    Schedules finishing event
    
    Keyword arguments:
    finish_time -- Time of occurrence of the finishing event
    '''
    # Check if finishing event already scheduled
    if not self._finish_event_exists:
      # Set finish time
      self._finish_time = finish_time
      # Schedule finishing event
      self._event_list += [Event("End", self._finish_time)]
      self._finish_event_exists = True
      # Sort the list so that finishing event is first (LIFO)
      self._event_list.sort(key=lambda x: x.time)
      self._event_list.reverse()
  
  def schedule(self, event):
    '''
    Schedules event (adds it to the event list)
    
    Keyword arguments:
    event -- Event to be scheduled
    '''
    # Discard new event if happens after the finishing event
    if event.time < self._finish_time:
      # Add the event to the event list
      self._event_list += [event]
      # Sort the list in a LIFO style
      self._event_list.sort(key=lambda x: x.time)
      self._event_list.reverse()
  

class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    # Create new simulation
    self.sim = SimulationEngine()
  
  def test_event_handler(self):
    eh = EventHandler(self.sim)
    self.sim.event_handler = eh
    self.assertEquals(self.sim.event_handler, eh)


if __name__ == '__main__':
  unittest.main()