#!/usr/bin/env python
# encoding: utf-8

import mm1
import sim


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
  se = sim.SimulationEngineFactory.get_instance()
  # Seed default PRNG
  se.prng.seed = 100
  # Create MM1 specific event handler
  event_handler = mm1.MM1EventHandler()
  event_handler.interarrival_rate = interarrival_rate
  event_handler.service_rate = service_rate
  
  ### Simulate
  # Schedule finishing event; simulate for 24h
  se.stop(60*60*24)
  # Start simulating
  se.start()


if __name__ == '__main__':
  main()