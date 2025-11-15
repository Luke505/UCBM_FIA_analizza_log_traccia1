#!/usr/bin/env python3
"""Example usage of the log analysis system."""

from datetime import datetime
from main import process_log_file

# Example 1: Process log file without filters
print("Example 1: Processing without filters")
print("-" * 50)
process_log_file(
	file_path="test_data/test_simple.json",
	output_logs_path="example_all_logs.json",
	output_stats_path="example_all_stats.json"
)
print()

# Example 2: Filter by IP address
print("Example 2: Filtering by IP address")
print("-" * 50)
process_log_file(
	file_path="test_data/test_simple.json",
	output_logs_path="example_ip_filtered_logs.json",
	output_stats_path="example_ip_filtered_stats.json",
	filter_ip_address="192.168.103.208"
)
print()

# Example 3: Filter by timestamp range
print("Example 3: Filtering by timestamp range")
print("-" * 50)
process_log_file(
	file_path="test_data/test_simple.json",
	output_logs_path="example_time_filtered_logs.json",
	output_stats_path="example_time_filtered_stats.json",
	filter_start_timestamp=datetime(2021, 11, 1, 0, 0, 0),
	filter_end_timestamp=datetime(2021, 11, 2, 23, 59, 59)
)
print()

# Example 4: Combine multiple filters
print("Example 4: Combining multiple filters")
print("-" * 50)
process_log_file(
	file_path="test_data/test_simple.json",
	output_logs_path="example_combined_filtered_logs.json",
	output_stats_path="example_combined_filtered_stats.json",
	filter_start_timestamp=datetime(2021, 11, 1, 0, 0, 0),
	filter_end_timestamp=datetime(2021, 11, 3, 23, 59, 59),
	filter_ip_address="79.19.222.61"
)
print()

print("All examples completed!")
print("Check the generated JSON files for results.")
