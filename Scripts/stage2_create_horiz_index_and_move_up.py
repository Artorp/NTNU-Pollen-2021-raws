import json
import os
from typing import List, Tuple, Set

import file_paths

# Stage 2:
# After creating the TIF files, move them up a directory level and create a horiz index file
# Before: SlideID1/Horiz1_75/a.tif, SlideID1/Horiz1_75/b.tif, SlideID/Horiz2_77/c.tif
# After: SlideID1/a.tif, SlideID1/b.tif, SlideID/c.tif


def main():
    index_filename = "horiz_index.json"
    index_file = os.path.join(file_paths.dataset_root_directory, index_filename)
    if os.path.exists(index_file):
        print(f"Index file {index_file} already exists, exiting...")
        exit(0)

    index_dict = dict()
    index_dict["horizontal_ids"] = []
    index_dict["mapping"] = dict()

    rename_jobs: List[Tuple[str, str]] = []
    rmdir_jobs: Set[str] = set()

    for path, dirs, files in os.walk(file_paths.TIFs_directory):
        for file in files:
            if not file.endswith(".tif"):
                continue
            destination_dir, horiz_name = os.path.split(path)
            if len(index_dict["horizontal_ids"]) == 0 or index_dict["horizontal_ids"][-1] != horiz_name:
                index_dict["horizontal_ids"].append(horiz_name)
            h_idx = len(index_dict["horizontal_ids"]) - 1
            index_dict["mapping"][file] = {"h_idx": h_idx}
            # move file one stage up
            rename_jobs.append((os.path.join(path, file), os.path.join(destination_dir, file)))
            # delete old directory if it is empty
            rmdir_jobs.add(path)

    for src, des in rename_jobs:
        print(src, "=>", des)
        os.rename(src, des)
    for path in sorted(rmdir_jobs):
        print("Deleting", path)
        os.rmdir(path)

    with open(index_file, "w", encoding="utf-8") as file:
        print("Creating index file", index_file)
        json.dump(index_dict, file, indent=2)


if __name__ == '__main__':
    main()
