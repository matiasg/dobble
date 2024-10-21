import logging
import math
from argparse import ArgumentParser
from hashlib import sha1
from itertools import count
from pathlib import Path
from typing import Iterator

from svgelements import SVG, Circle, Matrix, Point

from generate import generate_cards

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def positions_generator(
    N: int, sizes: float, end_size: float
) -> Iterator[tuple[float, float]]:
    theta = math.cos(2 * math.pi / N) + 1j * math.sin(2 * math.pi / N)
    for i in range(N):
        pos = theta**i * 0.6 * end_size
        x = pos.real
        y = pos.imag
        yield (x + end_size, y + end_size)


def rotations_list(svgs: list[SVG]) -> list[float]:
    return [2 * math.pi * sha1(repr(svg).encode()).digest()[0] / 256 for svg in svgs]


def make_card(svgs, indices, end_size=300.0) -> SVG:
    out_svg = SVG(width=2 * end_size, height=2 * end_size)
    N = len(indices)
    sizes = end_size / math.sqrt(N)
    rotations = rotations_list(svgs)
    for (
        i,
        idx,
        (x, y),
    ) in zip(count(), indices, positions_generator(N, sizes, end_size)):
        svg_file, svg = svgs[idx]
        rotation = rotations[idx]
        logger.info(
            "  using %s for card at pos %d: (x,y)=(%.3f, %.3f)", svg_file, i, x, y
        )
        size = max(svg.width, svg.height)
        for e in svg.elements():
            out_svg.append(
                e
                * Matrix.translate(-svg.width / 2, -svg.height / 2)
                * Matrix.scale(sizes / size)
                * Matrix.rotate(rotation)
                * Matrix.translate(x, y)
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
    assert len(svgs) >= symbols, f"need at least {symbols} svgs but got {len(svgs)}"
    for i, card in enumerate(generate_cards(order)):
        logger.info("doing card %d", i)
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
