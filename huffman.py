import doctest, time

from nodes import HuffmanNode, ReadNode, PriorityQueue


# ====================
# Helper functions for manipulating bytes


def get_bit(byte, bit_num):
  """ (int, int) -> int

  Return bit number bit_num from right in byte.

  >>> get_bit(0b00000101, 2)
  1
  >>> get_bit(0b00000101, 1)
  0
  """
  return (byte & (1 << bit_num)) >> bit_num

def byte_to_bits(byte):
  """ (int) -> str

  Return the representation of a byte as a string of bits.

  >>> byte_to_bits(14)
  '00001110'
  """
  return "".join([str(get_bit(byte, bit_num)) for bit_num in range(7, -1, -1)])


def bits_to_byte(bits):
  """ (str) -> int

  Return int represented by bits, padded on right.

  >>> bits_to_byte("00000101")
  5
  >>> bits_to_byte("101") == 0b10100000
  True
  """
  return sum([int(bits[pos]) * (1 << (7 - pos))
              for pos in range(len(bits))])


# ====================
# Functions for compression


def make_freq_dict(text):
  """ (bytes) -> dict of {int: int}

  Return a dictionary that maps each byte in text to its frequency.

  >>> d = make_freq_dict(bytes([65, 66, 67, 66]))
  >>> d == {65: 1, 66: 2, 67: 1}
  True
  """
  d = {}
  for ele in text:
    if ele not in d:
      d[ele] = 1

    else:
      d[ele] += 1
      
  return d


def helper_huffman_tree(freq_dict):
  """(dict) -> None

  Make a priority queue for items in freq_dict

  >>> freq = {3: 2, 2: 7, 9: 1}
  >>> helper_huffman_tree(freq)
  {1: HuffmanNode(9, None, None), 2: HuffmanNode(3, None, None), 7: HuffmanNode(2, None, None)}
  """
  p = PriorityQueue()
  
  for ele in freq_dict:
    node = HuffmanNode(ele)
    freq = freq_dict[ele]

    # make priority queue with freq as key and node as value
    p.insert(freq, node)
    
  return p


def huffman_tree(freq_dict):
  """ (dict of {int: int}) -> HuffmanNode

  Return the root HuffmanNode of a Huffman tree corresponding
  to frequency dictionary freq_dict.

  >>> freq = {2: 6, 3: 4}
  >>> t = huffman_tree(freq)
  >>> result1 = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
  >>> result2 = HuffmanNode(None, HuffmanNode(2), HuffmanNode(3))
  >>> t == result1 or t == result2
  True
  """
  
  p = helper_huffman_tree(freq_dict)
  
  match = True
  
  while match:
    n1 = p.extractMin()
    if p.is_empty(): # only runs when p has only one value(tree)
      match = False
      
    else:
      n2 = p.extractMin()
      # note: n1[1] refers to the second element in the tuple n1, which is the
      # node
      node = HuffmanNode(None, (n1[1]), (n2[1])) 

      # merge and insert
      # note: n1[0] refers to the first element in the tuple n1, which is the
      # frequency
      p.insert(n1[0] + n2[0], node)
    
  return n1[1]

  
def get_codes(tree):
  """ (HuffmanNode) -> dict of {int: str}

  Return a dict mapping symbols from tree rooted at HuffmanNode to codes.

  >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
  >>> d = get_codes(tree)
  >>> d == {3: '0', 2: '1'}
  True
  >>> tree = HuffmanNode(None, HuffmanNode(3, HuffmanNode(4), None), \
  HuffmanNode(2, None, HuffmanNode(9)))
  >>> d = get_codes(tree)
  >>> d == {9: '11', 2: '1', 3: '0', 4: '00'}
  True
  """
  dic = {}
  s = ''

  def helper(tree, s):
    if not tree or (not tree.left and not tree.right):
      return dic 
  
    if tree.left:
      if tree.left.symbol != None:
        dic[tree.left.symbol] = s + '0'
    helper(tree.left, s + '0') 

    
    if tree.right:
      if tree.right.symbol != None:
        dic[tree.right.symbol] = s + '1'
    helper(tree.right, s + '1')
    
  helper(tree, s)
  
  return dic


