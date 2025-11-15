"""Integration tests for the complete log analysis system."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from main import process_log_file


class TestIntegration(unittest.TestCase):
	"""Integration tests for end-to-end functionality."""

	def setUp(self):
		"""Set up test data and temporary directory."""
		self.test_data = [
			["2024-01-15 10:00:00", "user1", "web", "auth", "login", "User logged in", "frontend", "192.168.1.1"],
			["2024-01-15 11:00:00", "user2", "mobile", "auth", "login", "User logged in", "app", "192.168.1.2"],
			["2024-01-15 12:00:00", "user1", "web", "profile", "view", "Profile viewed", "frontend", "192.168.1.1"],
			["2024-01-15 13:00:00", "user1", "api", "data", "fetch", "Data fetched", "backend", "192.168.1.3"],
			["2024-01-15 14:00:00", "user3", "web", "auth", "login", "User logged in", "frontend", "192.168.1.1"]
		]
		self.temp_dir = TemporaryDirectory()

	def tearDown(self):
		"""Clean up temporary directory."""
		self.temp_dir.cleanup()

	def test_process_without_filters(self):
		"""Test processing without any filters."""
		# Create input file
		input_path = Path(self.temp_dir.name) / "input.json"
		with open(input_path, 'w') as f:
			json.dump(self.test_data, f)

		# Define output paths
		logs_path = Path(self.temp_dir.name) / "logs.json"
		stats_path = Path(self.temp_dir.name) / "stats.json"

		# Process
		process_log_file(
			str(input_path),
			str(logs_path),
			str(stats_path)
		)

		# Verify logs output
		with open(logs_path, 'r') as f:
			logs = json.load(f)
		self.assertEqual(len(logs), 5)
		self.assertEqual(logs[0]['user_id'], "user1")

		# Verify stats output
		with open(stats_path, 'r') as f:
			stats = json.load(f)
		self.assertEqual(len(stats), 3)

		# Check user1 stats
		user1_stats = next(s for s in stats if s['user_id'] == "user1")
		self.assertEqual(user1_stats['access_counter'], 3)
		self.assertEqual(user1_stats['usage_age'], "3 hours")  # Human-readable format
		self.assertEqual(len(user1_stats['ip_addresses']), 2)
		self.assertEqual(len(user1_stats['event_contexts']), 2)

	def test_process_with_timestamp_filter(self):
		"""Test processing with timestamp filters."""
		# Create input file
		input_path = Path(self.temp_dir.name) / "input.json"
		with open(input_path, 'w') as f:
			json.dump(self.test_data, f)

		# Define output paths
		logs_path = Path(self.temp_dir.name) / "logs.json"
		stats_path = Path(self.temp_dir.name) / "stats.json"

		# Process with filters
		process_log_file(
			str(input_path),
			str(logs_path),
			str(stats_path),
			filter_start_timestamp=datetime(2024, 1, 15, 11, 30, 0),
			filter_end_timestamp=datetime(2024, 1, 15, 13, 30, 0)
		)

		# Verify logs output
		with open(logs_path, 'r') as f:
			logs = json.load(f)
		self.assertEqual(len(logs), 2)

		# Verify stats output
		with open(stats_path, 'r') as f:
			stats = json.load(f)
		self.assertEqual(len(stats), 1)
		self.assertEqual(stats[0]['user_id'], "user1")

	def test_process_with_ip_filter(self):
		"""Test processing with IP address filter."""
		# Create input file
		input_path = Path(self.temp_dir.name) / "input.json"
		with open(input_path, 'w') as f:
			json.dump(self.test_data, f)

		# Define output paths
		logs_path = Path(self.temp_dir.name) / "logs.json"
		stats_path = Path(self.temp_dir.name) / "stats.json"

		# Process with IP filter
		process_log_file(
			str(input_path),
			str(logs_path),
			str(stats_path),
			filter_ip_address="192.168.1.1"
		)

		# Verify logs output
		with open(logs_path, 'r') as f:
			logs = json.load(f)
		self.assertEqual(len(logs), 3)
		self.assertTrue(all(log['ip_address'] == "192.168.1.1" for log in logs))

		# Verify stats output
		with open(stats_path, 'r') as f:
			stats = json.load(f)
		self.assertEqual(len(stats), 2)  # user1 and user3

	def test_process_with_combined_filters(self):
		"""Test processing with multiple filters."""
		# Create input file
		input_path = Path(self.temp_dir.name) / "input.json"
		with open(input_path, 'w') as f:
			json.dump(self.test_data, f)

		# Define output paths
		logs_path = Path(self.temp_dir.name) / "logs.json"
		stats_path = Path(self.temp_dir.name) / "stats.json"

		# Process with combined filters
		process_log_file(
			str(input_path),
			str(logs_path),
			str(stats_path),
			filter_start_timestamp=datetime(2024, 1, 15, 11, 0, 0),
			filter_end_timestamp=datetime(2024, 1, 15, 13, 0, 0),
			filter_ip_address="192.168.1.1"
		)

		# Verify logs output
		with open(logs_path, 'r') as f:
			logs = json.load(f)
		self.assertEqual(len(logs), 1)
		self.assertEqual(logs[0]['user_id'], "user1")
		self.assertEqual(logs[0]['component'], "profile")

		# Verify stats output
		with open(stats_path, 'r') as f:
			stats = json.load(f)
		self.assertEqual(len(stats), 1)
		self.assertEqual(stats[0]['user_id'], "user1")
		self.assertEqual(stats[0]['access_counter'], 1)

	def test_process_empty_result(self):
		"""Test processing that results in no matches."""
		# Create input file
		input_path = Path(self.temp_dir.name) / "input.json"
		with open(input_path, 'w') as f:
			json.dump(self.test_data, f)

		# Define output paths
		logs_path = Path(self.temp_dir.name) / "logs.json"
		stats_path = Path(self.temp_dir.name) / "stats.json"

		# Process with filter that matches nothing
		process_log_file(
			str(input_path),
			str(logs_path),
			str(stats_path),
			filter_ip_address="10.0.0.1"
		)

		# Verify empty outputs
		with open(logs_path, 'r') as f:
			logs = json.load(f)
		self.assertEqual(len(logs), 0)

		with open(stats_path, 'r') as f:
			stats = json.load(f)
		self.assertEqual(len(stats), 0)


if __name__ == '__main__':
	unittest.main()
