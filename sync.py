import os
import shutil
import argparse
import hashlib
import time


def sync_folders(source, replica, interval, log_file):
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(replica)

    while True:
        for root, _, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_dir = os.path.join(replica, relative_path)

            # Create the corresponding directory in the replica folder if it doesn't exist
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)

            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_dir, file)

                # Compare the MD5 hash of the source file and the replica file (if it exists)
                source_hash = md5_hash(source_file)
                replica_hash = md5_hash(replica_file) if os.path.exists(replica_file) else None

                # If the file doesn't exist in the replica folder or the hashes don't match, copy the file
                if not os.path.exists(replica_file) or source_hash != replica_hash:
                    print("Copying file:", source_file)
                    shutil.copy2(source_file, replica_file)
                    log("Copied file: " + source_file, log_file)

        time.sleep(interval)


def md5_hash(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def log(message, log_file):
    print(message)
    with open(log_file, "a") as file:
        file.write(message + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    sync_folders(args.source, args.replica, args.interval, args.log_file)
