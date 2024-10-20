import math
from argparse import ArgumentParser
from pathlib import Path

from svgelements import SVG, Circle, Matrix, Point

from generate import generate_cards


def make_card(svgs, indices, end_size=300.0):
    out_svg = SVG(width=2 * end_size, height=2 * end_size)
    N = len(indices)
    theta = math.cos(2 * math.pi / N) + 1j * math.sin(2 * math.pi / N)
    for i, idx in enumerate(indices):
        svg_file, svg = svgs[idx]
        print(f"  using {svg_file} for card at pos {i}")
        x = (theta**i).real
        y = (theta**i).imag
        size = max(svg.width, svg.height)
        for e in svg.elements():
            out_svg.append(
                e
                * Matrix.scale(end_size / size / N)
                * Matrix.translate(
                    end_size * (x * 0.8 + 1 - 1 / N / 2),
                    end_size * (y * 0.8 + 1 - 1 / N / 2),
                )
            )
    out_svg.append(
        Circle(
            center=Point(end_size, end_size),
            r=end_size,
            stroke="#000",
            stroke_width=5,
            fill="#fff",
            fill_opacity=0.2,
        )
    )
    return out_svg


def make_cards(svgs: list[tuple[Path, SVG]], order: int, outdir: Path):
    symbols = order**2 + order + 1
    assert len(svgs) >= symbols, f"need at least {symbols} but got {len(svgs)}"
    for i, card in enumerate(generate_cards(order)):
        print(f"doing card {i}")
        svg = make_card(svgs, card)
        svg.write_xml(outdir / f"card_{i}.svg")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "order",
        type=int,
        help="order of the Galois field, which is 1 less than the number of drawing in each card",
    )
    parser.add_argument("svgs", type=Path, help="directory with svg files to use")
    parser.add_argument(
        "--outdir", type=Path, default="tmp", help="directory where to dump cards to"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    svg_files = args.svgs.glob("*.svg")
    svgs = [(file, SVG.parse(file)) for file in svg_files]
    args.outdir.mkdir(exist_ok=True)
    make_cards(svgs, args.order, outdir=args.outdir)
