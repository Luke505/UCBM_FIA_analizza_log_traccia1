"""Tests for parser module."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from parser import LogParserError, parse_log_file, parse_timestamp


class TestParseTimestamp(unittest.TestCase):
	"""Test timestamp parsing functionality."""

	def test_parse_standard_format(self):
		"""Test parsing standard datetime format."""
		result = parse_timestamp("2024-01-15 10:30:45")
		self.assertEqual(result, datetime(2024, 1, 15, 10, 30, 45))

	def test_parse_iso_format(self):
		"""Test parsing ISO format."""
		result = parse_timestamp("2024-01-15T10:30:45")
		self.assertEqual(result, datetime(2024, 1, 15, 10, 30, 45))

	def test_parse_with_microseconds(self):
		"""Test parsing timestamp with microseconds."""
		result = parse_timestamp("2024-01-15 10:30:45.123456")
		self.assertEqual(result, datetime(2024, 1, 15, 10, 30, 45, 123456))

	def test_parse_invalid_format(self):
		"""Test that invalid format raises error."""
		with self.assertRaises(LogParserError):
			parse_timestamp("invalid-timestamp")


class TestParseLogFile(unittest.TestCase):
	"""Test log file parsing functionality."""

	def setUp(self):
		"""Set up test data."""
		self.valid_log_data = [
			["2024-01-15 10:00:00", "user1", "web", "auth", "login", "User logged in", "frontend", "192.168.1.1"],
			["2024-01-15 10:05:00", "user2", "mobile", "auth", "login", "User logged in", "app", "192.168.1.2"],
			["2024-01-15 10:10:00", "user1", "web", "profile", "view", "Profile viewed", "frontend", "192.168.1.1"]
		]

	def test_parse_valid_file(self):
		"""Test parsing a valid log file."""
		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			json.dump(self.valid_log_data, f)
			temp_path = f.name

		try:
			result = parse_log_file(temp_path)
			self.assertEqual(len(result), 3)
			self.assertEqual(result[0].user_id, "user1")
			self.assertEqual(result[0].ip_address, "192.168.1.1")
			self.assertEqual(result[1].user_id, "user2")
		finally:
			Path(temp_path).unlink()

	def test_parse_nonexistent_file(self):
		"""Test that parsing nonexistent file raises error."""
		with self.assertRaises(LogParserError) as cm:
			parse_log_file("nonexistent_file.json")
		self.assertIn("not found", str(cm.exception))

	def test_parse_invalid_json(self):
		"""Test that invalid JSON raises error."""
		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			f.write("invalid json content {")
			temp_path = f.name

		try:
			with self.assertRaises(LogParserError) as cm:
				parse_log_file(temp_path)
			self.assertIn("Invalid JSON", str(cm.exception))
		finally:
			Path(temp_path).unlink()

	def test_parse_non_list_root(self):
		"""Test that non-list root raises error."""
		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			json.dump({"key": "value"}, f)
			temp_path = f.name

		try:
			with self.assertRaises(LogParserError) as cm:
				parse_log_file(temp_path)
			self.assertIn("must be a list", str(cm.exception))
		finally:
			Path(temp_path).unlink()

	def test_parse_wrong_field_count(self):
		"""Test that entries with wrong field count raise error."""
		invalid_data = [
			["2024-01-15 10:00:00", "user1", "web"]  # Only 3 fields instead of 8
		]

		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			json.dump(invalid_data, f)
			temp_path = f.name

		try:
			with self.assertRaises(LogParserError) as cm:
				parse_log_file(temp_path)
			self.assertIn("must have exactly 8 fields", str(cm.exception))
		finally:
			Path(temp_path).unlink()

	def test_parse_non_list_entry(self):
		"""Test that non-list entries raise error."""
		invalid_data = [
			"not a list entry"
		]

		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			json.dump(invalid_data, f)
			temp_path = f.name

		try:
			with self.assertRaises(LogParserError) as cm:
				parse_log_file(temp_path)
			self.assertIn("must be a list", str(cm.exception))
		finally:
			Path(temp_path).unlink()

	def test_parse_empty_file(self):
		"""Test parsing empty log file."""
		with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			json.dump([], f)
			temp_path = f.name

		try:
			result = parse_log_file(temp_path)
			self.assertEqual(len(result), 0)
		finally:
			Path(temp_path).unlink()


if __name__ == '__main__':
	unittest.main()
