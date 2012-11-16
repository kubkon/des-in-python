#!/usr/bin/env python
# encoding: utf-8

import argparse
import csv
import numpy as np
import os
import scipy.stats as stats
import sys


### Parse command line arguments
parser = argparse.ArgumentParser(description="M/M/1 queue simulation -- Analysis script")
parser.add_argument('input_dir', help='directory containing simulation results')
parser.add_argument('mode', help='transient or steady-state')
parser.add_argument('--confidence', dest='confidence', default=0.95,
                    type=float, help='confidence to be used in confidence interval calculations')
args = parser.parse_args()
input_dir = args.input_dir
mode = args.mode
confidence = args.confidence

### Common params
# Ask for warm-up period index (if mode is steady-state)
if mode == 'steady-state':
  warmup = int(input('Warm-up period index: '))
elif mode == 'transient':
  warmup = 0
  window_size = int(input('Window size: '))
else:
  sys.exit('Unknown mode specified.')
# File names and paths
extension = ".out"
file_names = [f for _, _, files in os.walk(input_dir) for f in files if f.endswith(extension)]

### Read data from files
for fn in file_names:
  outer = []
  with open(input_dir + '/' + fn, 'rt') as f:
    reader = csv.reader(f)
    row_num = 1
    inner = []
    for row in reader:
      # Exclude data with index lower than specified warm-up period
      if row_num > warmup:
        inner += [float(row[0])]
      row_num += 1
  outer += [inner]

### Map and reduce...
if mode == 'steady-state':
  # Compute steady-state mean average
  averages = [sum(lst) / len(lst) for lst in outer]
  mean = sum(averages) / len(averages)
  # Compute standard deviation
  sd = np.sqrt(sum(map(lambda x: (x-mean)**2, averages)) / (len(averages)-1))
  # Compute standard error for the mean
  se = sd / np.sqrt(len(averages))
  # Compute confidence intervals for the mean
  ci = se * stats.t.ppf(0.5 + confidence/2, len(averages)-1)
  # Save to a file
  fn = input_dir + '/' + mode
  with open(fn, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['mean', 'sd', 'se', 'ci'])
    writer.writerow([mean, sd, se, ci])
else:
  # Compute mean
  zipped = zip(*[lst for lst in outer])
  init_means = list(map(lambda x: sum(x)/len(outer), zipped))
  means = []
  # Apply Welch's method
  if window_size == 0:
    means = init_means
  else:
    for i in range(len(init_means) - window_size):
      if i < window_size:
        means += [sum([init_means[i+s] for s in range(-i, i+1)]) / (2*(i+1) - 1)]
      else:
        means += [sum([init_means[i+s] for s in range(-window_size, window_size+1)]) / (2*window_size + 1)]
  # Compute standard deviation
  zipped = zip(*[lst for lst in outer])
  sds = [np.sqrt(sum(map(lambda x: (x-mean)**2, tup)) / (len(means) - 1)) for (tup, mean) in zip(zipped, means)]
  # Compute standard error for the mean
  ses = list(map(lambda x: x/np.sqrt(len(means)), sds))
  # Compute confidence intervals for the mean
  cis = list(map(lambda x: x * stats.t.ppf(0.5 + confidence/2, len(means)-1), ses))
  # Save to a file
  fn = input_dir + '/' + mode + '_{}'.format(window_size)
  with open(fn, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    zip_input = [means, sds, ses, cis]
    out_headers = ['mean', 'sd', 'se', 'ci']
    writer.writerow(out_headers)
    for tup in zip(*zip_input):
      writer.writerow(tup)
