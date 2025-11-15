"""Main entry point for log analysis."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from analyzer import generate_user_stats
from filters import apply_filters
from parser import LogParserError, parse_log_file


def process_log_file(
	file_path: str,
	output_logs_path: str = "filtered_logs.json",
	output_stats_path: str = "user_stats.json",
	filter_start_timestamp: Optional[datetime] = None,
	filter_end_timestamp: Optional[datetime] = None,
	filter_ip_address: Optional[str] = None
) -> None:
	"""
	Process log file and generate output files with filtered logs and user statistics.

	Args:
		file_path: Path to input JSON log file
		output_logs_path: Path for filtered logs output file
		output_stats_path: Path for user statistics output file
		filter_start_timestamp: Optional start timestamp filter
		filter_end_timestamp: Optional end timestamp filter
		filter_ip_address: Optional IP address filter

	Raises:
		LogParserError: If input file cannot be parsed
		IOError: If output files cannot be written
	"""
	# Parse input file
	print(f"Parsing log file: {file_path}")
	log_entries = parse_log_file(file_path)
	print(f"Parsed {len(log_entries)} log entries")

	# Apply filters
	filtered_entries = apply_filters(
		log_entries,
		filter_start_timestamp=filter_start_timestamp,
		filter_end_timestamp=filter_end_timestamp,
		filter_ip_address=filter_ip_address
	)
	print(f"After filtering: {len(filtered_entries)} log entries")

	# Generate filtered logs output
	print(f"Writing filtered logs to: {output_logs_path}")
	logs_output = [entry.to_dict() for entry in filtered_entries]
	with open(output_logs_path, 'w', encoding='utf-8') as f:
		json.dump(logs_output, f, indent=2, ensure_ascii=False)

	# Generate user statistics
	print(f"Generating user statistics")
	user_stats = generate_user_stats(filtered_entries)
	print(f"Generated statistics for {len(user_stats)} users")

	# Generate user stats output
	print(f"Writing user statistics to: {output_stats_path}")
	stats_output = [stats.to_dict() for stats in user_stats]
	with open(output_stats_path, 'w', encoding='utf-8') as f:
		json.dump(stats_output, f, indent=2, ensure_ascii=False)

	print("Processing complete!")


def main():
	"""Command-line entry point with example usage."""
	import argparse

	parser = argparse.ArgumentParser(
		description='Analyze log files and generate statistics'
	)
	parser.add_argument(
		'file_path',
		help='Path to input JSON log file'
	)
	parser.add_argument(
		'--output-logs',
		default='filtered_logs.json',
		help='Path for filtered logs output (default: filtered_logs.json)'
	)
	parser.add_argument(
		'--output-stats',
		default='user_stats.json',
		help='Path for user statistics output (default: user_stats.json)'
	)
	parser.add_argument(
		'--start-timestamp',
		help='Filter start timestamp (ISO format: YYYY-MM-DD HH:MM:SS)'
	)
	parser.add_argument(
		'--end-timestamp',
		help='Filter end timestamp (ISO format: YYYY-MM-DD HH:MM:SS)'
	)
	parser.add_argument(
		'--ip-address',
		help='Filter by IP address'
	)

	args = parser.parse_args()

	# Parse timestamp arguments if provided
	start_timestamp = None
	end_timestamp = None

	if args.start_timestamp:
		try:
			start_timestamp = datetime.fromisoformat(args.start_timestamp)
		except ValueError:
			print(f"Error: Invalid start timestamp format: {args.start_timestamp}")
			return

	if args.end_timestamp:
		try:
			end_timestamp = datetime.fromisoformat(args.end_timestamp)
		except ValueError:
			print(f"Error: Invalid end timestamp format: {args.end_timestamp}")
			return

	try:
		process_log_file(
			file_path=args.file_path,
			output_logs_path=args.output_logs,
			output_stats_path=args.output_stats,
			filter_start_timestamp=start_timestamp,
			filter_end_timestamp=end_timestamp,
			filter_ip_address=args.ip_address
		)
	except LogParserError as e:
		print(f"Error parsing log file: {e}")
	except IOError as e:
		print(f"Error writing output files: {e}")
	except Exception as e:
		print(f"Unexpected error: {e}")


if __name__ == "__main__":
	main()
