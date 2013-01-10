#!/usr/bin/env python
# encoding: utf-8

from simulator.modules.sim import *

class TestEventHandler(EventHandler):
  def __init__(self, simulation_engine):
    super().__init__(simulation_engine)
    self.start_callback_received = False
    self.stop_callback_received = False
    self.events = []

  def _handle_start(self):
    self.start_callback_received = True

  def _handle_stop(self):
    self.stop_callback_received = True

  def _handle_event(self, event):
    self.events.append(event)


class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    self.se = SimulationEngine()
    self.test_eh = TestEventHandler(self.se)
    self.se.event_handler = self.test_eh
 
  def test_raises_no_event_handler_exception(self):
    with self.assertRaisesRegexp(Exception, 'No EventHandler attached!'):
      SimulationEngine().start()

  def test_notify_start(self):
    self.se.stop(1)
    self.se.start()
    self.assertTrue(self.se.event_handler.start_callback_received)
  
  def test_notify_stop(self):
    self.se.stop(1)
    self.se.start()
    self.assertTrue(self.se.event_handler.stop_callback_received)
  
  def test_notify_event(self):
    self.se.stop(2)
    self.se.schedule(Event("Dummy", 1))
    self.se.start()
    self.assertEqual(self.se.event_handler.events[0].identifier, "Dummy")
    self.assertEqual(self.se.event_handler.events[0].time, 1)
    self.assertEqual(self.se.event_handler.events[1].identifier, "End")
    self.assertEqual(self.se.event_handler.events[1].time, 2)
  

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

