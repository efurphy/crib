from crib import *

def run():
  # each score_hand test is a list in the form [list: hand, int: expected score]
  score_tests = [
    [
      [Card("A", "spades"), Card("2", "hearts"), Card("2", "clubs"), Card("3", "hearts"), Card("8", "spades")],
      10
    ],
    [
      [Card("7", "spades"), Card("7", "hearts"), Card("8", "clubs"), Card("9", "hearts"), Card("10", "clubs")],
      14
    ],
    [
      [Card("9", "clubs"), Card("10", "clubs"), Card("J", "clubs"), Card("Q", "clubs"), Card("K", "clubs")],
      11
    ],
    [
      [Card("2", "spades"), Card("2", "hearts"), Card("5", "clubs"), Card("3", "hearts"), Card("9", "spades")],
      2
    ],
    [
      [Card("2", "spades"), Card("5", "hearts"), Card("6", "clubs"), Card("K", "hearts"), Card("3", "spades")],
      4
    ],
    [
      [Card("3", "spades"), Card("2", "hearts"), Card("2", "clubs"), Card("A", "hearts"), Card("2", "spades")],
      15
    ],
    [
      [Card("A", "hearts"), Card("2", "hearts"), Card("6", "hearts"), Card("Q", "hearts"), Card("K", "spades")],
      4
    ],
    [
      [Card("A", "hearts"), Card("2", "hearts"), Card("6", "hearts"), Card("Q", "clubs"), Card("K", "hearts")],
      0
    ],
    [
      [Card("A", "hearts"), Card("A", "hearts"), Card("A", "hearts"), Card("2", "clubs"), Card("3", "hearts")],
      15
    ],
    [
      [Card("J", "hearts"), Card("5", "diamonds"), Card("5", "clubs"), Card("5", "spades"), Card("5", "hearts")],
      29
    ],
    [
      [Card("Q", "hearts"), Card("4", "clubs"), Card("A", "clubs"), Card("A", "spades"), Card("5", "hearts")],
      8
    ],
    [
      [Card("K", "clubs"), Card("5", "hearts"), Card("4", "clubs"), Card("4", "spades"), Card("6", "hearts")],
      14
    ],
    [
      [Card("K", "clubs"), Card("5", "hearts"), Card("4", "clubs"), Card("4", "spades"), Card("6", "hearts")],
      14
    ],
    [
      [Card("9", "clubs"), Card("6", "hearts"), Card("7", "clubs"), Card("8", "spades"), Card("A", "hearts")],
      10
    ],
    [
      [Card("5", "clubs"), Card("6", "hearts"), Card("7", "clubs"), Card("2", "spades"), Card("A", "hearts")],
      7
    ],
    [
      [Card("6", "clubs"), Card("6", "hearts"), Card("6", "diamonds"), Card("6", "spades"), Card("9", "hearts")],
      20
    ],
    [
      [Card("4", "clubs"), Card("5", "hearts"), Card("5", "clubs"), Card("6", "spades"), Card("10", "hearts")],
      16
    ],
    [
      [Card("6", "clubs"), Card("6", "hearts"), Card("7", "clubs"), Card("7", "spades"), Card("8", "hearts")],
      20
    ],
    [
      [Card("J", "clubs"), Card("Q", "hearts"), Card("K", "clubs"), Card("Q", "spades"), Card("5", "hearts")],
      16
    ],
    [
      [Card("5", "clubs"), Card("5", "hearts"), Card("5", "clubs"), Card("4", "spades"), Card("6", "hearts")],
      23
    ],
    [
      [Card("A", "clubs"), Card("9", "hearts"), Card("3", "clubs"), Card("2", "spades"), Card("A", "hearts")],
      12
    ],
    [
      [Card("J", "hearts"), Card("10", "hearts"), Card("9", "hearts"), Card("J", "hearts"), Card("10", "hearts")],
      22
    ],
    [
      [Card("K", "hearts"), Card("J", "hearts"), Card("9", "hearts"), Card("8", "hearts"), Card("8", "diamonds")],
      6
    ],
  ]

  fails = []

  for i,t in enumerate(score_tests):
    score = score_hand(t[0][:-1], t[0][-1])
    expected = t[1]

    if score != expected:
      print(f"test {i+1}: ", end="")
      print(f"expected {expected} got {score}")
      fails.append(i)

  debug = False

  for f in fails:
    print(f"test {f+1}:")
    t = score_tests[f]
    display_cards(t[0])
    score_hand(t[0][:-1], t[0][-1], explain=debug, debug=debug)

  print()
  print(f"testing complete ({len(fails)} failed)")
  exit()