def post_order(t): # helper for number_nodes and tree_to_bytes
  """ (HuffmanNode) -> NoneType

  Return a list consisting of HuffmanNodes visited in post order traversal

  >>> left = HuffmanNode(None, HuffmanNode(3, None, None), HuffmanNode(2, None, None))
  >>> right = HuffmanNode(5)
  >>> tree = HuffmanNode(None, left, right)
  >>> post_order(tree)
  [HuffmanNode(3, None, None), HuffmanNode(2, None, None), HuffmanNode(None, HuffmanNode(3, None, None), HuffmanNode(2, None, None)), HuffmanNode(5, None, None), HuffmanNode(None, HuffmanNode(None, HuffmanNode(3, None, None), HuffmanNode(2, None, None)), HuffmanNode(5, None, None))]
  """
  
  if not t:
    return []
  return  post_order(t.left) + post_order(t.right) + [t]
  

def number_nodes(tree):
  """ (HuffmanNode) -> NoneType

  Number internal nodes in tree according to postorder traversal;
  start numbering at 0.

  >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
  >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
  >>> tree = HuffmanNode(None, left, right)
  >>> number_nodes(tree)
  >>> tree.left.number
  0
  >>> tree.right.number
  1
  >>> tree.number
  2
  >>> left = HuffmanNode(None, HuffmanNode(3, HuffmanNode(6), None), \
  HuffmanNode(2))
  >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
  >>> tree = HuffmanNode(None, left, right)
  >>> number_nodes(tree)
  >>> tree.left.left.number
  0
  >>> tree.left.number
  1
  >>> tree.right.number
  2
  >>> tree.number
  3
  """
  
  n = 0
  
  # call to helper function post_order (line 169)
  lst = post_order(tree)
  
  for ele in lst:
    if not ele.is_leaf():
      ele.number = n
      n += 1
      
  
def avg_length(tree, freq_dict):
  """(HuffmanNode, dict of {int : int}) -> float

  Return the number of bits per symbol required to compress text
  made of the symbols and frequencies in freq_dict, using the Huffman tree.
  
  >>> freq = {3: 2, 2: 7, 9: 1}
  >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
  >>> right = HuffmanNode(9)
  >>> tree = HuffmanNode(None, left, right)
  >>> avg_length(tree, freq)
  1.9
  """
  # total_bits = Σ (we sum for all symbols) (length of code for a symbol * \
  # frequency of the symbol)
  # average_bits = (total_bits)/(total number of symbols)

  codes = get_codes(tree) 
  lst1 = freq_dict.keys()
  
  total_bits = 0
  
  for ele in lst1:
    if ele in codes:
      len_code = len(codes[ele])
      frequency = freq_dict[ele]
      total_bits = total_bits + (len_code * frequency) 

  number_of_symbols = 0
  
  for freq in freq_dict.values():
    number_of_symbols = number_of_symbols + freq
    
  avge_bits = total_bits / number_of_symbols
  
  return avge_bits

  
def generate_compressed(text, codes):
  """ (bytes, dict of {int: str}) -> bytes

  Return compressed form of text, using mapping in codes for each symbol.

  >>> d = {0: "0", 1: "10", 2: "11"}
  >>> text = bytes([1, 2, 1, 0])
  >>> result = generate_compressed(text, d)
  >>> [byte_to_bits(byte) for byte in result]
  ['10111000']
  >>> text = bytes([1, 2, 1, 0, 2])
  >>> result = generate_compressed(text, d)
  >>> [byte_to_bits(byte) for byte in result]
  ['10111001', '10000000']
  """
  
  s = ''
  
  for ele in text:
    if ele in codes:
      code = codes[ele]
      s = s + code # the string of binary code we need to convert 

  byte_list = bytearray([])
  
  while len(s) > 0:
    byte_list.append(bytearray([bits_to_byte(s[:8])]))
    s = s[8:]
  
  return byte_list  

  
def tree_to_bytes(tree):
  """(HuffmanNode) -> bytes

  Return a bytes representation of the Huffman tree rooted at tree.
  The representation should be based on the postorder traversal of tree.
  Precondition: tree has its nodes numbered.
  
  >>> tree = HuffmanNode(None, HuffmanNode(3, None, None), HuffmanNode(2, None, None))
  >>> number_nodes(tree)
  >>> list(tree_to_bytes(tree))
  [0, 3, 0, 2]
  >>> left = HuffmanNode(None, HuffmanNode(3, None, None), HuffmanNode(2, None, None))
  >>> right = HuffmanNode(5)
  >>> tree = HuffmanNode(None, left, right)
  >>> number_nodes(tree)
  >>> list(tree_to_bytes(tree))
  [0, 3, 0, 2, 1, 0, 0, 5]
  """
  
  lst = post_order(tree) # call to the post_order helper function (line 169)
  
  b = bytes([])

  for ele in lst:
    if not ele.is_leaf():
      
      if ele.left.is_leaf():
        b = b + bytes([0]) + bytes([ele.left.symbol])
      else:
        b = b + bytes([1]) + bytes([ele.left.number])
 
      if ele.right.is_leaf():
        b = b + bytes([0]) + bytes([ele.right.symbol])
      else:
        b = b + bytes([1]) + bytes([ele.right.number])
        
  return b

  
