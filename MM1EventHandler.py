#!/usr/bin/env python
# encoding: utf-8
"""
MM1EventHandler.py

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

from EventHandler import *
from Event import *


class MM1EventHandler(EventHandler):
  '''
  MM1 queue specific event handler
  '''
  def __init__(self, simulation_engine):
    '''
    Constructs MM1EventHandler object
    '''
    super(MM1EventHandler, self).__init__(simulation_engine)
    # Initialize mean interarrival time
    self._interarrival_time = 0
    # Initialize mean service time
    self._service_time = 0
    # Initialize lenght of queue
    self._queue_length = 0
    # Initialize is processing flag
    self._is_processing = False
  
  @property
  def interarrival_time(self):
    '''
    Returns mean interarrival time
    '''
    return self._interarrival_time
  
  @interarrival_time.setter
  def interarrival_time(self, interarrival_time):
    '''
    Sets mean interarrival time
    '''
    self._interarrival_time = interarrival_time
  
  @property
  def service_time(self):
    '''
    Returns mean service time
    '''
    return self._service_time
  
  @service_time.setter
  def service_time(self, service_time):
    '''
    Sets mean service time
    '''
    self._service_time = service_time
  
  def generate_event(self, simulation_time):
    '''
    Overriden
    '''
    # Next customer arrival time
    delta_time = random.expovariate(1 / self._interarrival_time)
    event = Event("Arrival", simulation_time + delta_time)
    # Schedule event
    self._simulation_engine.schedule(event)
  
  def handle_event(self, event):
    '''
    Overriden
    '''
    # Print the event
    print("{}: {}".format(event.time, event.identifier))
    # Increment the queue length based on the event id
    if event.identifier == "Arrival":
      self._queue_length += 1
    elif event.identifier == "Departure":
      self._queue_length -= 1
      self._is_processing = False
    else:
      self._is_processing = False
    # Process customer if free and queue is not empty
    if not self._is_processing and self._queue_length > 0:
      # Compute service time
      delta_time = random.expovariate(self._service_time)
      dep_event = Event("Departure", event.time + delta_time)
      self._simulation_engine.schedule(dep_event)
      self._is_processing = True
    print("Queue length: {}".format(self._queue_length))
  

class MM1EventHandlerTests(unittest.TestCase):
  def setUp(self):
    self.eh = MM1EventHandler(None)
    
  def test_properties(self):
    self.eh.interarrival_time = 0.05
    self.eh.service_time = 0.1
    self.assertEquals(self.eh.interarrival_time, 0.05)
    self.assertEquals(self.eh.service_time, 0.1)

if __name__ == '__main__':
  unittest.main()