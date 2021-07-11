import os
from typing import List, Tuple

import file_paths

# Stage 4:
# After converting images to jpegs, manually delete files which are unsuitable for the training set.
# These images may be too blurry to be used, been taken by mistake without a good subject,
# or be duplicate of other images.
# This was done manually in the jpeg folder. This means that the tif folder will have the undeleted
# images. This script will just keep a count of which images were deleted and list them
# in deleted_images.txt.


def main():
    images_in_jpeg_folder = set()
    for root_path, dirs, files in os.walk(file_paths.JPEGs_directory):
        for file in files:
            if not file.endswith(".jpg"):
                continue
            base_filename, ext = os.path.splitext(file)
            images_in_jpeg_folder.add(base_filename)

    images_deleted: List[Tuple[str, str]] = list()
    for root_path, dirs, files in os.walk(file_paths.TIFs_directory):
        for file in files:
            if not file.endswith(".tif"):
                continue
            base_filename, ext = os.path.splitext(file)
            _, slide_id = os.path.split(root_path)
            if base_filename not in images_in_jpeg_folder:
                images_deleted.append((slide_id, base_filename))

    images_deleted_textfile = os.path.join(file_paths.dataset_root_directory, "stage4_images_deleted.txt")
    print(f"Detected {len(images_deleted)} images deleted, writing to {images_deleted_textfile}")
    with open(images_deleted_textfile, "w", encoding="utf-8") as f:
        for slide_id, image_filename in images_deleted:
            print(f"{slide_id} {image_filename}", file=f)


if __name__ == '__main__':
    main()
