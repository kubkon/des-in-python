#!/usr/bin/env python
# encoding: utf-8

import argparse
import mm1
import sim
import time


### Parse command line arguments
parser = argparse.ArgumentParser(description="M/M/1 queue simulation -- Main script")
parser.add_argument('sim_duration', metavar='simulation_duration',
                    type=int, help='simulation duration in seconds')
parser.add_argument('--seed', dest='seed', default=int(round(time.time())),
                    type=int, help='seed for the PRNG (default: current system timestamp)')
args = parser.parse_args()
sim_duration = args.sim_duration
seed = args.seed

### Params
# Mean interarrival rate of customers per second;
# hence, 0.05 <=> 3 people/minute
interarrival_rate = 0.05
# Mean service rate by the teller per second;
# hence, 0.1 <=> 6 people/minute
service_rate = 0.1
  
### Initialize
# Create new simulation engine
se = sim.SimulationEngine()
# Seed default PRNG
se.prng.seed = seed
# Create MM1 specific event handler
event_handler = mm1.MM1EventHandler()
event_handler.interarrival_rate = interarrival_rate
event_handler.service_rate = service_rate
  
### Simulate
# Schedule finishing event
se.stop(sim_duration)
# Start simulating
se.start()
