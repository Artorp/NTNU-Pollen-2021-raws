import os
from typing import Tuple, List

import tqdm
from PIL import Image

import file_paths

# Stage 3:
# Convert the TIF images to JPEG images.

jpeg_compression_options = {
    "quality": 98,
    "subsampling": "4:4:4"
}


def main():
    convert_to_jpeg_jobs: List[Tuple[str, str]] = []
    for root_path, dirs, files in os.walk(file_paths.TIFs_directory):
        for file in files:
            if not file.endswith(".tif"):
                continue
            base_filename, ext = os.path.splitext(file)
            path_in_jpeg_dir = root_path.replace(file_paths.TIFs_directory, file_paths.JPEGs_directory)
            jpeg_output_filename = os.path.join(path_in_jpeg_dir, base_filename + ".jpg")
            convert_to_jpeg_jobs.append((os.path.join(root_path, file), jpeg_output_filename))

    for tif_filename, jpeg_filename in tqdm.tqdm(convert_to_jpeg_jobs):
        jpeg_save_directory, jpeg_base_filename = os.path.split(jpeg_filename)
        tif_image: Image.Image = Image.open(tif_filename)
        if not os.path.exists(jpeg_save_directory):
            os.makedirs(jpeg_save_directory)
        tif_image.save(jpeg_filename, **jpeg_compression_options)


if __name__ == '__main__':
    main()
