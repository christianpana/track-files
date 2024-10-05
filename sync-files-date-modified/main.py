import os
import shutil
import time
import argparse
import hashlib
from db import FileIndexDB

def calculate_checksum(file_path):
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096 * 1024), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error computing checksum for {file_path}: {e}")
        return None

def file_was_modified_recently(file_path, time_threshold):
    modified_time = os.path.getmtime(file_path)
    return (time.time() - modified_time) <= time_threshold

def process_file(file_path, source_path, dest_path, indexed_at, time_threshold):
    relative_path = os.path.relpath(file_path, source_path)
    destination_file = os.path.join(dest_path, relative_path)

    try:
        stat = os.stat(file_path)
        size = stat.st_size
        created = stat.st_ctime
        modified = stat.st_mtime
        checksum = calculate_checksum(file_path)

        # If file is missing in destination or was modified recently
        if not os.path.exists(destination_file) or file_was_modified_recently(file_path, time_threshold):
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copy2(file_path, destination_file)
            print(f"Copied {destination_file}")

            file_info = {
                'absolute_path': os.path.abspath(file_path),
                'relative_path': relative_path,
                'size': size,
                'created': created,
                'modified': modified,
                'checksum': checksum,
                'indexed_at': indexed_at
            }
            return file_info
        else:
            return None
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return None

def walk_directory(path):
    for root, dirs, files in os.walk(path, followlinks=False):
        for name in files:
            yield os.path.join(root, name)

def main():
    parser = argparse.ArgumentParser(
        description='Copy missing or updated files from source to destination and index them.')
    parser.add_argument('source_folder', help='Path to the source folder')
    parser.add_argument('destination_folder', help='Path to the destination folder')
    parser.add_argument('--db-path', default='files.db', help='Path to the SQLite database file')
    parser.add_argument('--time', type=float, default=24,
                        help='Time threshold (in hours) to consider files for copying')
    parser.add_argument('--batch-size', type=int, default=100,
                        help='Number of files to process before writing to the database')

    args = parser.parse_args()

    source_path = os.path.abspath(args.source_folder)
    dest_path = os.path.abspath(args.destination_folder)
    db_path = os.path.abspath(args.db_path)
    time_threshold = args.time * 3600
    batch_size = args.batch_size

    db = FileIndexDB(db_path)
    indexed_at = time.time()
    file_infos = []

    try:
        for file_path in walk_directory(source_path):
            file_info = process_file(file_path, source_path, dest_path, indexed_at, time_threshold)
            if file_info:
                file_infos.append(file_info)
                if len(file_infos) >= batch_size:
                    db.add_files(file_infos)
                    print(f"Indexed {len(file_infos)} files.")
                    file_infos = []
        # Insert any remaining files
        if file_infos:
            db.add_files(file_infos)
            print(f"Indexed {len(file_infos)} files.")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        db.close()

if __name__ == '__main__':
    main()
