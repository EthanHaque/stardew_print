"""Playing with colors."""

import random
from pathlib import Path

import numpy as np
from PIL import Image


def create_color_gradient(
    n: int,
    start_color: tuple[int, int, int] = (0, 0, 0),
    end_color: tuple[int, int, int] = (255, 255, 255),
):
    """Create an n x n array of tuples representing a color gradient."""
    gradient = []

    for i in range(n):
        row = []
        for j in range(n):
            r = start_color[0] + (end_color[0] - start_color[0]) * (i + j) / (
                2 * (n - 1)
            )
            g = start_color[1] + (end_color[1] - start_color[1]) * (i + j) / (
                2 * (n - 1)
            )
            b = start_color[2] + (end_color[2] - start_color[2]) * (i + j) / (
                2 * (n - 1)
            )
            row.append((int(r), int(g), int(b)))
        gradient.append(row)

    return np.array(gradient)


def create_test_file(
    output_path: Path,
    n: int = 5,
    start_color: tuple[int, int, int] = (0, 0, 0),
    end_color: tuple[int, int, int] = (255, 255, 255),
) -> Path:
    """Create a simple image file with a color gradient."""
    color_gradient = create_color_gradient(n, start_color, end_color)
    image = Image.fromarray(color_gradient)
    image.save(output_path)


def read_file(file_path: Path) -> np.ndarray:
    """Read a file that contains colors."""
    return np.array(Image.open(file_path))


def convert_color_array_to_string(color_array: np.ndarray) -> str:
    """Construct a string based on 24-bit TrueColor from a 2D list of colors."""
    string_representation = [
        [f"\033[48;2;{r};{g};{b};{a}m  \033[0m" for (r, g, b, a) in row]
        for row in color_array
    ]
    rows = ["".join(row) for row in string_representation]
    return "\n".join(rows)


def get_random_color() -> tuple[int, int, int]:
    """Create a random rgb color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def main():
    """Entry point."""
    test_file = Path("data/blue_chicken.png")
    color_info = read_file(test_file)
    height, width = color_info.shape[:2]

    rows, cols = 7, 4

    xpos = random.randint(0, rows - 1)
    ypos = random.randint(0, cols - 1)

    row_height = height // rows
    col_width = width // cols
    color_info = color_info[
        xpos * row_height : (xpos + 1) * row_height,
        ypos * col_width : (ypos + 1) * col_width,
    ]

    print(convert_color_array_to_string(color_info))


if __name__ == "__main__":
    main()
