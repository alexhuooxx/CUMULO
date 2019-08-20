import numpy as np
import os
import sys

from PIL import Image

from interpolation import fill_all_channels, contain_invalid
from modis_level1 import get_swath_rgb

def save_swath_rbgs(radiance_filepath, save_dir, verbose=1):
    """
    :param radiance_filepath: the filepath of the radiance (MOD02) input file
    :param save_dir:
    :param verbose: verbosity switch: 0 - silent, 1 - verbose, 2 - partial, only prints confirmation at end
    :return: none
    Generate and save RBG channels of the given MODIS file. Expects to find a corresponding MOD03 file in the same directory. Comments throughout
    """

    basename = os.path.basename(radiance_filepath)

    # creating the save subdirectory
    save_dir = os.path.join(save_dir, "visual")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    visual_swath = get_swath_rgb(radiance_filepath)

    #interpolate to remove NaN artefacts
    fill_all_channels(visual_swath)

    pil_loaded_visual_swath = Image.fromarray(visual_swath.transpose(1, 2, 0).astype(np.uint8), mode="RGB")

    save_filename = os.path.join(save_dir, basename.replace(".hdf", ".png"))
    pil_loaded_visual_swath.save(save_filename)

    if verbose:
        print("swath {} processed".format(tail))


# Hook for pipe in
if __name__ == "__main__":
    target_filepath = sys.argv[1]
    save_swath_rbgs(target_filepath, save_dir="..DATA/aqua-data-processed/RGB/", verbose=1)
