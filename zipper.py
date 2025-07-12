


# Copyright (c) 2025 ethereald
# Author: ethereald
#
# MIT License
#
# This script provides utilities to backup and restore Lora model files for ComfyUI by encoding them into JSON archives.
#
# Functions:
#   - zip_folder: Encode files in a folder into JSON archives, optionally to a different output directory.
#   - unzip_folder: Restore files from JSON archives in a folder.
#   - main: Command-line interface for zip/unzip operations.

import os
import sys
import shutil
import zipfile
from pathlib import Path

MAX_ZIP_SIZE = 1 * 1024 * 1024  # 1MB

def zip_folder(folder_path):
    """
    Encode all files in the specified folder into JSON archives, splitting large files into chunks.
    Optionally, output the archives to a different directory.

    Args:
        folder_path (str or list): Path to the folder to encode, or [source_folder, output_dir].

    Returns:
        None. Prints status and creates JSON files.
    """
    import base64, json
    output_dir = None
    if isinstance(folder_path, (list, tuple)):
        folder = Path(folder_path[0])
        output_dir = Path(folder_path[1]) if len(folder_path) > 1 else None
    else:
        folder = Path(folder_path)
    if not folder.is_dir():
        print(f"{folder} is not a valid directory.")
        return
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = folder
    files = [f for f in folder.rglob('*') if f.is_file()]
    json_idx = 1
    current_json_size = 0
    current_json_files = []
    json_files = []
    import json as _json
    for file in files:
        rel_path = str(file.relative_to(folder))
        file_size = file.stat().st_size
        if file_size > MAX_ZIP_SIZE:
            with open(file, 'rb') as file_data:
                chunk_idx = 0
                while True:
                    chunk = file_data.read(MAX_ZIP_SIZE)
                    if not chunk:
                        break
                    encoded = base64.b64encode(chunk).decode('utf-8')
                    entry = {'relative_path': rel_path, 'chunk_index': chunk_idx, 'content': encoded}
                    entry_size = len(_json.dumps(entry).encode('utf-8'))
                    if current_json_size + entry_size > MAX_ZIP_SIZE and current_json_files:
                        json_name = output_dir / f"archive_{json_idx}.json"
                        with open(json_name, 'w', encoding='utf-8') as jf:
                            _json.dump(current_json_files, jf)
                        json_files.append(json_name)
                        json_idx += 1
                        current_json_size = 0
                        current_json_files = []
                    current_json_files.append(entry)
                    current_json_size += entry_size
                    chunk_idx += 1
        else:
            with open(file, 'rb') as file_data:
                encoded = base64.b64encode(file_data.read()).decode('utf-8')
            entry = {'relative_path': rel_path, 'content': encoded}
            entry_size = len(_json.dumps(entry).encode('utf-8'))
            if current_json_size + entry_size > MAX_ZIP_SIZE and current_json_files:
                json_name = output_dir / f"archive_{json_idx}.json"
                with open(json_name, 'w', encoding='utf-8') as jf:
                    _json.dump(current_json_files, jf)
                json_files.append(json_name)
                json_idx += 1
                current_json_size = 0
                current_json_files = []
            current_json_files.append(entry)
            current_json_size += entry_size
    if current_json_files:
        json_name = output_dir / f"archive_{json_idx}.json"
        with open(json_name, 'w', encoding='utf-8') as jf:
            json.dump(current_json_files, jf)
        json_files.append(json_name)
    # Only delete files/folders if output_dir is not provided
    if not (output_dir and output_dir != folder):
        for file in files:
            if file.is_file() and not str(file).endswith('.json'):
                file.unlink()
        # Remove all empty folders except the root
        dirs = sorted([d for d in folder.rglob('*') if d.is_dir() and d != folder], key=lambda x: -len(str(x)))
        for d in dirs:
            try:
                d.rmdir()
            except OSError:
                pass
        print(f"Encoded into {len(json_files)} JSON files and deleted originals.")
    else:
        print(f"Encoded into {len(json_files)} JSON files in {output_dir} (source files not deleted).")

def unzip_folder(folder_path):
    """
    Restore files from JSON archives in the specified folder.
    Reassembles large files from chunks and deletes JSON archives after extraction.

    Args:
        folder_path (str): Path to the folder containing JSON archives.

    Returns:
        None. Prints status and restores files.
    """
    import base64, json
    folder = Path(folder_path)
    json_files = list(folder.glob('*.json'))
    # Collect all chunks for each file
    file_chunks = {}
    restored_files = set()
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
        for entry in data:
            rel_path = entry['relative_path']
            content = base64.b64decode(entry['content'])
            chunk_index = entry.get('chunk_index')
            if chunk_index is not None:
                if rel_path not in file_chunks:
                    file_chunks[rel_path] = {}
                file_chunks[rel_path][chunk_index] = content
            else:
                out_path = folder / rel_path
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with open(out_path, 'wb') as f:
                    f.write(content)
                restored_files.add(rel_path)
        json_file.unlink()  # Remove JSON after extraction
    # Reassemble large files from chunks
    for rel_path, chunks in file_chunks.items():
        out_path = folder / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'wb') as f:
            for idx in sorted(chunks.keys()):
                f.write(chunks[idx])
        restored_files.add(rel_path)
    print(f"Restored {len(restored_files)} files and removed JSON files.")

def main():
    """
    Command-line interface for zipper.py.
    Usage:
        python zipper.py <zip|unzip> <folder_path> [output_dir_for_zip]

    Operations:
        zip: Encode files in folder_path into JSON archives. Optionally specify output_dir_for_zip.
        unzip: Restore files from JSON archives in folder_path.
    """
    if len(sys.argv) < 3:
        print("Usage: python zipper.py <zip|unzip> <folder_path> [output_dir_for_zip]")
        return
    operation = sys.argv[1].lower()
    folder_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    if operation == 'zip':
        if output_dir:
            zip_folder([folder_path, output_dir])
        else:
            zip_folder(folder_path)
    elif operation == 'unzip':
        unzip_folder(folder_path)
    else:
        print("Invalid operation. Use 'zip' or 'unzip'.")

if __name__ == "__main__":
    main()
