"""Prints Stardew Valley sprites to the terminal using 24-bit TrueColor."""

import base64
import io
import json
import random
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image


def get_ansi_color_code(r, g, b, background=True):
    """Construct the ANSI escape code for a given RGB color.

    Parameters
    ----------
    r : int
        Red component (0-255).
    g : int
        Green component (0-255).
    b : int
        Blue component (0-255).
    background : bool, optional
        Whether to set as background color (default is True).

    Returns
    -------
    str
        ANSI escape code string.
    """
    set_as_background = 48
    set_as_foreground = 38
    mode = set_as_background if background else set_as_foreground
    return f"\033[{mode};2;{r};{g};{b}m"


def get_ansi_reset_style_code():
    """Get the ANSI escape code to reset terminal styles.

    Returns
    -------
    str
        ANSI reset escape code.
    """
    return "\033[0m"


def crop_to_content(color_array: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """
    Crops a 2D color array to the bounding box containing all non-zero content.

    Parameters
    ----------
    color_array : NDArray
        Array with shape (h, w, 4). Last dimension is rgba format.

    Returns
    -------
    NDArray
        Cropped array containing only the bounding box with non-zero content.
    """
    if color_array.shape[-1] != 4:
        msg = f"Expected last dimension of color_array to have size 4. Got {color_array.shape[-1]}"
        raise ValueError(msg)

    alpha_channel = color_array[..., 3]

    # Find the bounding box where alpha is non-zero
    rows = np.any(alpha_channel != 0, axis=1)
    cols = np.any(alpha_channel != 0, axis=0)

    # Get the indices of the bounding box
    row_start, row_end = np.where(rows)[0][[0, -1]]
    col_start, col_end = np.where(cols)[0][[0, -1]]

    return color_array[row_start : row_end + 1, col_start : col_end + 1]


def convert_2D_color_array_to_truecolor_string(
    color_array: NDArray[np.uint8],
) -> str:
    """Construct a string based on 24-bit TrueColor from a 2D array of rgba colors.

    Parameters
    ----------
    color_array : NDArray
        Array with shape (h, w, 4). Last dimension is rgba format.

    Returns
    -------
    str
        Singular string where each pixel in the original image has been converted
        to a 24-bit TrueColor printable substring and concatenated together.
    """
    visible_pixel_char = "  "
    invisible_pixel_char = "  "
    reset_code = get_ansi_reset_style_code()

    if color_array.shape[-1] != 4:
        msg = f"Expected last dimension of color_array to have size 4. Has size {color_array.shape[-1]}"
        raise ValueError(msg)

    string_representation = []
    for row in color_array:
        for pixel in row:
            r, g, b, a = pixel
            if a:
                pixel_color = get_ansi_color_code(r, g, b)
                # TODO: Don't always need the reset code. Can make strings smaller.
                next_char = f"{pixel_color}{visible_pixel_char}{reset_code}"
            else:
                next_char = invisible_pixel_char
            string_representation.append(next_char)

        string_representation.append("\n")

    string_representation += reset_code
    return "".join(string_representation)


def read_image(path: Path) -> NDArray[np.uint8]:
    """Read an image from the given path and converts it to an RGBA numpy array.

    Parameters
    ----------
    path : Path
        Path to the image file.

    Returns
    -------
    NDArray
        Image as a numpy array with shape (h, w, 4) in RGBA format.
    """
    image = Image.open(path)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    return np.array(image, dtype=np.uint8)


def read_base64_encoded_png(base_64_encoded_png: str) -> NDArray[np.uint8]:
    """Decode a base64 encoded png string into an image.

    Parameters
    ----------
    base_64_encoded_png : str
        PNG image that has been encoded in base64.

    Returns
    -------
    NDArray
        Array with shape (height, width, channels).
    """
    image_data = base64.b64decode(base_64_encoded_png)
    image = Image.open(io.BytesIO(image_data))
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    return np.array(image, dtype=np.uint8)


def main() -> None:
    """Entry point."""
    with Path("data/merged.json").open("r") as file:
        content = json.loads(file.read())
        random_sprite = random.choice(content)
        base64_encoded_sprite_png = random_sprite["image"]
        sprite_id = random_sprite["id"]
        sprite_name = random_sprite["names"]["data-en-US"]

    image_array = read_base64_encoded_png(base64_encoded_sprite_png)
    cropped_image_array = crop_to_content(image_array)
    colored_string = convert_2D_color_array_to_truecolor_string(cropped_image_array)

    print(f"{sprite_id}: {sprite_name}\n")
    print(colored_string)


if __name__ == "__main__":
    main()
