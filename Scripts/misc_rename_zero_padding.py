import json
import os
from typing import List, Tuple

import file_paths

# TODO: just convert everything to be padded, and then no need for this file

# The cloud.annotations.ai service sorts images by name, this leads to the order
# ..., Snap-169.jpg, Snap-17.jpg, Snap-170.jpg, ...
# This makes it hard to properly annotate images since images of different focal lengths are not consecutive.
# Solution: rename images in JPEG_small with left zero padding. Also support renaming instances in _annotations.json
# file.

# Typical workflow:
# Take images, 17-Snap.jpg, 18-Snap.jpg...
# Run this script with convert_from_nopad_to_padded = True
# Upload resulting images to annotations service
# Annotate all images, download _annotations.json
# Run this script with convert_from_nopad_to_padded = False, and correct paths to annotations file
# Use converted annotations file

annotations_file_nopad = os.path.join(file_paths.dataset_root_directory, "Annotations", "oslo_2019-03-22_annotations.json")
annotations_file_withpad = os.path.join(file_paths.dataset_root_directory, "Annotations", "oslo_2019-03-22_annotations_padded.json")

convert_from_nopad_to_padded = True


def main():
    rename_jobs: List[Tuple[str, str]] = []
    for root_path, dirs, files in os.walk(os.path.join(file_paths.JPEGs_small_directory, "2019Oslo_22-03-kl13")):
        for file in files:
            if not file.endswith(".jpg"):
                continue
            next_filename = filename_pad(file) if convert_from_nopad_to_padded else filename_undo_pad(file)
            if file != next_filename:
                rename_jobs.append((os.path.join(root_path, file), os.path.join(root_path, next_filename)))

    print(f"Renaming {len(rename_jobs)} files...")
    for prev_name, next_name in rename_jobs:
        print(f"{prev_name} => {next_name}")
        os.rename(prev_name, next_name)

    # handle annotations file
    if convert_from_nopad_to_padded:
        if not os.path.exists(annotations_file_nopad):
            print("No annotations file found, won't convert annotations from nopad to padded")
        else:
            print("Converting annotations file from nopad to padded")
            print(f"From {annotations_file_nopad}\n  to {annotations_file_withpad}")
            with open(annotations_file_nopad, "r", encoding="utf-8") as f:
                annotations_content = json.load(f)
            annotations_dict = annotations_content["annotations"]
            key_value_list = []
            for filename, annotations_data in annotations_dict.items():
                next_filename = filename_pad(filename)
                key_value_list.append((next_filename, annotations_data))
            key_value_list.sort(key=lambda el: el[0])
            next_annotations_dict = dict()
            for filename, annotations_data in key_value_list:
                next_annotations_dict[filename] = annotations_data
            annotations_content["annotations"] = next_annotations_dict
            with open(annotations_file_withpad, "w", encoding="utf-8") as f:
                json.dump(annotations_content, f)
    else:
        if not os.path.exists(annotations_file_withpad):
            print("No annotations file found, won't convert annotations from padded to nopad")
        else:
            print("Converting annotations file from padded to nopad")
            print(f"From {annotations_file_withpad}\n  to {annotations_file_nopad}")
            with open(annotations_file_withpad, "r", encoding="utf-8") as f:
                annotations_content = json.load(f)
            annotations_dict = annotations_content["annotations"]
            key_value_list = []
            for filename, annotations_data in annotations_dict.items():
                next_filename = filename_undo_pad(filename)
                key_value_list.append((next_filename, annotations_data))
            key_value_list.sort(key=lambda el: el[0])
            next_annotations_dict = dict()
            for filename, annotations_data in key_value_list:
                next_annotations_dict[filename] = annotations_data
            annotations_content["annotations"] = next_annotations_dict
            with open(annotations_file_nopad, "w", encoding="utf-8") as f:
                json.dump(annotations_content, f)


def filename_pad(base_filename: str) -> str:
    base, ext = os.path.splitext(base_filename)
    snap, num = base.rsplit("-", 1)
    num2 = "0" * (3 - len(num)) + num  # 16 -> 016
    return "-".join([snap, num2]) + ext


def filename_undo_pad(base_filename: str) -> str:
    base, ext = os.path.splitext(base_filename)
    snap, num = base.rsplit("-", 1)
    num2 = str(int(num))  # 016 -> 16
    return "-".join([snap, num2]) + ext


if __name__ == '__main__':
    main()
