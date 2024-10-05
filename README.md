# track-files

## index-all-files
A simple Python script to index files in a directory, compute their checksums, and store metadata in a database.

## copy-missing-files
This repository contains a Python script that recursively copies missing files from a source folder to a destination folder, collects specific file information, and stores it in a local SQLite database. The script is designed to work on both Windows and Linux systems.

## sync-files-date-modified
This Python script copies updated and missing files from a source directory to a destination directory. It checks if files have been modified within a user-specified time frame and saves file metadata such as file size, creation time, modification time, and checksum to a local SQLite database.