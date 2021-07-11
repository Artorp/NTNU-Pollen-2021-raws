import os

import file_paths

# Stage 1:
# Move TIFs from "CZIs" directory to empty "TIFs" directory

# All images in the dataset is originally stored as CZI file format.
# They are then batch exported using the Zen (blue edition) software to 24bit (8bit per channel) RGB TIF image files,
# and the TIF image files are stored in the same location as the original CZI file.

# Naming scheme:
# A CZI file named "Snap-656.czi" is exported to "Snap-656-Image Export-01_ORG.tif",
# when moving, the folder structure should be retained, and the output file name
# should be the same as input except for the extension


def main():
    czi_dir = file_paths.CZIs_directory
    tif_dir = file_paths.TIFs_directory
    for path, dirs, files in os.walk(czi_dir):
        for file in files:
            if not file.endswith(".tif"):
                continue
            root, ext = os.path.splitext(file)
            # root = Snap-656-Image Export-01_ORG, ext = ".tif"
            a, _ = root.split("-Image Export-", 1)
            # print(a)
            path_in_tif_dir = path.replace(czi_dir, tif_dir)
            renamed_path = os.path.join(path_in_tif_dir, a + ext)
            print(renamed_path)
            if not os.path.exists(path_in_tif_dir):
                os.makedirs(path_in_tif_dir, exist_ok=False)
            os.rename(os.path.join(path, file), renamed_path)


if __name__ == '__main__':
    main()
