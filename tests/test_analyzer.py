"""Tests for analyzer module."""

import unittest
from datetime import datetime

from analyzer import generate_user_stats
from models import LogEntry


class TestGenerateUserStats(unittest.TestCase):
	"""Test user statistics generation."""

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
				user_id="user1",
				event_context="api",
				component="data",
				event="fetch",
				description="Data fetched",
				origin="backend",
				ip_address="192.168.1.3"
			)
		]

	def test_generate_stats_basic(self):
		"""Test basic statistics generation."""
		result = generate_user_stats(self.log_entries)
		self.assertEqual(len(result), 2)

		# Results should be sorted by user_id
		self.assertEqual(result[0].user_id, "user1")
		self.assertEqual(result[1].user_id, "user2")

	def test_user_access_counter(self):
		"""Test access counter calculation."""
		result = generate_user_stats(self.log_entries)
		user1_stats = next(s for s in result if s.user_id == "user1")
		user2_stats = next(s for s in result if s.user_id == "user2")

		self.assertEqual(user1_stats.access_counter, 3)
		self.assertEqual(user2_stats.access_counter, 1)

	def test_user_timestamps(self):
		"""Test first and last timestamp calculation."""
		result = generate_user_stats(self.log_entries)
		user1_stats = next(s for s in result if s.user_id == "user1")

		self.assertEqual(user1_stats.first_timestamp, datetime(2024, 1, 15, 10, 0, 0))
		self.assertEqual(user1_stats.last_timestamp, datetime(2024, 1, 15, 13, 0, 0))

	def test_usage_age(self):
		"""Test usage age calculation."""
		result = generate_user_stats(self.log_entries)
		user1_stats = next(s for s in result if s.user_id == "user1")
		user2_stats = next(s for s in result if s.user_id == "user2")

		# user1: 10:00 to 13:00 = 3 hours = 10800 seconds
		self.assertEqual(user1_stats.usage_age, 10800.0)
		# user2: only one entry, so usage_age = 0
		self.assertEqual(user2_stats.usage_age, 0.0)

		# Test human-readable format in dictionary output
		user1_dict = user1_stats.to_dict()
		self.assertEqual(user1_dict['usage_age'], "3 hours")
		user2_dict = user2_stats.to_dict()
		self.assertEqual(user2_dict['usage_age'], "0 seconds")

	def test_unique_ip_addresses(self):
		"""Test unique IP addresses collection."""
		result = generate_user_stats(self.log_entries)
		user1_stats = next(s for s in result if s.user_id == "user1")

		self.assertEqual(len(user1_stats.ip_addresses), 2)
		self.assertIn("192.168.1.1", user1_stats.ip_addresses)
		self.assertIn("192.168.1.3", user1_stats.ip_addresses)
		# Should be sorted
		self.assertEqual(user1_stats.ip_addresses, sorted(user1_stats.ip_addresses))

	def test_unique_event_contexts(self):
		"""Test unique event contexts collection."""
		result = generate_user_stats(self.log_entries)
		user1_stats = next(s for s in result if s.user_id == "user1")

		self.assertEqual(len(user1_stats.event_contexts), 2)
		self.assertIn("web", user1_stats.event_contexts)
		self.assertIn("api", user1_stats.event_contexts)
		# Should be sorted
		self.assertEqual(user1_stats.event_contexts, sorted(user1_stats.event_contexts))

	def test_empty_input(self):
		"""Test with empty log entries."""
		result = generate_user_stats([])
		self.assertEqual(len(result), 0)

	def test_single_entry(self):
		"""Test with single log entry."""
		single_entry = [self.log_entries[0]]
		result = generate_user_stats(single_entry)

		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].user_id, "user1")
		self.assertEqual(result[0].access_counter, 1)
		self.assertEqual(result[0].usage_age, 0.0)

		# Test human-readable format in dictionary output
		result_dict = result[0].to_dict()
		self.assertEqual(result_dict['usage_age'], "0 seconds")

	def test_duplicate_contexts_and_ips(self):
		"""Test that duplicate contexts and IPs are deduplicated."""
		duplicate_entries = [
			LogEntry(
				timestamp=datetime(2024, 1, 15, 10, 0, 0),
				user_id="user1",
				event_context="web",
				component="auth",
				event="login",
				description="Login 1",
				origin="frontend",
				ip_address="192.168.1.1"
			),
			LogEntry(
				timestamp=datetime(2024, 1, 15, 11, 0, 0),
				user_id="user1",
				event_context="web",
				component="auth",
				event="login",
				description="Login 2",
				origin="frontend",
				ip_address="192.168.1.1"
			)
		]

		result = generate_user_stats(duplicate_entries)
		self.assertEqual(len(result[0].ip_addresses), 1)
		self.assertEqual(len(result[0].event_contexts), 1)


if __name__ == '__main__':
	unittest.main()
