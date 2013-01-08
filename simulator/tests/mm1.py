#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from simulator.modules.mm1 import *
from simulator.modules.sim import SimulationEngine, Event


class MM1EventHandlerTests(unittest.TestCase):
  def setUp(self):
    sim = SimulationEngine()
    self.seed = 0
    sim.prng = np.random.RandomState(self.seed)
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
    self.eh.interarrival_rate = 0.2
    self.eh.service_rate = 0.5
    self.assertEqual(self.eh.interarrival_rate, 0.2)
    self.assertEqual(self.eh.service_rate, 0.5)

  def test_generate_arrival_event(self):
    event = self.eh._generate_arrival_event(1.0)
    prng = np.random.RandomState(self.seed)
    self.assertEqual(event.identifier, MM1EventHandler.ARRIVAL_EVENT)
    self.assertEqual(event.time, 1.0 + prng.exponential(1/self.eh.interarrival_rate))

  def test_generate_departure_event(self):
    event = self.eh._generate_departure_event(1.0)
    prng = np.random.RandomState(self.seed)
    self.assertEqual(event.identifier, MM1EventHandler.DEPARTURE_EVENT)
    self.assertEqual(event.time, 1.0 + prng.exponential(1/self.eh.service_rate))

  def test_handle_arrival_event(self):
    self.eh._handle_event(Event(MM1EventHandler.ARRIVAL_EVENT, 1.0))
    self.assertEqual(self.eh._queue_length, 1)
    self.assertEqual(self.eh._arrivals, [1.0])

  def test_handle_departure_event(self):
    self.eh._queue_length = 1
    self.eh._handle_event(Event(MM1EventHandler.DEPARTURE_EVENT, 1.0))
    self.assertEqual(self.eh._queue_length, 0)
    self.assertEqual(self.eh._departures, [1.0])

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

