#!/usr/bin/env python
# encoding: utf-8

import argparse
import numpy as np
import scipy.stats as stats
import csv


### Parse command line arguments
parser = argparse.ArgumentParser(description="M/M/1 queue simulation -- Analysis script")
parser.add_argument('file_name', help='name of the file containing data')
parser.add_argument('--confidence', dest='confidence', default=0.95,
                    type=float, help='confidence to be used in confidence interval calculations')
args = parser.parse_args()
file_name = args.file_name
confidence = args.confidence

### Load data from file
with open(file_name, mode='rt') as f:
  reader = csv.reader(f)
  delays = [float(col) for row in reader for col in row]

### Analyze data
# Compute mean delay
mean = sum(delays) / len(delays)
# Compute standard deviation
sd = np.sqrt(sum(map(lambda x: (x-mean)**2, delays)) / (len(delays)-1))
# Compute standard error for the mean
se = sd / np.sqrt(len(delays))
# Compute confidence intervals for the mean
ci = se * stats.t.ppf(0.5 + confidence/2, len(delays)-1)

### Output results
print("Mean delay: {} +/- {}".format(mean, ci))
