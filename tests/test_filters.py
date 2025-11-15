"""Tests for filters module."""

import unittest
from datetime import datetime

from filters import apply_filters
from models import LogEntry


class TestApplyFilters(unittest.TestCase):
	"""Test filtering functionality."""

	def setUp(self):
		"""Set up test log entries."""
		self.log_entries = [
			LogEntry(
				timestamp=datetime(2024, 1, 15, 10, 0, 0),
				user_id="user1",
				event_context="web",
				component="auth",
				event="login",
				description="User logged in",
				origin="frontend",
				ip_address="192.168.1.1"
			),
			LogEntry(
				timestamp=datetime(2024, 1, 15, 11, 0, 0),
				user_id="user2",
				event_context="mobile",
				component="auth",
				event="login",
				description="User logged in",
				origin="app",
				ip_address="192.168.1.2"
			),
			LogEntry(
				timestamp=datetime(2024, 1, 15, 12, 0, 0),
				user_id="user1",
				event_context="web",
				component="profile",
				event="view",
				description="Profile viewed",
				origin="frontend",
				ip_address="192.168.1.1"
			),
			LogEntry(
				timestamp=datetime(2024, 1, 15, 13, 0, 0),
				user_id="user3",
				event_context="web",
				component="auth",
				event="logout",
				description="User logged out",
				origin="frontend",
				ip_address="192.168.1.3"
			)
		]

	def test_no_filters(self):
		"""Test that no filters returns all entries."""
		result = apply_filters(self.log_entries)
		self.assertEqual(len(result), 4)

	def test_start_timestamp_filter(self):
		"""Test filtering by start timestamp."""
		result = apply_filters(
			self.log_entries,
			filter_start_timestamp=datetime(2024, 1, 15, 11, 30, 0)
		)
		self.assertEqual(len(result), 2)
		self.assertTrue(all(e.timestamp >= datetime(2024, 1, 15, 11, 30, 0) for e in result))

	def test_end_timestamp_filter(self):
		"""Test filtering by end timestamp."""
		result = apply_filters(
			self.log_entries,
			filter_end_timestamp=datetime(2024, 1, 15, 11, 30, 0)
		)
		self.assertEqual(len(result), 2)
		self.assertTrue(all(e.timestamp <= datetime(2024, 1, 15, 11, 30, 0) for e in result))

	def test_timestamp_range_filter(self):
		"""Test filtering by timestamp range."""
		result = apply_filters(
			self.log_entries,
			filter_start_timestamp=datetime(2024, 1, 15, 10, 30, 0),
			filter_end_timestamp=datetime(2024, 1, 15, 12, 30, 0)
		)
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].user_id, "user2")
		self.assertEqual(result[1].user_id, "user1")

	def test_ip_address_filter(self):
		"""Test filtering by IP address."""
		result = apply_filters(
			self.log_entries,
			filter_ip_address="192.168.1.1"
		)
		self.assertEqual(len(result), 2)
		self.assertTrue(all(e.ip_address == "192.168.1.1" for e in result))

	def test_combined_filters(self):
		"""Test combining multiple filters."""
		result = apply_filters(
			self.log_entries,
			filter_start_timestamp=datetime(2024, 1, 15, 10, 30, 0),
			filter_end_timestamp=datetime(2024, 1, 15, 12, 30, 0),
			filter_ip_address="192.168.1.1"
		)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].user_id, "user1")
		self.assertEqual(result[0].timestamp, datetime(2024, 1, 15, 12, 0, 0))

	def test_no_matching_entries(self):
		"""Test filter that matches no entries."""
		result = apply_filters(
			self.log_entries,
			filter_ip_address="10.0.0.1"
		)
		self.assertEqual(len(result), 0)

	def test_empty_input(self):
		"""Test filtering empty list."""
		result = apply_filters([])
		self.assertEqual(len(result), 0)

	def test_exact_timestamp_boundaries(self):
		"""Test that boundary timestamps are inclusive."""
		result = apply_filters(
			self.log_entries,
			filter_start_timestamp=datetime(2024, 1, 15, 11, 0, 0),
			filter_end_timestamp=datetime(2024, 1, 15, 12, 0, 0)
		)
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].timestamp, datetime(2024, 1, 15, 11, 0, 0))
		self.assertEqual(result[1].timestamp, datetime(2024, 1, 15, 12, 0, 0))


if __name__ == '__main__':
	unittest.main()
