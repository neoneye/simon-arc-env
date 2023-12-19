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

Count the frequency of tiles. Similar to the single pixel histogram, do the same with small images with size `2x2`.

This is similar to [ngrams](https://en.wikipedia.org/wiki/N-gram).

Are the histograms almost identical with a few pixels off.
Sort the counters of both predicted histogram and expected histogram.
Measure the distance between the predicted and the expected.
This distance indicates how similar the two images are. If the distance is zero the histograms are identical.


### Raw pixel data

Example. This `4x3` image:
```
0, 1, 2, 3
4, 5, 6, 7
8, 9, 10, 11
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

tile 3
4, 5
8, 9

tile 4
5, 6
9, 10

tile 5
6, 7
10, 11
```

In the above case all the `2x2` tiles are unique.

When comparing with another image, that also have all unique `2x2` tiles, then both images share this uniqueness property.

### Normalize tile orientation

Normalize the rotation/flipping of the `2x2` tiles, so no matter what orientation the tile has, it will yield the same hash.

```
1, 0
0, 1
```

Same as
```
0, 1
1, 0
```

### Count tile unique/sameness

Two images may share the same structure, while using different colors. Reward when the structure is similar.

In order to only consider the structure and ignore the colors, this `unique/sameness` approach may help.

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

### Normalize tile color

Two images may share the same structure, while using different colors. Reward when the structure is similar.

In the case where the most popular color may differ between two images. 

Here the colors can be normalized, by putting the colors in different bins.
- Replace the most popular color gets with `A`. 
- Replace the medium/most popular color with `B`.
- Replace the medium popular color with `C`.
- Replace the medium/least popular color with `D`.
- Replace the least popular color with `E`.

```
5, 5, 5, 0
5, 0, 5, 0
5, 5, 5, 0
```

Doing the replacement and it becomes a normalized image like this

```
A, A, A, E
A, E, A, E
A, A, A, E
```

With the normalized image, apply the histogram comparisons described in this document.


## Histogram of NxM pixels

Small tile sizes: `1x1, 1x2, 1x3, 1x4, 1x5, 2x2, 2x3, 2x4, 2x5, 3x3, 3x4, 3x5, 4x4, 4x5, 5x5`.

Do the same kind of histogram with these tile sizes.


### Tile pattern complexity

If a tile use only one color, then it's low complexity.

If every pixel in the tile is unique, then it's maximum complexity.

Can this be expressed as a complexity value?


### Tile sequence analysis

Consider the sequence in which tiles appear in the image. 
This sequential analysis could reveal patterns or regularities that are not evident from individual tile analysis alone.


## Compare overall variance for direction

What is the average length of same colored pixels.

In [LODA-RUST](https://github.com/loda-lang/loda-rust) I measured variance over 3 adjacent pixels, and I'm describing it here.

| Direction               | Explanation                                         |
|-------------------------|-----------------------------------------------------|
| left - right            | How much does the pixels change along the x axis.   |
| top - bottom            | How much does the pixels change along the y axis.   |
| top left - bottom right | How much does the pixels change along `Diagonal A`. |
| top right - bottom left | How much does the pixels change along `Diagonal B`. |

Example: Horizontal stripes. has `left - right` variance: average is 3 and sigma is 0.
When considering 3 adjacent pixels the highest number of same colored pixels is 3.

```
horizontal stripes
5, 5, 5, 5
7, 7, 7, 7
9, 9, 9, 9
```

Example: diagonal stripe. Here the `top left - bottom right` variance. Average is 3 and sigma is 0.
When considering 3 adjacent pixels the highest number of same colored pixels is 3.

```
diagonal stripe
7, 0, 0, 0
0, 7, 0, 0
0, 0, 7, 0
0, 0, 0, 7
```

When comparing two images, if they have `sigma=0` for a direction, then it may be an indicator that 
the images shares same structure.


