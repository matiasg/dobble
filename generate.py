import galois


def generate_cards(gf):
    """ugly first version of cards generator.
    TODO:
        - typing
        - infinity points
        - nice symbols
    """
    order = gf.order
    for a in range(order):
        for b in range(order):
            agf = gf(a)
            bgf = gf(b)
            cards = [int(agf * gf(x) + bgf) for x in range(gf.order)]
            print(f"card ({a},{b}) --> {cards}")


order = 7
GF = galois.GF(order)
generate_cards(GF)
