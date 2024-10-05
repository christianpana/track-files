# File Indexer

A simple Python script to index files in a directory, compute their checksums, and store metadata in a database.

## Overview

This script recursively scans a specified directory, processes each file to collect metadata, and saves the information to a database. The collected metadata includes:

- **Absolute Path**: Full path to the file.
- **Relative Path**: Path relative to the starting directory.
- **Size**: File size in bytes.
- **Creation Time**: Timestamp when the file was created.
- **Modification Time**: Timestamp when the file was last modified.
- **Checksum**: SHA-256 hash of the file contents.
- **Indexed At**: Timestamp when the file was indexed.

## Usage

    python file_indexer.py [start_path] [db_path]

- `start_path` *(optional)*: The directory to start indexing from. Defaults to the current directory (`./`) if not specified.
- `db_path` *(optional)*: The path to the database file where metadata will be stored. Defaults to `./files.db` if not specified.

## Examples

### Index the current directory and store metadata in `files.db`

    python file_indexer.py

### Index a specific directory and store metadata in a custom database

    python file_indexer.py /path/to/directory /path/to/my_files.db

### Index the current directory and specify a custom database file

    python file_indexer.py ./ /tmp/custom_files.db

## Notes

- Folders are not saved to the db.
- The script processes files in batches of 100 for efficient database insertion.
- Symbolic links are not followed during indexing.
- If a file cannot be processed, an error message will be displayed, and the script will continue with the next file.

## TODO
- Save progress