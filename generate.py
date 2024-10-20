from argparse import ArgumentParser

import galois
from galois._fields._meta import FieldArrayMeta


def default_graph(i):
    e0 = 0x1F600
    return chr(e0 + i)


def p2f_index(
    x: galois.FieldArray | None, y: galois.FieldArray | None, gf: FieldArrayMeta
) -> int:
    """`x` and `y` must be elements of the same Galois Field `gf` or None.
    If `x` is None, then `y` must be None as well.
    """
    assert gf is not None
    order = gf.order
    if y is None:
        ix = int(x) if x is not None else order
        return order**2 + ix
    assert x is not None, f"x is None but y == {y} != None"
    return int(x) + order * int(y)


def generate_cards(order: int):
    """
    Generates cards over with `order + 1` symbols each
    """
    gf = galois.GF(order)
    for a in range(order):
        agf = gf(a)
        for b in range(order):
            bgf = gf(b)
            cards = [p2f_index(x := gf(i), agf * x + bgf, gf) for i in range(order)]
            cards.append(p2f_index(gf(a), None, gf))
            yield cards
        cards = [p2f_index(gf(a), gf(i), gf) for i in range(order)]
        cards.append(p2f_index(None, None, gf))
        yield cards
    cards = [p2f_index(gf(i), None, gf) for i in range(order)]
    cards.append(p2f_index(None, None, gf))
    yield cards


def print_cards(order: int):
    for cards in generate_cards(order):
        graphs = [default_graph(i) for i in cards]
        print(f"{graphs}")


def main(args):
    print_cards(args.order)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "order",
        type=int,
        help="order of the Galois field, which is 1 less than the number of drawing in each card",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
