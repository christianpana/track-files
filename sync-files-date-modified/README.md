## File Sync & Indexing Script

### Overview

This Python script copies updated and missing files from a source directory to a destination directory. It checks if files have been modified within a user-specified time frame and saves file metadata such as file size, creation time, modification time, and checksum to a local SQLite database.

The script works on both Windows and Linux systems and ensures that the file copy and indexing are efficient and reliable.

### Usage

1. **Source Folder**: Directory from which files will be copied.
2. **Destination Folder**: Directory where files will be copied to.
3. **SQLite DB**: Stores metadata of copied files.

### Command Line Arguments

- `source_folder`: Path to the source folder (required).
- `destination_folder`: Path to the destination folder (required).
- `--db-path`: Path to the SQLite database file (default: `files.db`).
- `--time`: Time threshold (in hours) to check for file modifications (default: `24`).
- `--batch-size`: Number of files to process before committing to the database (default: `100`).

### Examples

```bash
# Copy files modified in the last 24 hours
python main.py /path/to/source /path/to/destination

# Copy files modified in the last 48 hours, with custom batch size
python main.py /path/to/source /path/to/destination --time 48 --batch-size 200

# Use a custom SQLite database file
python main.py /path/to/source /path/to/destination --db-path /path/to/custom.db
```

This script ensures that only modified or missing files are copied, saving you time and ensuring consistency across directories.
