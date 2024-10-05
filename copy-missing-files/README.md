# Copy Missing Files
This repository contains a Python script that recursively copies missing files from a source folder to a destination folder, collects specific file information, and stores it in a local SQLite database. The script is designed to work on both Windows and Linux systems.

Features
- Recursive File Copying: Copies files from the source directory to the destination directory, preserving the directory structure.
- Missing File Detection: Only copies files that do not already exist in the destination directory.
- File Indexing: Collects file metadata, including absolute and relative paths, size, creation and modification times, checksums, and indexing timestamp.
- SQLite Database Storage: Stores the collected file information in a local SQLite database using the provided FileIndexDB class.
- Batch Processing: Processes files in batches to improve performance when dealing with a large number of files.
- Cross-Platform Compatibility: Works seamlessly on both Windows and Linux systems.

### Notes
- Empty folders are not copied

### Usage

#### Example
```commandline
python main.py ./sample-source ./sample-destination
```

#### Command-Line Arguments
The script accepts the following command-line arguments:
- `source_folder` (required): Path to the source directory.
- `destination_folder` (required): Path to the destination directory.
- `--db-path` (optional): Path to the SQLite database file. Defaults to file_index.db in the current directory.
- `--batch-size` (optional): Number of files to process before writing to the database. Defaults to 100.

#### Parameters Explained
- `/path/to/source`: Replace with the absolute or relative path to your source directory containing the files you want to copy and index.
- `/path/to/destination`: Replace with the path to your destination directory where missing files will be copied.
- `--db-path`: (Optional) Specify the path to the SQLite database file where file information will be stored. If omitted, defaults to files.db in the current working directory.
- `--batch-size`: (Optional) Define the number of files to process before committing the data to the database. Adjusting this can improve performance with large datasets.
