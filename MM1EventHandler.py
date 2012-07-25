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

from SimulationEngine.EventHandler import *
from SimulationEngine.Event import *
from SimulationEngine.SimulationEngine import *


class MM1EventHandler(EventHandler):
  '''
  MM1 queue specific event handler
  '''
  # IDs of the handled events
  ARRIVAL_EVENT = "Arrival"
  DEPARTURE_EVENT = "Departure"
  
  def __init__(self, simulation_engine):
    '''
    Constructs MM1EventHandler object
    '''
    super(MM1EventHandler, self).__init__(simulation_engine)
    # Initialize mean interarrival time
    self._interarrival_rate = 0
    # Initialize mean service time
    self._service_rate = 0
    # Initialize lenght of queue
    self._queue_length = 0
    # Initialize is processing flag
    self._is_processing = False
    # Initialize list of arrival times
    self._arrivals = []
    # Initialize list of departure times
    self._departures = []
  
  @property
  def interarrival_rate(self):
    '''
    Returns mean interarrival rate
    '''
    return self._interarrival_rate
  
  @interarrival_rate.setter
  def interarrival_rate(self, interarrival_rate):
    '''
    Sets mean interarrival rate
    '''
    self._interarrival_rate = interarrival_rate
  
  @property
  def service_rate(self):
    '''
    Returns mean service rate
    '''
    return self._service_rate
  
  @service_rate.setter
  def service_rate(self, service_rate):
    '''
    Sets mean service rate
    '''
    self._service_rate = service_rate
  
  def _handle_start(self):
    '''
    Overriden method
    '''
    self._schedule_arrival_event(self._simulation_engine.simulation_time)
  
  def _handle_stop(self):
    '''
    Overriden method
    '''
    self._print_statistics()
  
  def _handle_event(self, event):
    '''
    Overriden method
    '''
    # Print the imminent event
    # print("{}: {}".format(event.time, event.identifier))
    # Check event's identifier
    if event.identifier == MM1EventHandler.ARRIVAL_EVENT:
      # Increment the queue length
      self._queue_length += 1
      # Record event's arrival time (stats)
      self._arrivals += [event.time]
      # Schedule next arrival event
      self._schedule_arrival_event(event.time)
    if event.identifier == MM1EventHandler.DEPARTURE_EVENT:
      # Decrement the queue length
      self._queue_length -= 1
      # Record event's departure time (stats)
      self._departures += [event.time]
      # Set is processing flag to False
      self._is_processing = False
    # Service customer if free and queue is not empty
    if not self._is_processing and self._queue_length > 0:
      # Schedule next departure event
      self._schedule_departure_event(event.time)
  
  def _schedule_arrival_event(self, base_time):
    '''
    Schedules next arrival event
    '''
    # Calculate interarrival time
    delta_time = random.expovariate(self._interarrival_rate)
    # Create next arrival event
    event = Event(MM1EventHandler.ARRIVAL_EVENT, base_time + delta_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
  
  def _schedule_departure_event(self, base_time):
    '''
    Schedules next departure event
    '''
    # Calculate service time
    delta_time = random.expovariate(self._service_rate)
    # Create next departure event
    event = Event(MM1EventHandler.DEPARTURE_EVENT, base_time + delta_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
    # Set is processing flag to True
    self._is_processing = True
  
  def _print_statistics(self):
    '''
    Prints some statistics when simulation ends
    '''
    # Calculate mean waiting time in the queue
    arrivals_len = len(self._arrivals)
    departures_len = len(self._departures)
    if arrivals_len == 0 or departures_len == 0:
      print("Mean waiting time unavailable")
    else:
      if arrivals_len >= departures_len:
        self._arrivals = self._arrivals[:departures_len]
      else:
        self._departures = self._departures[:arrivals_len]
      waiting_times = list(map(lambda x,y: x-y, self._departures, self._arrivals))
      print("Mean waiting time: {}".format(sum(waiting_times) / len(waiting_times)))
  

class MM1EventHandlerTests(unittest.TestCase):
  def setUp(self):
    self.eh = MM1EventHandler(SimulationEngine())
    
  def test_properties(self):
    self.eh.interarrival_rate = 0.05
    self.eh.service_rate = 0.1
    self.assertEquals(self.eh.interarrival_rate, 0.05)
    self.assertEquals(self.eh.service_rate, 0.1)

if __name__ == '__main__':
  unittest.main()