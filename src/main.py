"""Playing with colors."""

import random
from pathlib import Path


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

    return gradient


def create_test_file(
    output_path: Path,
    n: int = 5,
    start_color: tuple[int, int, int] = (0, 0, 0),
    end_color: tuple[int, int, int] = (255, 255, 255),
) -> Path:
    """Create a simple image file with a color gradient."""
    color_gradient = create_color_gradient(n, start_color, end_color)
    with output_path.open("w") as file:
        for row in color_gradient:
            out = ""
            for tup in row:
                r, g, b = tup
                out += f"({r},{g},{b}), "
            out = out[:-2] + "\n"
            file.write(out)
    return output_path


def read_file(file_path: Path):
    """Read a file that contains colors."""
    with file_path.open("r") as file:
        out = []
        for line in file:
            curr_row = []
            rgb_triplets = line.strip().split(", ")
            for triplet in rgb_triplets:
                r, g, b = triplet.lstrip("(").rstrip(")").split(",")
                curr_row.append((int(r), int(g), int(b)))
            out.append(curr_row)
        return out


def convert_color_array_to_string(color_array: list[list[tuple[int, int, int]]]) -> str:
    """Construct a string based on 24-bit TrueColor from a 2D list of colors."""
    string_representation = [
        [f"\033[48;2;{r};{g};{b}m  \033[0m" for (r, g, b) in row] for row in color_array
    ]
    rows = ["".join(row) for row in string_representation]
    return "\n".join(rows)


def get_random_color() -> tuple[int, int, int]:
    """Create a random rgb color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def main():
    """Entry point."""
    test_file = Path("data/test")
    color_1 = get_random_color()
    color_2 = get_random_color()
    create_test_file(test_file, n=15, start_color=color_1, end_color=color_2)

    color_info = read_file(test_file)
    print(convert_color_array_to_string(color_info))


if __name__ == "__main__":
    main()