def num_nodes_to_bytes(tree):
  """ (HuffmanNode) -> bytes
  Return number of nodes required to represent tree, the root of a
  numbered Huffman tree.
  """
  return bytes([tree.number + 1])


def size_to_bytes(size):
  """ (int) -> bytes
  Return the size as a bytes object.

  >>> list(size_to_bytes(300))
  [44, 1, 0, 0]
  """
  # little-endian representation of 32-bit (4-byte)
  # int size
  return size.to_bytes(4, "little")


def compress(in_file, out_file):
  """ (str, str) -> NoneType
  Compress contents of in_file and store results in out_file.
  """
  text = open(in_file, "rb").read()
  freq = make_freq_dict(text)
  tree = huffman_tree(freq)
  codes = get_codes(tree)
  number_nodes(tree)
  print("Bits per symbol:", avg_length(tree, freq))
  result = (num_nodes_to_bytes(tree) + tree_to_bytes(tree) +
            size_to_bytes(len(text)))
  result += generate_compressed(text, codes)
  open(out_file, "wb").write(result)


# ====================
# Functions for decompression


def generate_tree_general(node_lst, root_index):
  """ (list of ReadNode, int) -> HuffmanNode

  Return the root of the Huffman tree corresponding to node_lst[root_index].
  The function assumes nothing about the order of the nodes in the list.

  >>> lst = [ReadNode(0, 5, 0, 7)]
  >>> generate_tree_general(lst, 0)
  HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None))
  """
  
  root = node_lst[root_index]
  node = HuffmanNode()
  
  if root.l_type == 0:
    node.left = HuffmanNode(root.l_data)
    
  else:
    node.left = generate_tree_general(node_lst, root.l_data) 

  if root.r_type == 0:
    node.right = HuffmanNode(root.r_data)
    
  else:
    node.right = generate_tree_general(node_lst, root.r_data) 
    
  return node


def generate_tree_postorder(node_lst, root_index):
  """ (list of ReadNode, int) -> HuffmanNode

  Return the root of the Huffman tree corresponding to node_lst[root_index].
  The function assumes that the list represents a tree in postorder.

  >>> lst = [ReadNode(0, 5, 0, 7)]
  >>> generate_tree_postorder(lst, 0)
  HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None))
  """
  
  root = node_lst[root_index]
  node = HuffmanNode()

  if root.l_type == 0:
    node.left = HuffmanNode(root.l_data)
    if root.r_type == 0:
      node.right = HuffmanNode(root.r_data)
    else: # right node is NOT a leaf
      node.right = generate_tree_general(node_lst, (root_index - 1))

  else: # * left node is NOT a leaf *
    if root.r_type == 0:
      node.right = HuffmanNode(root.r_data)
      node.left = generate_tree_general(node_lst, (root_index - 1))
    else: # neither node is a leaf
      node.right = generate_tree_general(node_lst, (root_index - 1))
      node.left = generate_tree_general(node_lst, (root_index - 2))
    
  return node
  
def generate_uncompressed(tree, text, size):
  """ (HuffmanNode, bytes, int) -> bytes
  Use Huffman tree to decompress size bytes from text.
  """
  
  # codes will be a mapping of symbols to their codes
  codes = get_codes(tree)
  
  # symbols and their codes are unique so we can flip keys and values
  dic = {value : key for key,value in codes.items()}
  
  string_bits = ''
  for byte in text:
    string_bits = string_bits + byte_to_bits(byte)

  uncmopressed_bytes = bytes([])
  while len(uncmopressed_bytes) < size:
    i = 0
    bit_code = string_bits[i]
    while bit_code not in dic:
      i += 1
      bit_code = string_bits[0 : i]
    uncmopressed_bytes = uncmopressed_bytes + bytes([dic[bit_code]])
    s = s[i:]

  return uncmopressed_bytes
  
