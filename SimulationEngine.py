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


class SimulationEngine:
  '''
  Represents the main engine of a DES simulation platform
  '''
  def __init__(self):
    '''
    Constructs SimulationEngine instance
    '''
    # Create empty event list
    self.event_list = []
    # Create clock
    self.clock = Clock()
    # Initialize finish time
    self.finish_time = 0
    # Flag representing finishing event
    self.finish_event_exists = False
  
  def start(self):
    '''
    Starts simulation
    '''
    # Schedule first event
    self._schedule(Event(self.clock.simulation_time))
    # Traverse the event list
    while len(self.event_list) > 0:
      # Remove the imminent event from the event list
      imminent = self.event_list.pop()
      # Advance clock to the imminent event
      self.clock.simulation_time = imminent.time
      # Execute the imminent event
      imminent.trigger_action()
      # Schedule any additional events
      delta_time = random.randint(1, 5)
      self._schedule(Event(self.clock.simulation_time + delta_time))
  
  def stop(self, finish_time):
    '''
    Schedules finishing event
    
    Keyword arguments:
    finish_time -- Time of occurrence of the finishing event
    '''
    # Check if finishing event already scheduled
    if not self.finish_event_exists:
      self.finish_time = finish_time
      # Remove any scheduled event with time of occurrence
      # exceeding the time of occurrence of the finishing
      # event
      removed = filter(lambda e: e.time > self.finish_time, self.event_list)
      if len(removed) > 0:
        self.event_list = [e for e in self.event_list if e not in removed]
      # Schedule finishing event
      self.event_list += [Event(self.finish_time)]
      self.finish_event_exists = True
      # Sort the list so that finishing event is first (LIFO)
      self.event_list.sort(key=lambda x: x.time)
      self.event_list.reverse()
  
  def _schedule(self, event):
    '''
    Schedules event (adds it to the event list)
    
    Keyword arguments:
    event -- Event to be scheduled
    '''
    # Discard new event if happens after the finishing event
    if event.time < self.finish_time:
      # Add the event to the event list
      self.event_list += [event]
      # Sort the list in a LIFO style
      self.event_list.sort(key=lambda x: x.time)
      self.event_list.reverse()
  

class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    # Create new simulation
    self.sim = SimulationEngine()
  
  def test_simulation(self):
    # Schedule finishing event
    self.sim.stop(100)
    # Start simulating
    self.sim.start()


if __name__ == '__main__':
  unittest.main()