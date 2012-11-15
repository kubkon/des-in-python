#!/usr/bin/env python
# encoding: utf-8

import csv
import os.path
import des.sim as sim
import unittest


class MM1EventHandler(sim.EventHandler):
  """
  MM1 queue specific event handler
  """
  # IDs of the handled events
  ARRIVAL_EVENT = "Arrival"
  DEPARTURE_EVENT = "Departure"
  
  def __init__(self):
    """
    Constructs MM1EventHandler object
    """
    super().__init__()
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
    """
    Returns mean interarrival rate
    """
    return self._interarrival_rate
  
  @interarrival_rate.setter
  def interarrival_rate(self, interarrival_rate):
    """
    Sets mean interarrival rate
    
    Keyword arguments:
    interarrival_rate -- Interarrival rate to be set
    """
    self._interarrival_rate = interarrival_rate
  
  @property
  def service_rate(self):
    """
    Returns mean service rate
    """
    return self._service_rate
  
  @service_rate.setter
  def service_rate(self, service_rate):
    """
    Sets mean service rate
    
    Keyword arguments:
    service_rate -- Service rate to be set
    """
    self._service_rate = service_rate
  
  def _handle_start(self):
    """
    Overriden method
    """
    self._schedule_arrival_event(self._simulation_engine.simulation_time)
  
  def _handle_stop(self):
    """
    Overriden method
    """
    self._save_statistics()
  
  def _handle_event(self, event):
    """
    Overriden method
    """
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
    """
    Schedules next arrival event
    
    Keyword arguments:
    base_time -- Current simulation time
    """
    # Calculate interarrival time
    delta_time = self._simulation_engine.prng.exponential(1/self._interarrival_rate)
    # Create next arrival event
    event = sim.Event(MM1EventHandler.ARRIVAL_EVENT, base_time + delta_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
  
  def _schedule_departure_event(self, base_time):
    """
    Schedules next departure event
    
    Keyword arguments:
    base_time -- Current simulation time
    """
    # Calculate service time
    delta_time = self._simulation_engine.prng.exponential(1/self._service_rate)
    # Create next departure event
    event = sim.Event(MM1EventHandler.DEPARTURE_EVENT, base_time + delta_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
    # Set is processing flag to True
    self._is_processing = True
  
  def _save_statistics(self):
    """
    Save statistics when simulation ends
    """
    # Calculate mean delay
    arrivals_len = len(self._arrivals)
    departures_len = len(self._departures)
    if arrivals_len == 0 or departures_len == 0:
      print("Mean waiting time unavailable")
    else:
      if arrivals_len >= departures_len:
        self._arrivals = self._arrivals[:departures_len]
      else:
        self._departures = self._departures[:arrivals_len]
      delays = list(map(lambda x,y: x-y, self._departures, self._arrivals))
      # Save to a file
      fname = "delays_{}_{}.out".format(self._interarrival_rate,
                                        self._service_rate)
      with open(fname, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(delays)
  

class MM1EventHandlerTests(unittest.TestCase):
  def setUp(self):
    self.eh = MM1EventHandler()
    
  def test_properties(self):
    self.eh.interarrival_rate = 0.05
    self.eh.service_rate = 0.1
    self.assertEqual(self.eh.interarrival_rate, 0.05)
    self.assertEqual(self.eh.service_rate, 0.1)

if __name__ == '__main__':
  unittest.main()