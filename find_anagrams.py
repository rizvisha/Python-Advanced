from generate_perms import generate_perms

def perm_find_anagrams(word_lst, word):
  '''(list of str, str) -> list of str
  Return the list of permutations of word that exist in word_lst.
  '''
  res = []
  perms = generate_perms(word)
  for potential in perms:
    if potential in word_lst:
      res.append(potential)
  return res

def signature(s):
  '''(str) -> str
  Return the signature of s.
  '''
  lst = list(s)
  lst.sort()
  return ''.join(lst)

def sig_find_anagrams(word_lst, word):
  '''(list of str, str) -> list of str
  Return the list of words from word_lst that have 
  the same signature as word.
  '''
  res = []
  sig = signature(word)
  for check_word in word_lst:
    if signature(check_word) == sig:
      res.append(check_word)
  return res
  