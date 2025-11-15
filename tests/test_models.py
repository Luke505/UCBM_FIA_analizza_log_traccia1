"""Tests for models module."""

import unittest
from datetime import datetime

from models import LogEntry, UserStats, format_duration


class TestFormatDuration(unittest.TestCase):
	"""Test duration formatting functionality."""

	def test_zero_seconds(self):
		"""Test formatting zero seconds."""
		self.assertEqual(format_duration(0), "0 seconds")

	def test_only_seconds(self):
		"""Test formatting only seconds (less than a minute)."""
		self.assertEqual(format_duration(30), "30 seconds")
		self.assertEqual(format_duration(1), "1 second")

	def test_only_minutes(self):
		"""Test formatting only minutes."""
		self.assertEqual(format_duration(60), "1 minute")
		self.assertEqual(format_duration(120), "2 minutes")
		self.assertEqual(format_duration(300), "5 minutes")

	def test_only_hours(self):
		"""Test formatting only hours."""
		self.assertEqual(format_duration(3600), "1 hour")
		self.assertEqual(format_duration(7200), "2 hours")
		self.assertEqual(format_duration(10800), "3 hours")

	def test_only_days(self):
		"""Test formatting only days."""
		self.assertEqual(format_duration(86400), "1 day")
		self.assertEqual(format_duration(172800), "2 days")

	def test_hours_and_minutes(self):
		"""Test formatting hours and minutes."""
		self.assertEqual(format_duration(3660), "1 hour, 1 minute")
		self.assertEqual(format_duration(3720), "1 hour, 2 minutes")
		self.assertEqual(format_duration(7260), "2 hours, 1 minute")

	def test_days_and_hours(self):
		"""Test formatting days and hours."""
		self.assertEqual(format_duration(90000), "1 day, 1 hour")
		self.assertEqual(format_duration(93600), "1 day, 2 hours")

	def test_days_hours_minutes(self):
		"""Test formatting days, hours, and minutes."""
		self.assertEqual(format_duration(90060), "1 day, 1 hour, 1 minute")
		self.assertEqual(format_duration(93780), "1 day, 2 hours, 3 minutes")
		self.assertEqual(format_duration(258000), "2 days, 23 hours, 40 minutes")

	def test_large_duration(self):
		"""Test formatting large durations."""
		# 30 days, 5 hours, 15 minutes
		duration = (30 * 86400) + (5 * 3600) + (15 * 60)
		self.assertEqual(format_duration(duration), "30 days, 5 hours, 15 minutes")


class TestLogEntry(unittest.TestCase):
	"""Test LogEntry model."""

	def test_to_dict(self):
		"""Test converting LogEntry to dictionary."""
		entry = LogEntry(
			timestamp=datetime(2024, 1, 15, 10, 0, 0),
			user_id="user1",
			event_context="web",
			component="auth",
			event="login",
			description="User logged in",
			origin="frontend",
			ip_address="192.168.1.1"
		)

		result = entry.to_dict()

		self.assertEqual(result['timestamp'], "2024-01-15T10:00:00")
		self.assertEqual(result['user_id'], "user1")
		self.assertEqual(result['event_context'], "web")
		self.assertEqual(result['component'], "auth")
		self.assertEqual(result['event'], "login")
		self.assertEqual(result['description'], "User logged in")
		self.assertEqual(result['origin'], "frontend")
		self.assertEqual(result['ip_address'], "192.168.1.1")


class TestUserStats(unittest.TestCase):
	"""Test UserStats model."""

	def test_to_dict(self):
		"""Test converting UserStats to dictionary."""
		stats = UserStats(
			user_id="user1",
			first_timestamp=datetime(2024, 1, 15, 10, 0, 0),
			last_timestamp=datetime(2024, 1, 15, 13, 0, 0),
			access_counter=5,
			usage_age=10800.0,  # 3 hours in seconds
			ip_addresses=["192.168.1.1", "192.168.1.2"],
			event_contexts=["web", "mobile"]
		)

		result = stats.to_dict()

		self.assertEqual(result['user_id'], "user1")
		self.assertEqual(result['first_timestamp'], "2024-01-15T10:00:00")
		self.assertEqual(result['last_timestamp'], "2024-01-15T13:00:00")
		self.assertEqual(result['access_counter'], 5)
		self.assertEqual(result['usage_age'], "3 hours")
		self.assertEqual(result['ip_addresses'], ["192.168.1.1", "192.168.1.2"])
		self.assertEqual(result['event_contexts'], ["web", "mobile"])

	def test_to_dict_zero_usage_age(self):
		"""Test converting UserStats with zero usage_age."""
		stats = UserStats(
			user_id="user1",
			first_timestamp=datetime(2024, 1, 15, 10, 0, 0),
			last_timestamp=datetime(2024, 1, 15, 10, 0, 0),
			access_counter=1,
			usage_age=0.0,
			ip_addresses=["192.168.1.1"],
			event_contexts=["web"]
		)

		result = stats.to_dict()
		self.assertEqual(result['usage_age'], "0 seconds")


if __name__ == '__main__':
	unittest.main()
