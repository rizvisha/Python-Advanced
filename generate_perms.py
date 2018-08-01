def generate_perms(s):
  '''(str) -> list of str
  Return a list of all permutations of s.
  '''
  if len(s) == 0:
    return [""]
  ret = []
  for i in range(len(s)):
    shorter = s[0:i] + s[i+1:]
    short_perms = generate_perms (shorter)
    for p in short_perms:
      new_perm = s[i] + p
      if new_perm not in ret:
        ret.append (new_perm)
  return ret

def change(s1: Stack) -> None:
  s2 = Stack()
  while not s1.is_empty():
    first = s1.pop()
    if s1.is_empty():
      s2.push(first)
    else:
      second = s1.pop()
      s2.push(second)
      s2.push(first)
  while not s2.is_empty():
    s1.push(s2.pop())

s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.push(4)
change(s)
