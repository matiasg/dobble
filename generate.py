import galois


def p2f_index(gf, x, y) -> int:
    order = gf.order
    if y is None:
        ix = int(x) if x is not None else order
        return order**2 + ix
    return int(x) + order * int(y)


def generate_cards(gf):
    """ugly first version of cards generator.
    TODO:
        - typing
        - nice symbols
    """
    order = gf.order
    for a in range(order):
        agf = gf(a)
        for b in range(order):
            bgf = gf(b)
            cards = [p2f_index(gf, x := gf(i), agf * x + bgf) for i in range(order)]
            cards.append(p2f_index(gf, a, None))
            yield cards
        cards = [p2f_index(gf, a, gf(i)) for i in range(order)]
        cards.append(p2f_index(gf, None, None))
        yield cards
    cards = [p2f_index(gf, gf(i), None) for i in range(order)]
    cards.append(p2f_index(gf, None, None))
    yield cards


def print_cards(gf):
    for cards in generate_cards(gf):
        print(f"{cards}")


order = 2
GF = galois.GF(order)
print_cards(GF)
