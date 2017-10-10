#!/usr/bin/env python3

import math
from optparse import OptionParser
from warnings import warn

# Terminology derived from here - https://en.wikipedia.org/wiki/Histogram

def load_data(file_name):
	numbers = []
	with open(file_name, 'r') as file:
		for line in file:
			as_num = float(line)
			numbers.append(as_num)
	return numbers

def bin_values(values, num_bins, max_value):
	"""
	Bucket (bin) a _sorted_ list of numbers into intervals (groups, bins, etc.)
	The numbers are grouped based on the number of bins and the maximum
	value. Using the number of bins and the maximum value we derive the bin
	width (size, range, interval) used for each bin. The min value for bins
	is 0.

	Args:
		values:    A sorted list of numbers.
		num_bins:  Number of bins into which the data should be grouped.
		max_value: The maximum value against which we should size our bins.

	Returns:
		bin_width:   The width/range used for grouping numbers.
		bins:        The binned/bucketed/grouped list of numbers.
	"""
	bins = [0] * num_bins
	values.sort()

	bin_width = max_value / len(bins)
	for value in values:
		bin_index = math.floor(value / bin_width)
		bins[bin_index] += 1

	return bin_width, bins

def histogram(bins, increment, graph_width):
	"""
	Graph a list of numbers as a histogram.

	Args:
		bins:        A list of numbers that have been grouped into bins at fixed
		             intervals.
		interval:    The size used for the distribution of values into each bin.
		graph_width: Maximum width for the display of each frequency.
	"""
	last_min = 0
	last_max = increment
	highest_value = max(bins)

	# Maximum value/interval represented by the bins.
	max_value = increment * len(bins)
	# Width of the maximum bin interval.
	max_value_width = len(str(int(max_value)))
	# Width of the greatest frequency in the binned data.
	max_frequency_width = len(str(highest_value))
	# Scaled width of bar graph.
	scaled_graph_width = graph_width / highest_value

	precision = 1
	for count in bins:
		# TODO ceil or floor?
		scaled_count = math.floor(count * scaled_graph_width)
		ticks = ''.join(list(map(lambda x: "+", range(0, scaled_count))))
		fmt_count = '{:{width}d}'.format(count, width=max_frequency_width)
		fmt_min = format_number(last_min, max_value_width, precision)
		fmt_max = format_number(last_max, max_value_width, precision)
		print("{} - {} Mbps | {} {}".format(fmt_min, fmt_max, fmt_count, ticks))
		last_min += increment
		last_max += increment

def format_number(number, digit_width, precision_width):
	total_width = digit_width

	if precision_width > 0:
		# The 1 is for the decimal. This is the *total* width of the string.
		total_width += (1 + precision_width)

	return '{:{total_width}.{precision_width}f}'.format(
		number,
		total_width=total_width,
		precision_width=precision_width
	)

def main():
	parser = OptionParser()
	parser.add_option('-m', '--scale-max', dest='scale_max', type='int', help='Greatest value shown on Y axis.')
	parser.add_option('-w', '--graph-width', dest='graph_width', type='int', default=10, help='Max number of "+" signs to show in the graph. Controls graph width.')
	parser.add_option('-b', '--num-bins', dest='num_bins', type='int', default=15, help='Number of bins to display on Y axis.')
	parser.add_option('-f', '--file', dest='file_path', type='string', help='Path of file to analyze and graph.')
	(options, args) = parser.parse_args()

	graph_width = options.graph_width
	num_bins = options.num_bins
	if options.file_path is None:
		parser.error('File not provided. View help for this script with --help')
		exit(1)
	else:
		file_name = options.file_path
	if options.scale_max is None:
		parser.error('Scale max not provided. You must determine the maximum scale of your data.')
		exit(1)
	else:
		scale_max = options.scale_max

	# Raw data from file.
	numbers = load_data(file_name)

	numbers.sort()
	max_number = numbers[-1]

	if scale_max < max_number:
		exit('Scale max is invalid. Scale max is lower than the maximum value in the data.')

	interval, bins = bin_values(numbers, num_bins, scale_max)
	histogram(bins, interval, graph_width)

	print("total: {}".format(len(numbers)))
	print("max: {} Mbps".format(max(numbers)))
	print("min: {} Mbps".format(min(numbers)))
	print("average: {:.2f} Mbps".format(sum(numbers) / len(numbers)))

if __name__ == "__main__":
	main()
