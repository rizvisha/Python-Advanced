import time
from find_anagrams import perm_find_anagrams, sig_find_anagrams

def all_words(f):
  '''(file) -> list of str
  Return a list of all lines from f with newlines stripped.
  '''
  words = []
  for line in f:
    words.append(line.strip())
  return words
  

def run_finder(func, words, num_iterations, word):
  '''(function, list of str, int, str) -> float
  Test anagram-finder func num_iterations times, 
  using words as wordlist, generating anagrams of word. Return elapsed time.
  '''
  start = time.clock()
  for i in range(num_iterations):
    res = func(words, word)
  elapsed = time.clock() - start
  return elapsed


f = open('words.txt')
words = all_words(f)

num_iterations = 10 # increase if functions are too fast
word = 'abcdefgh' # change to test different words

elapsed = run_finder(sig_find_anagrams, words, num_iterations, word)
print('Signature time: ', elapsed)
elapsed = run_finder(perm_find_anagrams, words, num_iterations, word)
print('Permutation time: ', elapsed)
