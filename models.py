"""Data models for log entries and user statistics."""

from dataclasses import dataclass
from datetime import datetime
from typing import List


def format_duration(seconds: float) -> str:
	"""
	Convert duration in seconds to human-readable format.

	Args:
		seconds: Duration in seconds

	Returns:
		Human-readable string (e.g., "2 days, 3 hours, 15 minutes")
	"""
	if seconds == 0:
		return "0 seconds"

	days = int(seconds // 86400)
	remaining = seconds % 86400
	hours = int(remaining // 3600)
	remaining = remaining % 3600
	minutes = int(remaining // 60)
	secs = int(remaining % 60)

	parts = []
	if days > 0:
		parts.append(f"{days} day{'s' if days != 1 else ''}")
	if hours > 0:
		parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
	if minutes > 0:
		parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
	if secs > 0 and not parts:  # Only show seconds if no larger units
		parts.append(f"{secs} second{'s' if secs != 1 else ''}")

	return ", ".join(parts) if parts else "0 seconds"


@dataclass
class LogEntry:
	"""Represents a single log entry."""
	timestamp: datetime
	user_id: str
	event_context: str
	component: str
	event: str
	description: str
	origin: str
	ip_address: str

	def to_dict(self) -> dict:
		"""Convert log entry to dictionary with ISO format timestamp."""
		return {
			"timestamp": self.timestamp.isoformat(),
			"user_id": self.user_id,
			"event_context": self.event_context,
			"component": self.component,
			"event": self.event,
			"description": self.description,
			"origin": self.origin,
			"ip_address": self.ip_address
		}


@dataclass
class UserStats:
	"""Represents aggregated statistics for a user."""
	user_id: str
	first_timestamp: datetime
	last_timestamp: datetime
	access_counter: int
	usage_age: float  # duration in seconds
	ip_addresses: List[str]
	event_contexts: List[str]

	def to_dict(self) -> dict:
		"""Convert user stats to dictionary with ISO format timestamps and human-readable duration."""
		return {
			"user_id": self.user_id,
			"first_timestamp": self.first_timestamp.isoformat(),
			"last_timestamp": self.last_timestamp.isoformat(),
			"access_counter": self.access_counter,
			"usage_age": format_duration(self.usage_age),
			"ip_addresses": self.ip_addresses,
			"event_contexts": self.event_contexts
		}
