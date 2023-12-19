# Draft: image compare

This is an idea. It's not implemented. I'm considering adding this. Proposed by `neo` on lab42 discord.

A good diff algorithm is needed in order to train a RL, if it gets very close to the target, then reward high, if it’s wrong then no reward.

In order to reward good predictions, it may be useful with an algorithm that determines how close is the predicted image from the target image.

If it could explain why the two images are different, that could be useful.

For text there is [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

For images I'm not aware of a good algorithm. So here are some rough ideas.

## Histogram of pixels

Are the histograms identical, same colors, same counters. This may mean that the pixels are present, but some pixels may be misplaced.

Are all only the colors identical.

Are all only the counters identical.

Are the histograms almost identical with a few pixels off.
Sort the counters of both predicted histogram and expected histogram.
Measure the distance between the predicted and the expected.
This distance indicates how similar the two images are. If the distance is zero the histograms are identical.


## Histogram of 2x2 pixels

Similar to the single pixel histogram, do the same with small images with size `2x2`.

This is similar to [ngrams](https://en.wikipedia.org/wiki/N-gram).

Are the histograms almost identical with a few pixels off.
Sort the counters of both predicted histogram and expected histogram.
Measure the distance between the predicted and the expected.
This distance indicates how similar the two images are. If the distance is zero the histograms are identical.


### Raw pixel data

Example. This `3x4` image:
```
0, 1, 2, 3,
4, 5, 6, 7,
8, 9, 10, 11,
```

Can be split it into these `2x2` tiles:
```
tile 0
0, 1
4, 5

tile 1
1, 2
5, 6

tile 2
2, 3
6, 7

tile 4
4, 5
8, 9

tile 5
5, 6
9, 10

tile 6
6, 7
10, 11
```

In the above case all the `2x2` tiles are unique.

When comparing with another image, that also have all unique `2x2` tiles, then there is some similarity.

### Normalize

Normalise the rotation/flipping of the `2x2` tiles, so no matter what orientation the tile has, it will yield the same hash.

```
1, 0
0, 1
```

Same as
```
0, 1
1, 0
```

### Count unique/sameness

```
counter: 1 1 1 1, unique
0, 1
2, 3

counter: 2 1 1, two identical, 1 unique + 1 unique
0, 0
1, 2

counter: 2 2, two identical + two identical
0, 0
1, 1

counter: 3 1
0, 0
0, 1

counter: 4, all the same
0, 0
0, 0
```




## Histogram of NxM pixels

Small tile sizes: `1x1, 1x2, 1x3, 1x4, 1x5, 2x2, 2x3, 2x4, 2x5, 3x3, 3x4, 3x5, 4x4, 4x5, 5x5`.

Do the same kind of histogram with these tile sizes.
