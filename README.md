# Piano Fingering Suggester

Oct 2023 – present · Python · dynamic programming · optimization · AI-assisted

Most free sheet music has no fingering. The scores I learned piano from in Turkey were downloads, and most came without it, so for years I worked it out myself, piece by piece.

I started this program in October 2023. Give it a right-hand melody and it gives a finger for every note (1 = thumb, 5 = little finger).

## How it works

Choosing fingers is an optimization problem. Every key is a number (middle C = 60), and every hand movement from one finger to the next gets a cost:

- Two fingers too close or too far apart for that pair: one point per key.
- Thumb on a black key: one point.
- The same finger on a new note: five points.
- Thumb passing under fingers 2, 3 or 4, or them crossing over it: one or two points, plus one per key beyond four. Any other crossing: ten.

Dynamic programming finds the cheapest fingering for the whole melody without trying every combination: for each note and each finger, keep only the cheapest way to get there, then walk back from the end. For short melodies, a brute-force check tries every combination and agrees.

## Results

Matches standard fingering on scales and five-finger exercises. The arpeggio still comes out wrong.

| Melody | Suggested | Right? |
|---|---|---|
| C major scale up | 1 2 3 1 2 3 4 5 | Yes |
| C major scale down | 5 4 3 2 1 3 2 1 | Yes |
| G major scale up | 1 2 3 1 2 3 4 5 | Yes |
| Five-finger exercise | 1 2 3 4 5 4 3 2 1 | Yes |
| C major arpeggio | 1 3 1 2 | No: pianists play 1 2 3 5 |

## Next

- Fix the rules so the arpeggio comes out 1 2 3 5 without breaking the scales.
- Learn the costs with machine learning instead of setting them by hand.
- Add passages from pieces I play and compare with my own fingering.
- Researchers have worked on this since the 1990s, for example Parncutt et al. (1997).

## Run it

```
python3 fingering.py
```

The melodies are in `melodies.txt`, one per line.

---

Bora Marasli · Information Technology in Mechanical Engineering, TU Berlin · [LinkedIn](https://www.linkedin.com/in/boramarasli) · [More projects](https://github.com/boramarasli)
