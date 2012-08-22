#!/usr/bin/env python
# encoding: utf-8
"""
sim.py

Created by Jakub Konka on 2012-08-22.
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

from abc import ABCMeta, abstractmethod

import datetime
import random
import time
import unittest


class _SimulationEngine(object):
  '''
  Represents the main engine of a DES simulation platform;
  should not be instantiated directly
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
    self._callback_dict = {_SimulationEngine.START_CALLBACK: [], _SimulationEngine.STOP_CALLBACK: [], _SimulationEngine.EVENT_CALLBACK: []}
    # Initialize default PRNG
    self._prng = PRNG()
  
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
    
    Keyword arguments:
    simulation_time -- Simulation time to be set
    '''
    self._simulation_time = simulation_time
  
  @property
  def prng(self):
    '''
    Returns used PRNG
    '''
    return self._prng
  
  @prng.setter
  def prng(self, prng):
    '''
    Sets PRNG to be used by the simulation engine
    '''
    self._prng = prng
  
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
      self._event_list += [Event(_SimulationEngine.END_EVENT, self._finish_time)]
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
    for func in self._callback_dict[_SimulationEngine.START_CALLBACK]: func()
  
  def _notify_stop(self):
    '''
    Notifies of stop of the simulation 
    '''
    for func in self._callback_dict[_SimulationEngine.STOP_CALLBACK]: func()
  
  def _notify_event(self, event):
    '''
    Notifies of an imminent event
    
    Keyword arguments:
    event -- The imminent event 
    '''
    for func in self._callback_dict[_SimulationEngine.EVENT_CALLBACK]: func(event)
  

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
      SimulationEngineFactory._INSTANCE = _SimulationEngine()
    return SimulationEngineFactory._INSTANCE
  

class Event(object):
  '''
  Represents an abstract event
  '''
  def __init__(self, identifier, time, **kwargs):
    '''
    Constructs Event instance
    
    Keyword arguments:
    identifier -- ID/type of this event
    time -- Time of occurring of this event
    kwargs -- Optional arguments
    '''
    self._identifier = identifier
    self._time = time
    self._kwargs = kwargs
  
  @property
  def identifier(self):
    '''
    Returns id of this event
    '''
    return self._identifier
  
  @property
  def time(self):
    '''
    Returns time of occurring
    '''
    return self._time
  
  @property
  def kwargs(self):
    '''
    Returns dictionary of optional arguments
    '''
    return self._kwargs
  

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
    self._simulation_engine.register_callback(self._handle_start, _SimulationEngine.START_CALLBACK)
    # stop of the simulation
    self._simulation_engine.register_callback(self._handle_stop, _SimulationEngine.STOP_CALLBACK)
    # imminent event
    self._simulation_engine.register_callback(self._handle_event, _SimulationEngine.EVENT_CALLBACK)
  
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
  

class PRNG(object):
  '''
  Represents default PRNG (currently, wrapper class for random module)
  '''
  
  def __init__(self):
    '''
    Constructs PRNG instance
    '''
    # Default seed value to current datetime
    self._seed = int(time.mktime(datetime.datetime.now().timetuple()))
    # Initialize PRNG with the default seed value
    random.seed(self._seed)
  
  @property
  def seed(self):
    '''
    Returns current seed value
    '''
    return self._seed
  
  @seed.setter
  def seed(self, seed):
    '''
    Sets new seed value
    
    Keyword arguments:
    seed -- New seed value
    '''
    self._seed = seed
    # Re-initialize PRNG with new seed value
    random.seed(self._seed)
  
  def randint(self, a, b):
    '''
    Returns a random integer N such that a <= N <= b
    
    Keyword arguments:
    a -- Lower bound
    b -- Upper bound
    '''
    return random.randint(a, b)
  
  def uniform(self, a, b):
    '''
    Returns a random floating point number N such that
    a <= N <= b for a <= b and b <= N <= a for b < a
    
    Keyword arguments:
    a -- Lower bound
    b -- Upper bound
    '''
    return random.uniform(a, b)
  
  def expovariate(self, lambd):
    '''
    Returns a random floating point number N drawn
    from an exponential distribution with parameter lambd (1 / E[X])
    
    Keyword arguments:
    lambd -- Lambda parameter of exponential distribution (1 / E[X])
    '''
    return random.expovariate(lambd)
  

class SimulationEngineFactoryTests(unittest.TestCase):
  def setUp(self):
    self.sim = SimulationEngineFactory.get_instance()
  
  def test_singleton_like_behaviour(self):
    sim = SimulationEngineFactory.get_instance()
    self.assertEqual(self.sim, sim)
  
  def test_notify_start(self):
    def f(): print("Callback received")
    self.sim.register_callback(f, _SimulationEngine.START_CALLBACK)
    self.sim.stop(1)
    self.sim.start()
  
  def test_notify_stop(self):
    def f(): print("Callback received")
    self.sim.register_callback(f, _SimulationEngine.STOP_CALLBACK)
    self.sim.stop(1)
    self.sim.start()
  
  def test_notify_event(self):
    def f(e): print("Callback received. Event: {}@{}".format(e.identifier, e.time))
    self.sim.register_callback(f, _SimulationEngine.EVENT_CALLBACK)
    self.sim.stop(2)
    self.sim.schedule(Event("Dummy", 1))
    self.sim.start()
  

class EventTests(unittest.TestCase):
  def setUp(self):
    self.e1 = Event("Arrival", 10)
    self.e2 = Event("Arrival", 10, special="Special")
  
  def test_properties(self):
    self.assertEqual(self.e1.identifier, "Arrival")
    self.assertEqual(self.e1.time, 10)
    self.assertEqual(self.e2.identifier, "Arrival")
    self.assertEqual(self.e2.time, 10)
    self.assertEqual(self.e2.kwargs.get('special', None), "Special")
  

if __name__ == '__main__':
  unittest.main()