#!/usr/bin/env python3

import os
import sys
import math

file_name = sys.argv[1]

# Constants
scale_max = 50

scale_min = 0
max_buckets = 15
max_bar_width = 10

def load_data(file_name):
	numbers = []
	with open(file_name, 'r') as file:
		for line in file:
			as_num = float(line)
			numbers.append(as_num)
	return numbers

def bucket_data(max_buckets, numbers, scale_max):
	buckets = [0] * max_buckets
	numbers.sort()
	increment = scale_max / len(buckets)
	for number in numbers:
		bucket_index = math.floor(number / increment)
		buckets[bucket_index] += 1
	return buckets

def graph(buckets, scale_min, scale_max, max_bar_width):
	increment = scale_max / len(buckets)
	last_min = 0
	last_max = increment
	highest_value = max(buckets)
	count_width = len(str(highest_value))
	precision = 0
	for bucket in buckets:
		scale = max_bar_width / highest_value
		# TODO ceil or floor?
		scaled_count = math.floor(bucket * scale)
		ticks = ''.join(list(map(lambda x: "#", range(0, scaled_count))))
		fmt_count = '{:{width}d}'.format(bucket, width=count_width)
		fmt_min = format_mbps(last_min, len(str(scale_max)), precision)
		fmt_max = format_mbps(last_max, len(str(scale_max)), precision)
		print("{} - {} Mbps [{}] {}".format(fmt_min, fmt_max, fmt_count, ticks))
		last_min += increment
		last_max += increment

def format_mbps(number, digit_width, precision_width):
	total_width = digit_width

	if precision_width > 0:
		# The 1 is for the decimal. This is the *total* width of the string.
		total_width += (1 + precision_width)

	return '{:{total_width}.{precision_width}f}'.format(
		number,
		total_width=total_width,
		precision_width=precision_width
	)

# Raw data from file.
numbers = load_data(file_name)

# -1 in the file indicates an error condition.
error_count = sum(1 if x == -1 else 0 for x in numbers)

# Copy of the list with the errors removed.
filtered = list(filter(lambda x: x != -1, numbers))

# Bucket the data based on the max number of buckets we want.
# Buckets represent ranges. 0 - 5, 6 - 10, etc. Based on whatever the max is.
# TODO WFH Get this working with static scale_max, or max(buckets)
buckets = bucket_data(max_buckets, filtered, scale_max)

# Display graph of the bucketed/grouped data.
graph(buckets, scale_min, scale_max, max_bar_width)

print("intervals: {}".format(len(numbers)))
print("errors: {}".format(error_count))
print("max: {} Mbps".format(max(filtered)))
print("min: {} Mbps".format(min(filtered)))
print("average: {:.2f} Mbps".format(sum(filtered) / len(filtered)))
