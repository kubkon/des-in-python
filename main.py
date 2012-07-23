#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Jakub Konka on 2012-07-23.
Copyright (c) 2012 Jakub Konka. All rights reserved.

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

from Event import *
from SimulationEngine import *


def main():
  # Create new simulation
	sim = SimulationEngine()
	# Create a set of deterministic events
	events = [Event(1), Event(4), Event(9)]
	# Populate event list (FEL)
	sim.addEvents(events)
	# Start simulating
	sim.start(10)


if __name__ == '__main__':
	main()

