# Dobble

A python script that produces [dobble](https://en.wikipedia.org/wiki/Dobble) sets of cards.

As explained in the the Wikipedia page, the drawings in a set of `dobble` are points in $\mathbf{P^2}(\mathbb{F}_q)$,
the projective plane of the Galois field $\mathbb{F}_q$.
The external links there explain pretty well how this works, so I'm not going to explain it here.
(see
[here](https://www.youtube.com/watch?v=VTDKqW_GLkw),
[here](https://www.petercollingridge.co.uk/blog/mathematics-toys-and-games/dobble/) or
[here](https://puzzlewocky.com/games/the-math-of-spot-it/)).
Suffice it to say that $q$ is the power of a prime (either a prime, a prime squared, a prime cube, etc).
Then there can be up to $q^2 + q + 1$ cards, each with $q + 1$ drawings. The number of drawings is
$q^2 + q + 1$.

For instance, the version for sale is made with $q=7$. This gives 57 drawings and 57 cards.
But typically, they sell the game with 55 cards, because, well, maybe they know why, because I don't.

If you take $q=2$, the smallest example, you are left with 7 cards with 7 drawings. This is known as the Fano Plane.

The current script just produces cards for any $q$:

```sh
$ python generate.py 2
['😀', '😁', '😄']
['😂', '😃', '😄']
['😀', '😂', '😆']
['😀', '😃', '😅']
['😂', '😁', '😅']
['😁', '😃', '😆']
['😄', '😅', '😆']
```

Also, `draw.py` generates cards from a directory with svg files (still rough cards)
```sh
$ python draw.py 2 svgs --outdir cards
```
takes at least 7 svg inside the `svgs` dir and outputs round cards in the `cards` directory.
