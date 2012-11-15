#!/usr/bin/env python
# encoding: utf-8

import argparse
import subprocess as sub


### Parse command line arguments
parser = argparse.ArgumentParser(description="M/M/1 queue simulation -- Helper script")
parser.add_argument('reps', metavar='repetitions',
                    type=int, help='number of repetitions')
parser.add_argument('sim_duration', metavar='simulation_duration',
                    type=int, help='duration of each simulation stage in seconds')
parser.add_argument('int_rate', metavar='interarrival_rate',
                    type=int, help='mean packet interarrival rate in seconds')
parser.add_argument('sr_rate', metavar='service_rate',
                    type=int, help='mean packet service rate in seconds')
parser.add_argument('--batch_size', dest='batch_size', default=4,
                    type=int, help='batch size for multiprocessing')
parser.add_argument('--initial_seed', dest='init_seed', default=0,
                    type=int, help='base for seed values')
args = parser.parse_args()
repetitions = args.reps
sim_duration = args.sim_duration
interarrival_rate = args.int_rate
service_rate = args.sr_rate
batch_size = args.batch_size
init_seed = args.init_seed

### Run simulations
try:
  # One process at a time
  if batch_size == 1:
    for n in range(repetitions):
      sub.call("python main-example.py {} {} {} --seed={}".format(sim_duration, interarrival_rate, service_rate, n+init_seed), shell=True)
  # In batches
  else:
    # Split num of repetitions into batches
    quotient = repetitions // batch_size
    remainder = repetitions % batch_size
    # Run the simulations in parallel as subprocesses
    num_proc = batch_size if batch_size <= repetitions else remainder
    procs = [sub.Popen("python main-example.py {} {} {} --seed={}".format(sim_duration, interarrival_rate, service_rate, n+init_seed), shell=True) for n in range(num_proc)]
    while True:
      procs_poll = list(map(lambda x: x.poll() != None, procs))
      if not all(procs_poll):
        procs[procs_poll.index(False)].wait()
      elif num_proc < repetitions:
        temp_num = batch_size if num_proc + batch_size <= repetitions else remainder
        for n in range(num_proc, num_proc + temp_num):
          procs += [sub.Popen("python main-example.py {} {} {} --seed={}".format(sim_duration, interarrival_rate, service_rate, n+init_seed), shell=True)]
        num_proc += temp_num
      else:
        break
except OSError as e:
  print("Execution failed: ", e)
