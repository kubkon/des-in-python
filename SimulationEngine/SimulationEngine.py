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

from .Event import *


class SimulationEngine(object):
  '''
  Represents the main engine of a DES simulation platform
  '''
  # ID of the finishing event
  END_EVENT = "End"
  # Callback types
  START_CALLBACK = "start"
  STOP_CALLBACK = "stop"
  EVENT_CALLBACK = "event"
  
  def __init__(self):
    '''
    Constructs SimulationEngine instance
    '''
    # Create empty event list
    self._event_list = []
    # Initialize current simulation time
    self._simulation_time = 0
    # Initialize finish time
    self._finish_time = 0
    # Flag representing finishing event
    self._finish_event_exists = False
    # Initialize callback dictionary
    self._callback_dict = {self.START_CALLBACK: [], self.STOP_CALLBACK: [], self.EVENT_CALLBACK: []}
  
  @property
  def simulation_time(self):
    '''
    Returns current simulation time
    '''
    return self._simulation_time
  
  @simulation_time.setter
  def simulation_time(self, simulation_time):
    '''
    Sets current simulation time
    '''
    self._simulation_time = simulation_time
  
  def start(self):
    '''
    Starts simulation
    '''
    # Notify of the start of simulation; event handlers should
    # generate first event
    self._notify_start()
    # Traverse the event list
    while len(self._event_list) > 0:
      # Remove the imminent event from the event list
      imminent = self._event_list.pop()
      # Advance clock to the imminent event
      self._simulation_time = imminent.time
      # Notify of the current event
      self._notify_event(imminent)
    # Notify of the end of the simulation
    self._notify_stop()
  
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
      self._event_list += [Event(self.END_EVENT, self._finish_time)]
      self._finish_event_exists = True
  
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
  
  def register_callback(self, func, ttype):
    '''
    Register function for callback when simulation ends
    
    Keyword arguments:
    func -- Function to call back
    ttype -- Type of the callback
    '''
    self._callback_dict[ttype] += [func]
  
  def _notify_start(self):
    '''
    Notifies of start of the simulation
    '''
    for func in self._callback_dict[self.START_CALLBACK]: func()
  
  def _notify_stop(self):
    '''
    Notifies of stop of the simulation 
    '''
    for func in self._callback_dict[self.STOP_CALLBACK]: func()
  
  def _notify_event(self, event):
    '''
    Notifies of an imminent event 
    '''
    for func in self._callback_dict[self.EVENT_CALLBACK]: func(event)
  

class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    self.sim = SimulationEngine()
  
  def test_notify_start(self):
    def f(): print("Callback received")
    self.sim.register_callback(f, self.sim.START_CALLBACK)
    self.sim.stop(1)
    self.sim.start()
  
  def test_notify_stop(self):
    def f(): print("Callback received")
    self.sim.register_callback(f, self.sim.STOP_CALLBACK)
    self.sim.stop(1)
    self.sim.start()
  
  def test_notify_event(self):
    def f(e): print("Callback received. Event: {}@{}".format(e.identifier, e.time))
    self.sim.register_callback(f, self.sim.EVENT_CALLBACK)
    self.sim.stop(2)
    self.sim.schedule(Event("Dummy", 1))
    self.sim.start()
  

if __name__ == '__main__':
  unittest.main()