#!/usr/bin/env python
# encoding: utf-8

import argparse
import numpy as np
import simulator.modules.mm1 as mm1
import simulator.modules.sim as sim
import time


### Parse command line arguments
parser = argparse.ArgumentParser(description="M/M/1 queue simulation -- Main script")
parser.add_argument('sim_duration', metavar='simulation_duration',
                    type=int, help='simulation duration in seconds')
parser.add_argument('int_rate', metavar='interarrival_rate',
                    type=int, help='mean packet interarrival rate in seconds')
parser.add_argument('sr_rate', metavar='service_rate',
                    type=int, help='mean packet service rate in seconds')
parser.add_argument('--id', dest='id', default=0,
                    type=int, help='simulation run id (default: 0)')
parser.add_argument('--seed', dest='seed', default=int(round(time.time())),
                    type=int, help='seed for the PRNG (default: current system timestamp)')
args = parser.parse_args()
sim_duration = args.sim_duration
interarrival_rate = args.int_rate
service_rate = args.sr_rate
sim_id = args.id
seed = args.seed
  
### Initialize
# Create new simulation engine
se = sim.SimulationEngine()
# Seed NumPy PRNG
se.prng = np.random.RandomState(seed)
# Create MM1 specific event handler, and
# connect it with the simulation engine
event_handler = mm1.MM1EventHandler(se)
se.event_handler = event_handler
# Set simulation parameters
event_handler.interarrival_rate = interarrival_rate
event_handler.service_rate = service_rate
event_handler.sim_id = sim_id
  
### Simulate
# Schedule finishing event
se.stop(sim_duration)
# Start simulating
se.start()
