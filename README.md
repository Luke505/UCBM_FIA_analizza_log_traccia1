# Log Analysis System

A clean, modular Python application for analyzing log files and generating user statistics.

## Features

- Parse JSON log files containing lists of log entries
- Filter logs by timestamp range and IP address
- Generate comprehensive user statistics including:
	- First and last access timestamps
	- Total access counter
	- Usage age (human-readable duration between first and last access)
	- Unique IP addresses used
	- Unique event contexts
- Export filtered logs and statistics to JSON
- Comprehensive error handling
- Full test coverage

## Requirements

- Python 3.8 or higher
- No external dependencies (uses standard library only)

## Project Structure

```
.
├── models.py          # Data models (LogEntry, UserStats)
├── parser.py          # JSON log file parser
├── filters.py         # Log filtering functions
├── analyzer.py        # User statistics generation
├── main.py            # Main entry point and CLI
├── requirements.txt   # Python dependencies
├── tests/             # Test suite
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_filters.py
│   ├── test_analyzer.py
│   └── test_integration.py
└── test_data/         # Sample test data
    ├── test_simple.json
    ├── test_small.json
    └── test_large.json
```

## Input Format

The input JSON file must contain a list of lists, where each inner list represents a log entry with exactly 8 fields:

```json
[
   [
      "3/11/2021 18:42",
      "00001",
      "Corso: Fondamenti di informatica [20-21]",
      "Log",
      "Visualizzato report log",
      "The user with id '7' viewed the log report for the course with id '488'.",
      "web",
      "192.168.103.208"
   ],
   [
      "3/11/2021 18:42",
      "00001",
      "Corso: Fondamenti di informatica [20-21]",
      "Sistema",
      "Visualizzato corso",
      "The user with id '7' viewed the course with id '488'.",
      "web",
      "192.168.103.208"
   ]
]
```

**Fields (in order):**

1. `timestamp` - Date and time (various formats supported)
2. `user_id` - User identifier
3. `event_context` - Context of the event
4. `component` - System component
5. `event` - Event type
6. `description` - Event description
7. `origin` - Event origin
8. `ip_address` - IP address

## Output Format

### Filtered Logs (`filtered_logs.json`)

List of log entry objects matching the applied filters:

```json
[
	{
		"timestamp": "2024-01-15T10:00:00",
		"user_id": "user1",
		"event_context": "web",
		"component": "auth",
		"event": "login",
		"description": "User logged in",
		"origin": "frontend",
		"ip_address": "192.168.1.1"
	}
]
```

### User Statistics (`user_stats.json`)

Aggregated statistics for each user:

```json
[
	{
		"user_id": "user1",
		"first_timestamp": "2024-01-15T10:00:00",
		"last_timestamp": "2024-01-15T13:00:00",
		"access_counter": 3,
		"usage_age": "3 hours",
		"ip_addresses": [
			"192.168.1.1",
			"192.168.1.3"
		],
		"event_contexts": [
			"api",
			"web"
		]
	}
]
```

**Note:** `usage_age` is formatted as a human-readable duration string (e.g., "2 days, 3 hours, 15 minutes").

## Usage

### Basic Usage

Process a log file without filters:

```bash
python main.py test_data/test_simple.json
```

This will generate:

- `filtered_logs.json` - All log entries
- `user_stats.json` - Statistics for all users

### With Filters

Filter by timestamp range:

```bash
python main.py test_data/test_simple.json \
  --start-timestamp "2024-01-15 10:00:00" \
  --end-timestamp "2024-01-15 12:00:00"
```

Filter by IP address:

```bash
python main.py test_data/test_simple.json \
  --ip-address "192.168.1.1"
```

Combine multiple filters:

```bash
python main.py test_data/test_simple.json \
  --start-timestamp "2024-01-15 10:00:00" \
  --end-timestamp "2024-01-15 12:00:00" \
  --ip-address "192.168.1.1"
```

### Custom Output Paths

```bash
python main.py test_data/test_simple.json \
  --output-logs my_logs.json \
  --output-stats my_stats.json
```

### Command-Line Options

```
positional arguments:
  file_path             Path to input JSON log file

optional arguments:
  -h, --help            Show help message and exit
  --output-logs PATH    Path for filtered logs output (default: filtered_logs.json)
  --output-stats PATH   Path for user statistics output (default: user_stats.json)
  --start-timestamp TS  Filter start timestamp (ISO format: YYYY-MM-DD HH:MM:SS)
  --end-timestamp TS    Filter end timestamp (ISO format: YYYY-MM-DD HH:MM:SS)
  --ip-address IP       Filter by IP address
```

## Programmatic Usage

You can also use the modules directly in your Python code:

```python
from datetime import datetime
from main import process_log_file

# Process with filters
process_log_file(
	file_path="test_data/test_simple.json",
	output_logs_path="output_logs.json",
	output_stats_path="output_stats.json",
	filter_start_timestamp=datetime(2024, 1, 15, 10, 0, 0),
	filter_end_timestamp=datetime(2024, 1, 15, 12, 0, 0),
	filter_ip_address="192.168.1.1"
)
```

Or use individual modules:

```python
from parser import parse_log_file
from filters import apply_filters
from analyzer import generate_user_stats
from datetime import datetime

# Parse log file
log_entries = parse_log_file("test_data/test_simple.json")

# Apply filters
filtered = apply_filters(
	log_entries,
	filter_start_timestamp=datetime(2024, 1, 15, 10, 0, 0)
)

# Generate statistics
stats = generate_user_stats(filtered)

# Access results
for stat in stats:
	print(f"User {stat.user_id}: {stat.access_counter} accesses")
```

## Running Tests

Run all tests:

```bash
python -m unittest discover tests
```

Run specific test modules:

```bash
python -m unittest tests.test_parser
python -m unittest tests.test_filters
python -m unittest tests.test_analyzer
python -m unittest tests.test_integration
```

Run with verbose output:

```bash
python -m unittest discover tests -v
```

## Error Handling

The application includes comprehensive error handling:

- **File not found**: Clear error message if input file doesn't exist
- **Invalid JSON**: Descriptive error for malformed JSON
- **Invalid format**: Validation errors for incorrect data structure
- **Invalid timestamps**: Errors for unparseable timestamp formats
- **IO errors**: Proper handling of file read/write errors

Example error messages:

```
Error parsing log file: File not found: nonexistent.json
Error parsing log file: Entry 5 must have exactly 8 fields, got 7
Error parsing log file: Unable to parse timestamp: invalid-date
```

## Testing Coverage

The test suite includes:

- **Valid inputs**: Standard use cases with various data sizes
- **Invalid inputs**: Malformed JSON, wrong formats, missing fields
- **Edge cases**: Empty files, single entries, boundary timestamps
- **Integration tests**: End-to-end workflows with various filter combinations

## Performance

The application efficiently handles large log files:

- Streaming JSON parsing for memory efficiency
- Single-pass filtering and aggregation
- Optimized data structures for statistics generation

Tested with files containing:

- Simple: 22 entries
- Small: 98 entries
- Large: 83627 entries

## License

This project is provided as-is for educational and professional use.