"""Parser module for reading and parsing JSON log files."""

import json
from datetime import datetime
from pathlib import Path
from typing import List

from models import LogEntry


class LogParserError(Exception):
	"""Custom exception for log parsing errors."""
	pass


def parse_timestamp(timestamp_str: str) -> datetime:
	"""
	Parse timestamp string to datetime object.
	Supports multiple common formats.
	"""
	formats = [
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%dT%H:%M:%S",
		"%Y-%m-%d %H:%M:%S.%f",
		"%Y-%m-%dT%H:%M:%S.%f",
		"%Y-%m-%dT%H:%M:%S.%fZ",
		"%d/%m/%Y %H:%M",  # DD/MM/YYYY HH:MM
		"%-d/%-m/%Y %H:%M",  # D/M/YYYY HH:MM (without leading zeros)
	]

	for fmt in formats:
		try:
			return datetime.strptime(timestamp_str, fmt)
		except ValueError:
			continue

	# Try ISO format parsing as fallback
	try:
		return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
	except ValueError:
		raise LogParserError(f"Unable to parse timestamp: {timestamp_str}")


def parse_log_file(file_path: str) -> List[LogEntry]:
	"""
	Parse JSON log file containing list of lists into LogEntry objects.

	Args:
		file_path: Path to the JSON file

	Returns:
		List of LogEntry objects

	Raises:
		LogParserError: If file cannot be read or parsed
	"""
	try:
		path = Path(file_path)
		if not path.exists():
			raise LogParserError(f"File not found: {file_path}")

		with open(path, 'r', encoding='utf-8') as f:
			data = json.load(f)

		if not isinstance(data, list):
			raise LogParserError("JSON root must be a list")

		log_entries = []
		for idx, entry in enumerate(data):
			try:
				if not isinstance(entry, list):
					raise LogParserError(f"Entry {idx} must be a list")

				if len(entry) != 8:
					raise LogParserError(
						f"Entry {idx} must have exactly 8 fields, got {len(entry)}"
					)

				log_entry = LogEntry(
					timestamp=parse_timestamp(entry[0]),
					user_id=str(entry[1]),
					event_context=str(entry[2]),
					component=str(entry[3]),
					event=str(entry[4]),
					description=str(entry[5]),
					origin=str(entry[6]),
					ip_address=str(entry[7])
				)
				log_entries.append(log_entry)

			except (IndexError, ValueError, LogParserError) as e:
				raise LogParserError(f"Error parsing entry {idx}: {str(e)}")

		return log_entries

	except json.JSONDecodeError as e:
		raise LogParserError(f"Invalid JSON format: {str(e)}")
	except IOError as e:
		raise LogParserError(f"Error reading file: {str(e)}")
