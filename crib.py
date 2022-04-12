import math
import random
import itertools
import sys
import crib_test
import re

class Deck:
  def __init__(self):
    self.cards = []

    # a list of cards that have been drawn, and therefore aren't in
    self.drawn_cards = []

    for i in range(52):
      rank = Card.ranks[i % len(Card.ranks)]
      suit = Card.suits[i // len(Card.ranks)]
      self.cards.append(Card(rank, suit))

  # draw a card. draws "face up" meaning the drawn card will be added to the end of the drawn_cards list. the end of the list represents the "bottom" of the deck of drawn cards, if the deck is arranged face down.
  def draw_card(self, i):
    card = self.cards.pop(i)
    self.drawn_cards.append(card)
    return card

  def draw_top_card(self):
    return self.draw_card(0)

  def draw_random_card(self):
    return self.draw_card(random.randint(0, len(self.cards) - 1))

  # put all the drawn cards back onto the top of the deck
  def collect(self):
    self.cards = self.drawn_cards + self.cards
    self.drawn_cards.clear()

  # shuffle the deck
  def shuffle(self):
    random.shuffle(self.cards)

  # deal a number of hands, each with a number of cards.
  # returns a list of lists of cards
  def deal_hands(self, n_hands, n_cards):
    hands = [[] for i in range(n_hands)]

    for i in range(n_cards):
      for hand in hands:
        hand.append(self.draw_top_card())

    return hands

  def __str__(self):
    s = str(len(self.cards)) + " cards: "
    for i in range(len(self.cards)):
      s += str(self.cards[i])
      if i != len(self.cards) - 1:
        s += ", "
    return s

class Card:
  ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
  suits = ["clubs", "hearts", "spades", "diamonds"]
  rank_words = {"A": "ace", "J": "jack", "Q": "queen", "K": "king"}
  rank_values = {"A": 1, "J": 10, "Q": 10, "K": 10}

  u_suits = {
    "clubs": "♣",
    "hearts": "♥",
    "spades": "♠",
    "diamonds": "♦",
  }

  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
    self.value = Card.rank_values[rank] if rank in Card.rank_values else int(rank)

  def __repr__(self):
    s = ""
    if self.rank in Card.rank_words:
      s += Card.rank_words[self.rank].capitalize()
    else:
      s += self.rank
    s += " of "
    s += self.suit.capitalize()
    return s

# display up to 5 text representations of cards onto the terminal.
def display_cards(cards):
  if type(cards) != list:
    cards = [cards]

  if len(cards) == 0:
    print("No cards.")
    return

  for i in range(5):
    for j,card in enumerate(cards):
      #print(card.rank + card.suit[0].upper(), end=" ")

      if i == 0 or i == 4:
        print(" ", end="")
        print("-" * 5, end="")
        print(" ", end="")
      elif i == 1:
        print("|", end="")
        print(card.rank + " " * (5 - len(card.rank)), end="")
        print("|", end="")
      elif i == 2:
        suit = card.suit[0].upper()
        #suit = Card.u_suits[card.suit]

        print("|", end="")
        print("  " + suit + "  ", end="")
        print("|", end="")
      elif i == 3:
        print("|", end="")
        print(" " * (5 - len(card.rank)) + card.rank, end="")
        print("|", end="")

      if j != 5:
        print(" ", end="")

    print()

# score a hand by the rules of cribbage.
# takes a list of 4 cards representing a hand, and a single card representing a cut. returns the total score of the hand.
def score_hand(hand, cut, explain=False, debug=False):
  if len(hand) != 4:
    raise ValueError

  def dprint(s):
    if not debug:
      return
    print(s)

  score = 0

  # the total hand to count the score of is the given hand plus the cut
  total_hand = hand + [cut]

  # get a list of all possible combinations of the total hand (w/o replacement), call these subhands.
  subhands = []
  for i in range(2, len(total_hand) + 1):
    combins = list(itertools.combinations(total_hand, i))
    subhands += combins

  # get the sums of each subhand's card values. if a sum is 15, add 2 to the score.
  for subhand in subhands:
    subhand_score = 0

    for card in subhand:
      subhand_score += card.value

    if subhand_score == 15:
      score += 2

      if explain:
        print("fifteen")

  # if all four of the hand's cards are the same suit, add four points. if the cut is also the same suit, add another point.
  same_suit = True

  for i in range(1, len(hand)):
    if hand[i].suit == hand[i - 1].suit:
      continue

    same_suit = False
    break

  if same_suit:
    score += 4
    if explain:
      print("suits", end="")

    if hand[0].suit == cut.suit:
      score += 1
      if explain:
        print("+cut")
    elif explain:
        print()

  # look for pairs in the total hand, adding 2 to the score for each.
  for i in range(len(total_hand)):
    for j in range(i+1, len(total_hand)):
      if total_hand[i].rank == total_hand[j].rank:
        score += 2

        if explain:
          print("pair")

  # check for runs, meaning sequences of 3 or more cards whose ranks are in order. e.g. a 2, 3, and 4 (of any suits) gives 3 points.
  hand_range = []

  for card in total_hand:
    ind = Card.ranks.index(card.rank) + 1
    hand_range.append(ind)

  #dprint(hand_range)

  run = hand_range.copy()

  run.sort()

  dprint(run)

  potential_runs = []

  for i in range(3, len(run)+1):
    combins = list(itertools.combinations(run, i))

    for c in combins:
      s = sorted(list(set(c)))
      newc = list(c)

      dprint(s)

      if len(s) > 2 and s == newc:
        if max(s) - min(s) + 1 == len(s):
          potential_runs.append(set(s))

  dprint(potential_runs)

  if len(potential_runs) > 0:
    max_len = max(potential_runs, key=lambda x: len(x))

    dprint(max_len)

    for i,r in enumerate(potential_runs):
      if len(r) < len(max_len) and r.issubset(max_len):
        potential_runs[i] = set()

    dprint(potential_runs)

  for r in potential_runs:
    score += len(r)

    if explain:
      print("run", r)

  # if the hand has a jack with the same suit as the cut, add one point
  jacks = []

  for card in hand:
    if card.rank == "J":
      jacks.append(card.suit)

  for j in jacks:
    if j == cut.suit:
      score += 1

      if explain:
        print("jack")

      break

  # return the final score
  return score

# select a card or cards from a list of cards. text should be a string in the form "AS 7D" for example, which would try to find the Ace of Spades and 7 of Diamonds in the list of cards.
# returns a new list of cards from 'cards' that were specified by 'text'
def select_cards(text, cards):
  text = text.split()

  pattern = r"^([2-9]|10|[AJQKajqk])([CHSDchsd])$"

  text_reprs = []

  for s in text:
    match = re.search(pattern, s)

    if not match:
      raise ValueError

    text_reprs.append(match.string.upper())

  cards_reprs = []

  for c in cards:
    cards_reprs.append(c.rank + c.suit[0].upper())

  result = []

  for t in text_reprs:
    if t in cards_reprs:
      result.append(cards[cards_reprs.index(t)])

  return result

if __name__ == "__main__":
  # test the program if "test" is given as a command line argument
  if len(sys.argv) > 1 and sys.argv[1] == "test":
    crib_test.run()

  '''
  cards = [Card("9", "clubs"), Card("10", "clubs"), Card("J", "clubs"), Card("Q", "clubs"), Card("K", "hearts")]

  while True:
    display_cards(cards)

    text = input()

    selected = select_cards(text, cards)

    #print(selected)
    display_cards(selected)
  '''

  # setup a standard deck of cards
  deck = Deck()

  # when a player reaches this score, they win the game
  max_score = 100

  # start two players off at scores of 0
  p1_score = 0
  p2_score = 0

  # the first crib starts with a randomly selected player 
  crib_turn = random.randint(1,2)

  while p1_score < max_score and p2_score < max_score:
    print("new turn")
    print("scores: " + str(p1_score) + ", " + str(p2_score))
    print()

    # shuffle the deck
    deck.shuffle()

    # deal each player a hand of 6 cards
    p1_hand, p2_hand = deck.deal_hands(2, 6)

    # the crib is selected from the top two cards from each player's hand
    crib = [p1_hand.pop(0) for i in range(2)] + [p2_hand.pop(0) for i in range(2)]

    # the cut is a randomly drawn card from the deck
    cut = deck.draw_random_card()

    # score each hand and the crib, displaying all cards and their scores
    p1_hand_score = score_hand(p1_hand, cut)
    p2_hand_score = score_hand(p2_hand, cut)
    crib_score = score_hand(crib, cut)

    print("cut:")
    display_cards(cut)
    print()

    print(f"player 1 hand ({p1_hand_score}):")
    display_cards(p1_hand)
    print()

    print(f"player 2 hand ({p2_hand_score}):")
    display_cards(p2_hand)
    print()

    print(f"player {crib_turn} crib ({crib_score}):")
    display_cards(crib)
    print()

    p1_score += p1_hand_score
    p2_score += p2_hand_score

    if crib_turn == 1:
      p1_score += crib_score
    else:
      p2_score += crib_score

    # collect all drawn cards back into the deck
    deck.collect()

    print("turn end")
    print("scores: " + str(p1_score) + ", " + str(p2_score))
    print()

    crib_turn = 1 if crib_turn == 2 else 2

    input("press enter to continue: ")
    print()

  if p1_score > p2_score:
    print("player 1 wins")
  else:
    print("player 2 wins")