#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from simulator.modules.mm1 import MM1EventHandler
from simulator.modules.sim import SimulationEngine, Event
import unittest


class MM1EventHandlerTests(unittest.TestCase):
  def setUp(self):
    sim = SimulationEngine()
    sim.prng = np.random.RandomState(0)
    self.eh = MM1EventHandler(sim)
    self.eh.interarrival_rate = 0.05
    self.eh.service_rate = 0.1
    
  def test_init(self):
    eh = MM1EventHandler(SimulationEngine())
    self.assertEqual(eh._queue_length, 0)
    self.assertEqual(eh._arrivals, [])
    self.assertEqual(eh._departures, [])
    self.assertFalse(eh._is_processing)

  def test_properties(self):
    self.assertEqual(self.eh.interarrival_rate, 0.05)
    self.assertEqual(self.eh.service_rate, 0.1)

  def test_generate_arrival_event(self):
    event_time = 1.0
    event = self.eh._generate_arrival_event(event_time)
    self.assertEqual(event.identifier, MM1EventHandler.ARRIVAL_EVENT)
    self.assertGreater(event.time, event_time)

  def test_generate_departure_event(self):
    event_time = 1.0
    event = self.eh._generate_departure_event(event_time)
    self.assertEqual(event.identifier, MM1EventHandler.DEPARTURE_EVENT)
    self.assertGreater(event.time, event_time)

  def test_handle_arrival_event(self):
    event_time = 1.0
    self.eh._handle_event(Event(MM1EventHandler.ARRIVAL_EVENT, event_time))
    self.assertEqual(self.eh._queue_length, 1)
    self.assertEqual(self.eh._arrivals, [event_time])

  def test_handle_departure_event(self):
    self.eh._queue_length = 1
    event_time = 1.0
    self.eh._handle_event(Event(MM1EventHandler.DEPARTURE_EVENT, event_time))
    self.assertEqual(self.eh._queue_length, 0)
    self.assertEqual(self.eh._departures, [event_time])

  def test_is_processing_for_arrival_and_busy(self):
    self.eh._is_processing = True
    self.eh._handle_event(Event(MM1EventHandler.ARRIVAL_EVENT, 1.0))
    self.assertTrue(self.eh._is_processing)

  def test_is_processing_for_arrival_and_idle(self):
    self.eh._is_processing = False
    self.eh._handle_event(Event(MM1EventHandler.ARRIVAL_EVENT, 1.0))
    self.assertTrue(self.eh._is_processing)

  def test_is_processing_for_departure_and_empty_queue(self):
    self.eh._queue_length = 1
    self.eh._handle_event(Event(MM1EventHandler.DEPARTURE_EVENT, 1.0))
    self.assertFalse(self.eh._is_processing)

  def test_is_processing_for_departure_and_nonempty_queue(self):
    self.eh._queue_length = 2
    self.eh._handle_event(Event(MM1EventHandler.DEPARTURE_EVENT, 1.0))
    self.assertTrue(self.eh._is_processing)


if __name__ == '__main__':
  unittest.main()

