import gym
import tensorflow as tf
from collections import namedtuple
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

# NOTES:
# Will need to deal with penalizing doing the same action over and over,
#  -> Only allow for N moves before returning a negative amount. The number
#     of moves will need to also be a piece of state that is sent back though
# We will need to keep track of how many cards are flipped over as all these cards
# will need to be visible in the state that is returned...so internally we will
# know what the value of the flipped over cards were but to the obs we just set it
# to be some unknown value (53?)

# The number which respresents an empty space
EMPTY_SPACE = 52
FLIPPED_CARD = 53

# An action represents a valid action that can occur in the double solitare
# Game. There are two types of actions: 'move_card' and 'advance_deck'. Moving
# a card requires valid start and end indicies, which are used to determine how
# to update the internal state representation with the new state. The advance_deck
# Action just requires start indices, which determines which deck should be 
# advanced by three cards (or less if it is the end of the deck).
Action = namedtuple('Action', ['type', 'start_indices', 'end_indices'])

class bcolors:
  GREEN = '\033[92m'
  RED = '\033[93m'
  ENDC = '\033[0m'

'''
Return the appropriate card denotation from a 0-12 number
'''
def format_card_number(number):
  shifted_number = number + 1
  if shifted_number == 1:
    return "A"
  elif shifted_number <= 10:
    return "{}".format(shifted_number)
  elif shifted_number == 11:
    return "J"
  elif shifted_number == 12:
    return "Q"
  elif shifted_number == 13:
    return "K"
  else:
    raise ValueError("Invalid number provided"); 

'''
format a card in a human readable way based on the index of the card
if they were all lined up Ace through King one suit at a time. 

>> format_card(21) = 9♥
'''
def format_card(index):
  suits = ["♠","♥","♣","♦"]
  # This means empty, there are no cards here
  if index == EMPTY_SPACE:
    return "__"

  number = int(index % (52 / 4))
  suit_index = int(tf.floor(index / (52 / 4)))
  suit = suits[suit_index]

  if suit_index % 2 == 1:
    return "{}{}{}{}".format(bcolors.RED, format_card_number(number), suit, bcolors.ENDC)

  return "{}{}".format(format_card_number(number), suit)

'''
Decodes a 1-hot vector encoding of a card and formats it in a
human-readable way
'''
def format_card_one_hot(encoding):
  index = int(tf.argmax(card_encoding, axis=0))
  return format_card(index)

'''
Create a random starting position for the actionable cards in
front of a player. This will be represented as a 7x7 array where
the first value in the array is the top card. The game state that
will be observable to the algorithm will just be the top card 
of each position

NOTE: This is not a 1-hot encoding, to make it more human readable
'''
def create_random_spread():
  stacks = []
  for i in range(1,8):
    stacks.append(np.pad(np.random.randint(0, high=52, size=(i,)), (0, 7-i), constant_values=EMPTY_SPACE))
  return np.array(stacks)

'''
Create a random deck for the player to go through, 3 cards at a time
'''
def create_random_deck():
  return np.random.randint(0, high=52, size=(24,))

def format_player_spread(spread):
  visible_cards = spread[:,0]
  result = ""

  for card in visible_cards:
    result += "{} ".format(format_card(card))

  return result

def format_aces_pot(aces_pot):
  visible_cards = aces_pot[:,0]
  result = ""

  for card in visible_cards:
    result += "{} ".format(format_card(card))

  return result

def format_player_deck(deck):
  return format_card(deck[0])

class DoubleSolitaireEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(DoubleSolitaireEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.action_space = spaces.Discrete(198)

    # Here "spread" is referring to the cards that are lined up
    # in front of a player which can be played on
    self.player_one_spread = create_random_spread()
    self.player_two_spread = create_random_spread()

    self.player_one_deck = create_random_deck()
    self.player_two_deck = create_random_deck()

    # 8x14 array of aces state
    self.aces_pot = np.full((8, 14), EMPTY_SPACE)

    # Space observable
    # The middle row of the three rows is for the aces,
    # The first and last have 7 spaces for the playable cards
    # and then one extra space for the deck that is being 
    # flipped through. Note that for now, we are not storing
    # how many cards are underneath the visible card right now
    # in the state
    self.observation_space = spaces.Box(low=0, high=1, shape=
                    (3, 8, 53), dtype=np.uint8)

  def is_valid_action(self, action_index):
    # Series of checks based on the action type


  def valid_actions(self):
    action_indices = range(len(ACTIONS))
    return list(filter(self.is_valid_action, action_indices))

  def step(self, action):
    pass

  def reset(self):
    pass

  def render(self, mode='human', close=False):
    return "{}     {}\n\n{}\n\n{}     {}".format(
      format_player_spread(self.player_one_spread),
      format_player_deck(self.player_one_deck),
      format_aces_pot(self.aces_pot),
      format_player_spread(self.player_two_spread),
      format_player_deck(self.player_two_deck),
    )

if __name__ == '__main__':
  env = DoubleSolitaireEnv()
  print(env.render())