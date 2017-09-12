#!/usr/bin/env python3

import os
import sys

file_name = sys.argv[1]

sum = 0
count = 0
errors = 0
max = 0
min = -1
zeros = 0
max_range = 10

numbers = []

with open(file_name, "r") as file:
    for line in file:
        as_num = float(line)

        if as_num == -1:
            errors += 1
            continue

        if as_num > max:
            max = as_num
        if as_num < min or min == -1:
            min = as_num
        if as_num == 0:
            zeros += 1

        numbers.append(as_num)

        count += 1
        sum = sum + as_num

# TODO WFH Two charts. One doing what I'm doing now to show off strength. One
# to plot a histogram of where most of the results lie.

numbers.sort()
for number in numbers:
    ticks = ''.join(list(map(lambda x: "#", range(0, int(number)))))
    print("{:.2f} | {}".format(number, ticks))

print("domain: {}".format(count))
print("errors: {}".format(errors))
print("max: {} Mbps".format(max))
print("min: {} Mbps".format(min))
print("average: {:.2f} Mbps".format(sum / count))
