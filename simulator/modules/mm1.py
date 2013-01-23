#!/usr/bin/env python
# encoding: utf-8

import csv
import os.path
import simulator.modules.sim as sim
import unittest


class MM1EventHandler(sim.EventHandler):
  """
  MM1 queue specific event handler
  """
  # IDs of the handled events
  ARRIVAL_EVENT = "Arrival"
  DEPARTURE_EVENT = "Departure"
  
  def __init__(self, simulation_engine):
    """
    Constructs MM1EventHandler object
    """
    super().__init__(simulation_engine)
    # Initialize mean interarrival time
    self.interarrival_rate = 0
    # Initialize mean service time
    self.service_rate = 0
    # Initialize lenght of queue
    self._queue_length = 0
    # Initialize is processing flag
    self._is_processing = False
    # Initialize list of arrival times
    self._arrivals = []
    # Initialize list of departure times
    self._departures = []
  
  def handle_start(self):
    """
    Overriden method
    """
    self._schedule_arrival_event(self._simulation_engine.simulation_time)
  
  def handle_stop(self):
    """
    Overriden method
    """
    self._save_statistics()
  
  def handle_event(self, event):
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
      # Set is processing flag to True
      self._is_processing = True
  
  def _generate_arrival_event(self, base_time):
    """
    Returns next arrival event

    Keyword arguments:
    base_time -- Current simulation time
    """
    # Calculate interarrival time
    delta_time = self._simulation_engine.prng.exponential(1/self.interarrival_rate)
    # Create next arrival event
    return sim.Event(MM1EventHandler.ARRIVAL_EVENT, base_time + delta_time)

  def _schedule_arrival_event(self, base_time):
    """
    Schedules next arrival event
    
    Keyword arguments:
    base_time -- Current simulation time
    """
    event = self._generate_arrival_event(base_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
  
  def _generate_departure_event(self, base_time):
    """
    Returns next departure event

    Keyword arguments:
    base_time -- Current simulation time
    """
    # Calculate service time
    delta_time = self._simulation_engine.prng.exponential(1/self.service_rate)
    # Create next departure event
    return sim.Event(MM1EventHandler.DEPARTURE_EVENT, base_time + delta_time)

  def _schedule_departure_event(self, base_time):
    """
    Schedules next departure event
    
    Keyword arguments:
    base_time -- Current simulation time
    """
    event = self._generate_departure_event(base_time)
    # Schedule the event
    self._simulation_engine.schedule(event)
  
  def _save_statistics(self):
    """
    Save statistics when simulation ends
    """
    # Check if folder exists
    path = "delays_{}_{}".format(self.interarrival_rate, self.service_rate)
    if not os.path.exists(path):
      os.makedirs(path)
    # Calculate delays
    arrivals_len = len(self._arrivals)
    departures_len = len(self._departures)
    if arrivals_len == 0 or departures_len == 0:
      print("Empty list(s) encountered")
    else:
      if arrivals_len >= departures_len:
        self._arrivals = self._arrivals[:departures_len]
      else:
        self._departures = self._departures[:arrivals_len]
      delays = list(map(lambda x,y: x-y, self._departures, self._arrivals))
      # Save to a file
      fn = "delays_{}.out".format(self.sim_id)
      with open(path + "/" + fn, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for d in delays:
          writer.writerow([d])
  
