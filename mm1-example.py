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

from SimulationEngine.SimulationEngine import *
from MM1EventHandler import *


def main():
  ### Params
  # Mean interarrival rate of customers per second;
  # hence, 0.05 <=> 3 people/minute
  interarrival_rate = 0.05
  # Mean service rate by the teller per second;
  # hence, 0.1 <=> 6 people/minute
  service_rate = 0.1
  
  ### Initialize
  # Create new simulation engine
  sim = SimulationEngine()
  # Seed PRNG
  sim.prng.seed = 100
  # Create MM1 specific event handler
  event_handler = MM1EventHandler(sim)
  event_handler.interarrival_rate = interarrival_rate
  event_handler.service_rate = service_rate
  
  ### Simulate
  # Schedule finishing event; simulate for 24h
  sim.stop(60*60*24)
  # Start simulating
  sim.start()


if __name__ == '__main__':
  main()