def bytes_to_nodes(buf):
  """ (bytes) -> list of ReadNode

  Return a list of ReadNodes corresponding to the bytes in buf.

  >>> bytes_to_nodes(bytes([0, 1, 0, 2]))
  [ReadNode(0, 1, 0, 2)]
  """
  lst = []
  for i in range(0, len(buf), 4):
    l_type = buf[i]
    l_data = buf[i+1]
    r_type = buf[i+2]
    r_data = buf[i+3]
    lst.append(ReadNode(l_type, l_data, r_type, r_data))
  return lst


def bytes_to_size(buf):
  """ (bytes) -> int
  Return the size corresponding to the given 4-byte 
  little-endian representation.

  >>> bytes_to_size(bytes([44, 1, 0, 0]))
  300
  """
  return int.from_bytes(buf, "little")


def uncompress(in_file, out_file):
  """ (str, str) -> NoneType
  Uncompress contents of in_file and store results in out_file.
  """
  f = open(in_file, "rb")
  num_nodes = f.read(1)[0]
  buf = f.read(num_nodes * 4)
  node_lst = bytes_to_nodes(buf)
  # use generate_tree_general or generate_tree_postorder here
  tree = generate_tree_general(node_lst, num_nodes - 1)
  size = bytes_to_size(f.read(4))
  g = open(out_file, "wb")
  text = f.read()
  g.write(generate_uncompressed(tree, text, size))


# ====================
# Other functions

def helper1_improve_tree(freq_dict):
  """ (dict) -> list

  >>> freq = {3: 2, 2: 7, 9: 1}
  >>> helper1_improve_tree(freq)
  [2, 3, 9]

  Return a list containing  all symbols in freq_dict in descending orders with
  respect to frequency.
  """
  
  lst = []

  while len(freq_dict) != 0:
    symbol = max(freq_dict, key = freq_dict.get)
    lst.append(symbol)
    del freq_dict[symbol]

  return lst

def helper2_improve_tree(tree, lst):
  """(tree, list) -> NoneType

  Improve the tree as much as possible, without changing its shape, by assigning
  nodes of tree, the symbols from lst.
  """
  
  if not tree:
    return
  
  if len(lst) != 0:
    if tree.left and (tree.left.is_leaf()):
      
      # assign the least deep leaf (depth 1 if left subtree of root is leaf)
      # the most frequent symbol
      tree.left.symbol = lst.pop(0) 
  
  if len(lst) != 0:
    if tree.right and (tree.right.is_leaf()):
      
      # assign the least deep leaf (depth 1 if right subtree of root is leaf)
      # the most frequent symbol (second most frequent if the previous if
      # statement was true)
      tree.right.symbol = lst.pop(0)

  helper2_improve_tree(tree.left, lst)
  helper2_improve_tree(tree.right, lst)

def improve_tree(tree, freq_dict):
  """(HuffmanNode, dict of {int : int}) -> NoneType

  Improve the tree as much as possible, without changing its shape,
  by swapping nodes. The improvements are with respect to freq_dict.

  >>> tree = HuffmanNode(None, HuffmanNode(None, HuffmanNode(99, None, None),\
  HuffmanNode(100, None, None)), HuffmanNode(None, HuffmanNode(101, None, None),\
  HuffmanNode(None, HuffmanNode(97, None, None), HuffmanNode(98, None, None))))
  >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
  >>> improve_tree(tree, freq)
  >>> avg_length(tree, freq)
  2.31
  """

  if not tree  or tree.is_leaf():
    return

  # make a replica of freq_dict which will be modified in helper1_improve_tree
  # instead of freq_dict  as other functions might want to use freq_dict after
  #running improve_tree without wanting to re-define freq_dict
  dict2 = dict(freq_dict)

  lst = helper1_improve_tree(dict2)
  
  helper2_improve_tree(tree, lst)


  
if __name__ == "__main__":
  doctest.testmod()

  mode = input("Press c to compress or u to uncompress: ")
  if mode == "c":
    fname = input("File to compress: ")
    start = time.time()
    compress(fname, fname + ".huf")
    print("compressed {} in {} seconds.".format(fname, time.time() - start))
  elif mode == "u":
    fname = input("File to uncompress: ")
    start = time.time()
    uncompress(fname, fname + ".orig")
    print("uncompressed {} in {} seconds.".format(fname, time.time() - start))

