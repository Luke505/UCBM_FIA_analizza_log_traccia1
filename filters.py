"""Filtering module for log entries."""

from datetime import datetime
from typing import List, Optional

from models import LogEntry


def apply_filters(
	log_entries: List[LogEntry],
	filter_start_timestamp: Optional[datetime] = None,
	filter_end_timestamp: Optional[datetime] = None,
	filter_ip_address: Optional[str] = None
) -> List[LogEntry]:
	"""
	Apply filters to log entries.

	Args:
		log_entries: List of log entries to filter
		filter_start_timestamp: Include entries on or after this timestamp
		filter_end_timestamp: Include entries on or before this timestamp
		filter_ip_address: Include only entries with this IP address

	Returns:
		Filtered list of log entries
	"""
	filtered = log_entries

	# Apply timestamp filters
	if filter_start_timestamp is not None:
		filtered = [
			entry for entry in filtered
			if entry.timestamp >= filter_start_timestamp
		]

	if filter_end_timestamp is not None:
		filtered = [
			entry for entry in filtered
			if entry.timestamp <= filter_end_timestamp
		]

	# Apply IP address filter
	if filter_ip_address is not None:
		filtered = [
			entry for entry in filtered
			if entry.ip_address == filter_ip_address
		]

	return filtered
