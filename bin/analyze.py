#!/usr/bin/env python3

import os
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-m', '--scale-max', dest='scale_max', type='int', default=50, help='Greatest value shown on Y axis.')
parser.add_option('-w', '--graph-width', dest='graph_width', type='int', default=10, help='Max number of "+" signs to show in the graph. Controls graph width.')
parser.add_option('-b', '--max-buckets', dest='max_buckets', type='int', default=15, help='Number of bucketed data points to display on Y axis.')
parser.add_option('-f', '--file', dest='file_path', type='string', help='Path of file to analyze and graph.')

(options, args) = parser.parse_args()

scale_max = options.scale_max
graph_width = options.graph_width
max_buckets = options.max_buckets
if options.file_path is None:
	parser.error('File not provided. View help for this script with --help')
	exit(1)
else:
	file_name = options.file_path

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

def graph(buckets, scale_max, graph_width):
	increment = scale_max / len(buckets)
	last_min = 0
	last_max = increment
	highest_value = max(buckets)
	count_width = len(str(highest_value))
	precision = 0
	for bucket in buckets:
		scale = graph_width / highest_value
		# TODO ceil or floor?
		scaled_count = math.floor(bucket * scale)
		ticks = ''.join(list(map(lambda x: "+", range(0, scaled_count))))
		fmt_count = '{:{width}d}'.format(bucket, width=count_width)
		fmt_min = format_mbps(last_min, len(str(scale_max)), precision)
		fmt_max = format_mbps(last_max, len(str(scale_max)), precision)
		print("{} - {} Mbps | {} {}".format(fmt_min, fmt_max, fmt_count, ticks))
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

# Bucket the data based on the max number of buckets we want.
# Buckets represent ranges. 0 - 5, 6 - 10, etc. Based on whatever the max is.
buckets = bucket_data(max_buckets, numbers, scale_max)

# Display graph of the bucketed/grouped data.
graph(buckets, scale_max, graph_width)

print("total: {}".format(len(numbers)))
print("max: {} Mbps".format(max(numbers)))
print("min: {} Mbps".format(min(numbers)))
print("average: {:.2f} Mbps".format(sum(numbers) / len(numbers)))
