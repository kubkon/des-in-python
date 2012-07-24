#!/usr/bin/env python
# encoding: utf-8
"""
mm1-example.py

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

from SimulationEngine import *
from MM1EventHandler import *


def main():
  ### Params
  # Mean interarrival time of customers (per second)
  interarrival_time = 5
  # Mean service time by the teller (per second)
  service_time = 1
  
  ### Initialize
  # Create new simulation engine
  sim = SimulationEngine()
  # Create MM1 specific event handler
  event_handler = MM1EventHandler(sim)
  event_handler.interarrival_time = interarrival_time
  event_handler.service_time = service_time
  # Register event handler with the simulation engine
  sim.event_handler = event_handler
  
  ### Simulate
  # Schedule finishing event
  sim.stop(10)
  # Start simulating
  sim.start()


if __name__ == '__main__':
  main()