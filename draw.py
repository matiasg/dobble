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
    N: int, sizes: list[float], card_size: float, scale_margin: float = 0.8
) -> Iterator[tuple[float, float]]:
    theta = math.cos(2 * math.pi / N) + 1j * math.sin(2 * math.pi / N)
    for i, size in zip(count(), sizes):
        pos = theta**i * scale_margin * (card_size - size / 2.0)
        yield (pos.real + card_size, pos.imag + card_size)


def sizes_list(svgs: list[tuple[Path, SVG]], card_size: float, N: int) -> list[float]:
    hash_sizes = [0.5 + sha1(repr(svg).encode()).digest()[0] / 256 for _, svg in svgs]
    return [s * card_size / math.sqrt(N) for s in hash_sizes]


def rotations_list(svgs: list[tuple[Path, SVG]]) -> list[float]:
    return [2 * math.pi * sha1(repr(svg).encode()).digest()[0] / 256 for _, svg in svgs]


def make_card(
    svgs: list[tuple[Path, SVG]],
    indices: list[int],
    card_size: float = 300.0,
    margins: float = 40.0,
    stroke_width: float = 5.0,
) -> SVG:
    total_size = 2 * card_size + margins + stroke_width
    out_svg = SVG(width=total_size, height=total_size)
    N = len(indices)
    sizes = sizes_list(svgs, card_size, N)
    logger.info("sizes: %s", sizes)
    rotations = rotations_list(svgs)
    for i, idx, (x, y) in zip(
        count(), indices, positions_generator(N, sizes, card_size)
    ):
        svg_file, svg = svgs[idx]
        rotation = rotations[idx]
        symbol_size = sizes[idx]
        logger.info(
            "  using %s for card at pos %d: (x,y)=(%.3f, %.3f)", svg_file, i, x, y
        )
        original_size = max(svg.width, svg.height)
        for e in svg.elements():
            out_svg.append(
                e
                * Matrix.translate(-svg.width / 2, -svg.height / 2)
                * Matrix.scale(symbol_size / original_size)
                * Matrix.rotate(rotation)
                * Matrix.translate(x + margins, y + margins)
            )
    out_svg.append(
        Circle(
            center=Point(card_size + margins, card_size + margins),
            r=card_size,
            stroke="#000",
            stroke_width=stroke_width,
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
