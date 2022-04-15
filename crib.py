import math
import random
import itertools
import sys
import re
import traceback # for debugging

class Deck:
  def __init__(self):
    self.cards = []

    # a list of cards that have been drawn, and therefore aren't currently in the deck
    self.drawn_cards = []

    # create 52 unique cards
    for i in range(52):
      rank = Card.ranks[i % len(Card.ranks)]
      suit = Card.suits[i // len(Card.ranks)]
      self.cards.append(Card(rank, suit))

  # draw a card. draws "face up" meaning the drawn card will be added to the end of the drawn_cards list. the end of the list represents the "bottom" of the deck of drawn cards, if the deck is arranged face down.
  def draw_card(self, i):
    card = self.cards.pop(i)
    self.drawn_cards.append(card)
    return card

  def draw_top(self):
    return self.draw_card(0)

  def draw_random(self):
    return self.draw_card(random.randint(0, len(self.cards) - 1))

  # put all the drawn cards back onto the top of the deck
  def collect(self):
    self.cards = self.drawn_cards + self.cards
    self.drawn_cards.clear()

  # shuffle the deck
  def shuffle(self):
    random.shuffle(self.cards)

  # deal a number of n-card hands.
  # returns a list of lists of cards
  def deal_hands(self, n_hands, n_cards):
    hands = [[] for i in range(n_hands)]

    for i in range(n_cards):
      for hand in hands:
        hand.append(self.draw_top())

    return hands

  def __len__(self):
    return len(self.cards)

  def __str__(self):
    s = ""
    for i in range(len(self.cards)):
      s += repr(self.cards[i])
      if i != len(self.cards) - 1:
        s += ","
    return s

  def __repr__(self):
    s = "<Deck object: "
    s += str(len(self.cards)) + " cards, "
    s += str(len(self.drawn_cards)) + " drawn"
    s += ">"
    return s

class Card:
  ranks = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
  rank_words = {"a": "ace", "j": "jack", "q": "queen", "k": "king"}
  rank_values = {"a": 1, "j": 10, "q": 10, "k": 10}
  suits = ["c", "h", "s", "d"]
  suit_words = ["clubs", "hearts", "spades", "diamonds"]

  u_suits = {"clubs": "♣", "hearts": "♥", "spades": "♠", "diamonds": "♦"}

  def __init__(self, *args):
    # if given one argument, it should be parsed with parse_card_string to get a tuple of (rank, suit). if given two arguments, they should be rank and suit.
    if len(args) == 1:
      tup = parse_card_string(args[0])

      if len(tup) != 1:
        raise ValueError

      tup = tup[0]

      rank = tup[0]
      suit = tup[1]
    elif len(args) == 2:
      rank = args[0]
      suit = args[1]
    else:
      raise TypeError

    rank = rank.lower()
    suit = suit.lower()

    if rank in self.ranks:
      self.rank = rank
    elif rank in self.rank_words.values():
      self.rank = rank[0]
    else:
      raise ValueError

    if suit in self.suits:
      self.suit = suit
    elif suit in self.suit_words:
      self.suit = suit[0]
    else:
      raise ValueError

    self.value = Card.rank_values[self.rank] if self.rank in Card.rank_values else int(self.rank)

  def __eq__(self, other):
    if type(self) != type(other):
      return False

    if self.rank == other.rank and self.suit == other.suit:
      return True

    return False

  def __hash__(self):
    return hash(self.__repr__())

  def __str__(self):
    s = ""
    if self.rank in Card.rank_words:
      s += Card.rank_words[self.rank].capitalize()
    else:
      s += self.rank
    s += " of "
    s += self.suit_words[self.suits.index(self.suit)].capitalize()
    return s

  def __repr__(self):
    s = self.rank + self.suit
    s = s.upper()
    return s

# display text representations of cards onto the terminal.
# can accept any number of arguments, and each argument must be either a Card object or an interable that contains only Card objects. otherwise, an exception is raised.
def display_cards(*args):
  cards = []

  for arg in args:
    if type(arg) == Card:
      cards.append(arg)
      continue

    itr = iter(arg) # raises error if a is not iterable

    for i in itr:
      if type(i) == Card:
        cards.append(i)
      else:
        raise TypeError

  if len(cards) == 0:
    print("No cards to display.")
    return

  for i in range(5):
    for j,card in enumerate(cards):
      if i == 0 or i == 4:
        print(" ", end="")
        print("-" * 5, end="")
        print(" ", end="")
      elif i == 1:
        rank = card.rank.upper()

        print("|", end="")
        print(rank + " " * (5 - len(rank)), end="")
        print("|", end="")
      elif i == 2:
        suit = card.suit[0].upper()
        #suit = Card.u_suits[card.suit]

        print("|", end="")
        print("  " + suit + "  ", end="")
        print("|", end="")
      elif i == 3:
        rank = card.rank.upper()

        print("|", end="")
        print(" " * (5 - len(rank)) + rank, end="")
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

  hand_range.sort()

  runs = []

  for i in range(3, len(hand_range)+1):
    combins = list(itertools.combinations(hand_range, i))

    for c in combins:
      s = sorted(list(set(c)))
      newc = list(c)

      if len(s) > 2 and s == newc:
        if max(s) - min(s) + 1 == len(s):
          runs.append(set(s))

  if len(runs) > 0:
    max_run = max(runs, key=lambda x: len(x))

    for i,r in enumerate(runs):
      if len(r) < len(max_run) and r.issubset(max_run):
        runs[i] = set()

  for r in runs:
    score += len(r)

    if explain:
      print("run", r)

  # if the hand has a jack with the same suit as the cut, add one point
  jacks = []

  for card in hand:
    if card.rank == "j":
      jacks.append(card.suit)

  for j in jacks:
    if j == cut.suit:
      score += 1

      if explain:
        print("jack")

      break

  # return the final score
  return score

# parse a string that is supposed to represent card(s). looks for strings like "AS" for "ace of spades", or "10H" for "10 of hearts" for example, and finds 1 or more of these matches, separated by non-word characters. like "as 10h" or "aS,10d" for example. if no cards found, returns empty list.
# otherwise, returns a list of tuples in the form [(rank, suit), ...]
def parse_card_string(string):
  pattern = r"(?:\b([2-9]|10|[AJQKajqk])([CHSDchsd])\b)+"
  match = re.findall(pattern, string)
  return match

# select card(s) from a list of cards. `text` is a string to pass to parse_card_string, cards is a list of Card objects.
# does not support selecting multiple of the same kind of card. say you wanted to select 2 aces of spades ("as,as"). given the card 'as' was present in `cards`, this would only return 1 ace of spades, even if multiple instances of that card were present in the list.
# returns a new list of cards from `cards` that were specified by `text`
def select_cards(text, cards):
  text_tuples = parse_card_string(text)

  result = set()

  for t in text_tuples:
    for c in cards:
      if t[0].lower() == c.rank and t[1].lower() == c.suit[0]:
        result.add(c)

  return result

# get user input to select n cards from a list of cards.
def user_select_cards(prompt, n_cards, cards):
  # keep getting user input until no error is raised (if everything is working as intended, no error would mean the user input is valid and the correct cards were returned)
  while True:
    text = input(prompt)

    try:
      selected = select_cards(text, cards)

      if len(selected) != n_cards:
        raise ValueError

      break
    except:
      # print an error if an exception was found, then continue the while loop
      print(f"Invalid input: Please select {n_cards} valid cards.")

  return selected

if __name__ == "__main__":
  # if any command line arguments were given, get the first one
  if len(sys.argv) > 1:
    arg = sys.argv[1]

    # test the program
    if arg == "t" or arg == "test":
      import crib_test
      crib_test.run()
    # start this script in interactive mode
    elif arg == "i" or arg == "interactive":
      import code
      code.interact(local=locals())

  # setup a standard deck of cards
  deck = Deck()

  # when a player reaches this score, they win the game
  max_score = 100

  # start two players off at scores of 0
  p1_score = p2_score = 0

  # the first crib starts with a randomly selected player 
  crib_turn = random.randint(1,2)

  # start the game loop
  while p1_score < max_score and p2_score < max_score:
    print("START TURN")
    print("scores: " + str(p1_score) + ", " + str(p2_score))
    print()

    # shuffle the deck
    deck.shuffle()

    # deal each player a hand of 6 cards
    p1_hand, p2_hand = deck.deal_hands(2, 6)

    print(f"crib goes to player {crib_turn}.")
    print()

    # print each users hand and get their input to select the cards they want to put in the crib, then remove the selected cards from each players hands and add those cards to the crib.
    crib = []

    for i in range(2):
      if i == 0:
        hand = p1_hand
      elif i == 1:
        hand = p2_hand

      print(f"player {i+1} hand:")
      display_cards(hand)
      crib_cards = user_select_cards("select 2 cards: ", 2, hand)
      print()

      for c in crib_cards:
        hand.remove(c)
        crib.append(c)

    # the cut is randomly drawn from the deck
    cut = deck.draw_random()
    print("cut:")
    display_cards(cut)
    print()

    # start pegging phase:

    p1_play_hand = p1_hand.copy()
    p2_play_hand = p2_hand.copy()

    # whoever doesnt have the crib this turn plays the first card.
    turn = 1 if crib_turn == 2 else 2

    # list of cards that have been played
    played = []
    played_values = []

    while True:
      if turn == 1 and len(p1_play_hand) == 0:
        if len(p2_play_hand) != 0:
          turn = 2
          continue
        break
      elif turn == 2 and len(p2_play_hand) == 0:
        if len(p1_play_hand) != 0:
          turn = 1
          continue
        break

      sum_of_played = sum(played_values)

      next_turn = False
      for c in hand:
        if sum_of_played + c.value <= 31:
          continue

        turn = 1 if turn == 2 else 2

        print(f"Last card: +1 for player {turn}")
        print()

        if turn == 1:
          p1_score += 1
        elif turn == 2:
          p2_score += 1

        played.clear()
        played_values.clear()

        next_turn = True
        break

      if next_turn:
        turn = 1 if turn == 2 else 2
        continue

      print(f"player {turn}s turn:")

      if turn == 1:
        hand = p1_play_hand
      elif turn == 2:
        hand = p2_play_hand

      display_cards(hand)

      while True:
        try:
          play = user_select_cards("play a card: ", 1, hand)

          for c in play:
            if sum_of_played + c.value > 31:
              raise ValueError

          break
        except:
          print("Invalid input: Total would exceed 31.")

      print()

      for c in play:
        if len(played) > 0 and c.rank == played[-1].rank:
          print(f"Pair: +2 for player {turn}.")
          print()

          if turn == 1:
              p1_score += 2
          elif turn == 2:
              p2_score += 2

        hand.remove(c)
        played.append(c)
        played_values.append(c.value)

      sum_of_played = sum(played_values)

      print("Total:", sum_of_played)
      print()

      if sum_of_played == 15:
        print(f"15: +2 for player {turn}.")
        print()

        if turn == 1:
            p1_score += 2
        elif turn == 2:
            p2_score += 2
      elif sum_of_played == 31:
        print(f"31: +2 for player {turn}.")
        print()

        if turn == 1:
            p1_score += 2
        elif turn == 2:
            p2_score += 2

        played.clear()
        played_values.clear()

      turn = 1 if turn == 2 else 2

    # score each hand and the crib, displaying all cards and their scores
    p1_hand_score = score_hand(p1_hand, cut)
    p2_hand_score = score_hand(p2_hand, cut)
    crib_score = score_hand(crib, cut)

    # print scores and all relevant cards.
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

    # add calculated scores to each player's scores
    p1_score += p1_hand_score
    p2_score += p2_hand_score
    if crib_turn == 1:
      p1_score += crib_score
    else:
      p2_score += crib_score

    # collect all drawn cards back into the deck
    deck.collect()

    # switch the crib over to the other player
    crib_turn = 1 if crib_turn == 2 else 2

    print("scores: " + str(p1_score) + ", " + str(p2_score))
    print("END TURN")
    print()

    input("press enter to continue: ")
    print()

  if p1_score > p2_score:
    print("player 1 wins")
  else:
    print("player 2 wins")
