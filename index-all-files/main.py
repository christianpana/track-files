import os
import sys
import time
import hashlib
from db import FileIndexDB

def calculate_checksum(file_path):
    hash_func = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Failed to calculate checksum for {file_path}: {e}")
        return None

def process_file(file_path, start_path, indexed_at):
    relative_path = os.path.relpath(file_path, start_path)
    try:
        stat = os.stat(file_path)
        size = stat.st_size
        created = stat.st_ctime
        modified = stat.st_mtime
        checksum = calculate_checksum(file_path)
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
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return None

def walk_directory(path):
    for root, dirs, files in os.walk(path, followlinks=False):
        for name in files:
            yield os.path.join(root, name)

def main(start_path, db_path):
    db = FileIndexDB(db_path)
    start_time = time.time()
    indexed_at = time.time()
    file_infos = []
    batch_size = 100

    for file_path in walk_directory(start_path):
        file_info = process_file(file_path, start_path, indexed_at)
        if file_info:
            file_infos.append(file_info)
            if len(file_infos) >= batch_size:
                db.add_files(file_infos)
                print(".")
                file_infos = []

    # Insert any remaining files
    if file_infos:
        db.add_files(file_infos)
        print(".")

    db.close()
    elapsed_time = time.time() - start_time
    print(f"Indexing completed in {elapsed_time:.2f} seconds.")


if __name__ == '__main__':
    try:
        start_path = sys.argv[1]
    except IndexError:
        start_path = "./"

    try:
        db_path = sys.argv[2]
    except IndexError:
        db_path = "./files.db"

    main(start_path, db_path)
