import os
from typing import Tuple, List

import tqdm
from PIL import Image, ImageDraw, ImageFont

import file_paths

# Stage 5:
# The Annotations service Cloud Annotations (https://cloud.annotations.ai/) rescales
# images down to a max width of 1500px, or 1500x843px for Full HD images.
# To preserve the original file names, scale on our side before uploading directly to the bucket,
# the generated json files will then use the correct file names and the original file sizes
# can be used directly

# Due to Cloud Annotations not showing the file name, the image filename is also burned into the
# image. Note: This means that the generated images can not be used to train a model.

jpeg_compression_options = {
    "quality": 95,
    "subsampling": "4:4:4"
}


def main():
    scale_down_jobs: List[Tuple[str, str]] = []
    for root_path, dirs, files in os.walk(file_paths.JPEGs_directory):
        for file in files:
            if not file.endswith(".jpg"):
                continue
            jpeg_input_filename = os.path.join(root_path, file)
            path_in_small_jpeg_dir = root_path.replace(file_paths.JPEGs_directory, file_paths.JPEGs_small_directory)
            jpeg_output_filename = os.path.join(path_in_small_jpeg_dir, file)
            scale_down_jobs.append((jpeg_input_filename, jpeg_output_filename))

    font = ImageFont.truetype("fonts/arialbd.ttf", 14)
    for jpeg_filename, jpeg_output_filename in tqdm.tqdm(scale_down_jobs):
        jpeg_save_directory, jpeg_base_filename = os.path.split(jpeg_output_filename)
        jpeg_image: Image.Image = Image.open(jpeg_filename)
        if not os.path.exists(jpeg_save_directory):
            os.makedirs(jpeg_save_directory)
        resized_image = jpeg_image.resize((1500, 843))
        # burn in name of image so that it is visible in cloud.annotations.ai software
        # (these images should not be used for training)
        _, basename = os.path.split(jpeg_filename)
        draw = ImageDraw.Draw(resized_image)
        draw.text((4, 4), basename, fill="black", font=font, stroke_width=2, stroke_fill="white")
        resized_image.save(jpeg_output_filename, **jpeg_compression_options)
        resized_image.close()
        jpeg_image.close()


if __name__ == '__main__':
    main()
