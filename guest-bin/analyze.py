#!/usr/bin/env python3

import os
import sys
import math

file_name = sys.argv[1]

sum = 0
count = 0
errors = 0
max = 90
min = -1
zeros = 0
max_range = 15
max_width = 20

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

# TODO (max / (max_range - 1)) if you want to use a dynamic max.
increment = max / max_range

index = 0
buckets = [0] * max_range

numbers.sort()

max_count = max_width

for number in numbers:
    bucket_index = math.floor(number / increment)
    buckets[bucket_index] += 1
    if buckets[bucket_index] > max_width:
        max_count = buckets[bucket_index]

last_min = 0
last_max = increment
for bucket in buckets:
    ticks = ''.join(list(map(lambda x: "#", range(0, int(bucket * (max_count / max_width))))))
    print("{:6.2f} Mbps - {:6.2f} Mbps | {}".format(last_min, last_max, ticks))
    last_min += increment
    last_max += increment

print("intervals: {}".format(count))
print("errors: {}".format(errors))
print("max: {} Mbps".format(max))
print("min: {} Mbps".format(min))
print("average: {:.2f} Mbps".format(sum / count))
