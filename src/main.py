"""Playing with colors."""

from pathlib import Path


def create_color_gradient(
    n: int,
    start_color: tuple[int, int, int] = (0, 0, 0),
    end_color: tuple[int, int, int] = (255, 255, 255),
):
    """Create an n x n array of tuples representing a color gradient.

    Parameters
    ----------
    n : int
        Size of the grid (n x n).
    start_color : tuple of int, optional
        RGB tuple for the starting color (default is (0, 0, 0)).
    end_color : tuple of int, optional
        RGB tuple for the ending color (default is (255, 255, 255)).

    Returns
    -------
    list of list of tuple
        A nested list of shape (n, n) containing RGB tuples.
    """
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
):
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


def read_file(input_path: Path):
    """Read a file that contains colors."""
    with input_path.open("r") as file:
        out = []
        for line in file:
            curr_row = []
            rgb_triplets = line.strip().split(", ")
            for triplet in rgb_triplets:
                r, g, b = triplet.lstrip("(").rstrip(")").split(",")
                curr_row.append((int(r), int(g), int(b)))
            out.append(curr_row)
        return out


def print_color_gradient(gradient):
    """
    Print the color gradient as colored squares to the terminal.

    Parameters
    ----------
    gradient : list of list of tuple
        The gradient to print, where each tuple represents an RGB color.
    """
    for row in gradient:
        for color in row:
            r, g, b = color
            print(f"\033[48;2;{r};{g};{b}m  \033[0m", end="")
        print()


def main():
    """Entry point."""
    test_file = Path("data/test")
    create_test_file(
        test_file, n=10, start_color=(100, 20, 30), end_color=(200, 230, 180)
    )
    print_color_gradient(read_file(test_file))


if __name__ == "__main__":
    main()
