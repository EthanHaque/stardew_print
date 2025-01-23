"""Prints Stardew Valley sprites to the terminal using 24-bit TrueColor."""

import base64
import io
import json
import random
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image


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
    if color_array.shape[-1] != 4:
        msg = f"Expected last dimension of color_array to have size 4. Has size {color_array.shape[-1]}"
        raise ValueError(msg)

    string_representation = [
        [f"\033[48;2;{r};{g};{b};{a}m  \033[0m" for (r, g, b, a) in row]
        for row in color_array
    ]
    rows = ["".join(row) for row in string_representation]
    return "\n".join(rows)


def read_base64_encoded_png(base_64_encoded_png: str) -> NDArray[np.uint8]:
    """Decode a base64 encoded png string into an image.

    Parameters
    ----------
    base_64_encoded_png : str
        PNG image that has been encoded in base64.

    Returns
    -------
    NDArray
        Array with shape (h, w, c) where c is the number of channels in the image.
    """
    image_data = base64.b64decode(base_64_encoded_png)
    img = Image.open(io.BytesIO(image_data))
    return np.array(img)


def main() -> None:
    """Entry point."""
    with Path("data/merged.json").open("r") as file:
        content = json.loads(file.read())
        random_sprite = random.choice(content)
        base64_encoded_sprite_png = random_sprite["image"]
        sprite_id = random_sprite["id"]
        sprite_name = random_sprite["names"]["data-en-US"]

    print(f"{sprite_id}: {sprite_name}")
    print(
        convert_2D_color_array_to_truecolor_string(
            read_base64_encoded_png(base64_encoded_sprite_png)
        )
    )


if __name__ == "__main__":
    main()
