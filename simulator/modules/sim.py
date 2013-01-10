#!/usr/bin/env python
# encoding: utf-8

from abc import abstractmethod, ABCMeta
import datetime
import random
import time
import unittest


class PRNG:
  """
  Represents default PRNG (currently, wrapper class for random module).
  """
  def __init__(self):
    """
    Constructs PRNG instance
    """
    # Default seed value to current datetime
    self._seed = int(time.mktime(datetime.datetime.now().timetuple()))
    # Initialize PRNG with the default seed value
    random.seed(self._seed)
  
  @property
  def seed(self):
    """
    Returns current seed value
    """
    return self._seed
  
  @seed.setter
  def seed(self, seed):
    """
    Sets new seed value
    
    Arguments:
    seed -- New seed value
    """
    self._seed = seed
    # Re-initialize PRNG with new seed value
    random.seed(self._seed)
  
  def randint(self, a, b):
    """
    Returns a random integer N such that a <= N <= b
    
    Arguments:
    a -- Lower bound
    b -- Upper bound
    """
    return random.randint(a, b)
  
  def uniform(self, a, b):
    """
    Returns a random floating point number N such that
    a <= N <= b for a <= b and b <= N <= a for b < a
    
    Arguments:
    a -- Lower bound
    b -- Upper bound
    """
    return random.uniform(a, b)
  
  def expovariate(self, lambd):
    """
    Returns a random floating point number N drawn
    from an exponential distribution with parameter lambd (1 / E[X])
    
    Arguments:
    lambd -- Lambda parameter of exponential distribution (1 / E[X])
    """
    return random.expovariate(lambd)
  

class Event:
  """
  Represents an abstract event.
  """
  def __init__(self, identifier, time, **kwargs):
    """
    Constructs Event instance
    
    Arguments:
    identifier -- ID/type of this event
    time -- Time of occurring of this event

    Keyword arguments:
    kwargs -- Optional keyword arguments
    """
    self._identifier = identifier
    self._time = time
    self._kwargs = kwargs
  
  @property
  def identifier(self):
    """
    Returns id of this event
    """
    return self._identifier
  
  @property
  def time(self):
    """
    Returns time of occurring
    """
    return self._time
  
  @property
  def kwargs(self):
    """
    Returns dictionary of optional arguments
    """
    return self._kwargs
  

class EventHandler(metaclass=ABCMeta):
  """
  Abstract base class for event handlers
  """
  def __init__(self, simulation_engine):
    """
    Constructs EventHandler object

    Arguments:
    simulation_engine = SimulationEngine instance
    """
    # Connect with SimulationEngine
    self._simulation_engine = simulation_engine
    # Register callback functions:
    # start of the simulation
    self._simulation_engine.register_callback(self._handle_start, SimulationEngine.START_CALLBACK)
    # stop of the simulation
    self._simulation_engine.register_callback(self._handle_stop, SimulationEngine.STOP_CALLBACK)
    # imminent event
    self._simulation_engine.register_callback(self._handle_event, SimulationEngine.EVENT_CALLBACK)
  
  @abstractmethod
  def _handle_start(self):
    """
    Abstract method for handling start of the simulation
    """
    pass
  
  @abstractmethod
  def _handle_stop(self):
    """
    Abstract method for handling stop of the simulation
    """
    pass
  
  @abstractmethod
  def _handle_event(self, event):
    """
    Abstract method for handling imminent events
    
    Arguments:
    event -- Event to be handled
    """
    pass
  

class SimulationEngine:
  """
  Represents the main engine of a DES simulation platform
  """
  # ID of the finishing event
  END_EVENT = "End"
  # Callback types
  START_CALLBACK = "start"
  STOP_CALLBACK = "stop"
  EVENT_CALLBACK = "event"
  
  def __init__(self):
    """
    Constructs SimulationEngine instance
    """
    # Create empty event list
    self._event_list = []
    # Initialize current simulation time
    self.simulation_time = 0
    # Initialize finish time
    self._finish_time = 0
    # Flag representing finishing event
    self._finish_event_exists = False
    # Initialize callback dictionary
    self._callback_dict = {self.START_CALLBACK: [], self.STOP_CALLBACK: [], self.EVENT_CALLBACK: []}
    # Initialize default PRNG
    self.prng = PRNG()
    # Initialize event handler
    self.event_handler = None

  def start(self):
    """
    Starts simulation
    """
    # Check whether an EventHandler is attached; if not, throw an error
    if not self.event_handler:
      raise Exception("No EventHandler attached!")
    # Notify of the start of simulation; event handlers should
    # generate first event
    self._notify_start()
    # Traverse the event list
    while len(self._event_list) > 0:
      # Remove the imminent event from the event list
      imminent = self._event_list.pop()
      # Advance clock to the imminent event
      self.simulation_time = imminent.time
      # Notify of the current event
      self._notify_event(imminent)
    # Notify of the end of the simulation
    self._notify_stop()
  
  def stop(self, finish_time):
    """
    Schedules finishing event
    
    Arguments:
    finish_time -- Time of occurrence of the finishing event
    """
    # Check if finishing event already scheduled
    if not self._finish_event_exists:
      # Set finish time
      self._finish_time = finish_time
      # Schedule finishing event
      self._event_list += [Event(self.END_EVENT, self._finish_time)]
      self._finish_event_exists = True
  
  def schedule(self, event):
    """
    Schedules event (adds it to the event list)
    
    Arguments:
    event -- Event to be scheduled
    """
    # Discard new event if happens after the finishing event
    if event.time < self._finish_time:
      # Add the event to the event list
      self._event_list += [event]
      # Sort the list in a LIFO style
      self._event_list.sort(key=lambda x: x.time)
      self._event_list.reverse()
  
  def register_callback(self, func, ttype):
    """
    Register function for callback when simulation ends
    
    Arguments:
    func -- Function to call back
    ttype -- Type of the callback
    """
    self._callback_dict[ttype] += [func]
  
  def _notify_start(self):
    """
    Notifies of start of the simulation
    """
    for func in self._callback_dict[self.START_CALLBACK]: func()
  
  def _notify_stop(self):
    """
    Notifies of stop of the simulation
    """
    for func in self._callback_dict[self.STOP_CALLBACK]: func()
  
  def _notify_event(self, event):
    """
    Notifies of an imminent event
    
    Arguments:
    event -- The imminent event 
    """
    for func in self._callback_dict[self.EVENT_CALLBACK]: func(event)
  
