"""Analyzer module for generating user statistics from log entries."""

from collections import defaultdict
from typing import Dict, List

from models import LogEntry, UserStats


def generate_user_stats(log_entries: List[LogEntry]) -> List[UserStats]:
	"""
	Generate aggregated statistics for each user from log entries.

	Args:
		log_entries: List of log entries to analyze

	Returns:
		List of UserStats objects, one per unique user_id
	"""
	if not log_entries:
		return []

	# Group entries by user_id
	user_data: Dict[str, List[LogEntry]] = defaultdict(list)
	for entry in log_entries:
		user_data[entry.user_id].append(entry)

	# Generate stats for each user
	user_stats_list = []
	for user_id, entries in user_data.items():
		# Sort entries by timestamp
		sorted_entries = sorted(entries, key=lambda e: e.timestamp)

		first_timestamp = sorted_entries[0].timestamp
		last_timestamp = sorted_entries[-1].timestamp
		access_counter = len(entries)

		# Calculate usage age in seconds
		usage_age = (last_timestamp - first_timestamp).total_seconds()

		# Collect unique IP addresses and event contexts
		ip_addresses = list(set(entry.ip_address for entry in entries))
		event_contexts = list(set(entry.event_context for entry in entries))

		# Sort for consistent output
		ip_addresses.sort()
		event_contexts.sort()

		user_stats = UserStats(
			user_id=user_id,
			first_timestamp=first_timestamp,
			last_timestamp=last_timestamp,
			access_counter=access_counter,
			usage_age=usage_age,
			ip_addresses=ip_addresses,
			event_contexts=event_contexts
		)
		user_stats_list.append(user_stats)

	# Sort by user_id for consistent output
	user_stats_list.sort(key=lambda s: s.user_id)

	return user_stats_list
