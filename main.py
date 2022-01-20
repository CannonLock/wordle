import requests
import pickle
import numpy as np
from itertools import product
from os.path import exists
from termcolor import colored


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def read_five_letter_words():

  if exists("five_letter_words.pkl"):
    with open("five_letter_words.pkl", "rb") as fp:
      five_letter_words = pickle.load(fp)
      return five_letter_words

  file = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")

  words = list(file.iter_lines())

  five_letter_words = [word.decode("utf-8") for word in filter(lambda x: len(x) == 5, words)]

  with open("five_letter_words.pkl", "wb") as fp:
    pickle.dump(five_letter_words, fp)

  return five_letter_words


class Wordle:

  def __init__(self, letters, ranks):
    """
    Creates a Wordle state
    :param letters: The letters of the word
    :param ranks: States of letters 0 is unknown, 1 is in the word, 2 is letter is set
    """
    self.letters = np.array(list(letters))
    self.ranks = np.array(ranks)

  def __str__(self):
    str = ""

    for index, letter in enumerate(self.letters):
      if self.ranks[index] == 0:
        str += f"[{letter}]"
      elif self.ranks[index] == 1:
        str += colored(f"[{letter}]", "yellow")
      elif self.ranks[index] == 2:
        str += colored(f"[{letter}]", "green")

    return str

  def __repr__(self):
    return self.__str__()

  @staticmethod
  def get_possible_states(word):
    return [Wordle(list(word), rank) for rank in product(range(3), repeat=5)]


  def matches(self, word):

    cant_contain_letters = self.letters[np.where(self.ranks == 0)[0]]
    for letter in cant_contain_letters:
      if letter in word:
        return False

    must_contain_letters = self.letters[np.where(self.ranks == 1)[0]]
    for letter in must_contain_letters:
      if letter not in word:
        return False

    set_indices = np.where(self.ranks == 2)[0]
    for index in set_indices:
      if self.letters[index] != word[index]:
        return False

    return True

basic = Wordle.get_possible_states("basic")

basic[1].matches("carts")


five_letter_words = read_five_letter_words()

results = {}

for word in five_letter_words:
  print(word)
  results[word] = {}

  states = Wordle.get_possible_states(word)

  for state in states:
    results[word][str(state)] = list(filter(lambda x: state.matches(x), five_letter_words))

with open("results.pkl", "wb") as fp:
  pickle.dump(results, fp)






