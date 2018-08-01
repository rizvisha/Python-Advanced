class HuffmanNode:

  """A node in a Huffman tree.
  Symbols occur only at leaves.
  Each node has a number attribute that can be used for node-numbering.
  """
    
  def __init__(self, symbol=None, left=None, right=None):
    """(HuffmanNode, int|None, HuffmanNode|None, HuffmanNode|None,
    HuffmanNode|None)
    
    Create a new HuffmanNode with the given parameters.
    """
    self.symbol = symbol
    self.left, self.right = left, right
    self.number = None
    
  def __eq__(self, other):
    """(HuffmanNode, HuffmanNode) -> bool
    
    Return True iff self is equivalent to other.
    
    >>> a = HuffmanNode(4)
    >>> b = HuffmanNode(4)
    >>> a == b
    True
    >>> b = HuffmanNode(5)
    >>> a == b
    False
    """
    return (type(self) == type(other) and self.symbol == other.symbol and
    self.left == other.left and self.right == other.right)

  def __lt__(self, other):
    """ (HuffmanNode, HuffmanNode) -> bool
    
    Return True iff self is less than other.
    """
    return False # arbitrarily say that one node is never less than another
    
  def __repr__(self):
    """(HuffmanNode) -> str
    
    Return constructor-style string representation.
    
    """
    return 'HuffmanNode({}, {}, {})'.format(self.symbol,
    self.left, self.right)
    
  def is_leaf(self):
    """(HuffmanNode) -> bool
    
    Return True iff self is a leaf.
    
    >>> t = HuffmanNode(None)
    >>> t.is_leaf()
    True
    """
    return not self.left and not self.right
    

class ReadNode:

  """A node as read from a compressed file.
  Each node consists of type and data information as described in the handout.
  This class offers a clean way to collect this information together for each node.
  """
  
  def __init__(self, l_type, l_data, r_type, r_data):
    """(ReadNode, int, int, int, int)
    
    Create a new ReadNode with the given parameters.
    """
    self.l_type, self.l_data = l_type, l_data
    self.r_type, self.r_data = r_type, r_data
  
  def __repr__(self):
    """(ReadNode) -> str
    
    Return constructor-style string representation.
    
    """
    return 'ReadNode({}, {}, {}, {})'.format(
    self.l_type, self.l_data, self.r_type, self.r_data)



class PriorityQueueError(Exception):
  pass

class PriorityQueue:

  def __init__(self):
    """(PriorityQueue, dict) -> None

    Create a PriorityQueue object
    """
    
    self._items = {}


  def __repr__(self):
    """(self) -> str

    Return constructor-style string representation.
    """
    
    if self._items == {}:
      return '{}'
    x = '{'
    for ele in (self._items):
      x = x + (repr(ele)) + ':' + ' ' + (repr(self._items[ele])) + ',' + ' '
    x = x.strip()
    x = x[:-1]
    return x + '}'


  def insert(self, key, val):
    """(self, int, val) -> None

    Insert the value = 'val' with key = 'key' to the Queue
    """

    # keys will be frequencies. keys cannot be HuffmanNodes: unhashable
    if isinstance(key, int):
      self._items[key] = val
    else:
      raise PriorityQueueError('Queue takes only integers as key')


  def extractMin(self):
    """ (self) -> tuple

    Extract and return the value with the smallest key
    """
    
    if self._items == {}:
      raise PriorityQueueError('Cannot extract from empty Queue')
    
    mini_key = min(self._items.keys()) # get the key with lowest value
    
    #the key and value for that key as a tuple
    mini = (mini_key, self._items[mini_key])
    
    del self._items[mini_key]
    
    return mini

  
  def min(self):
    """(self) -> tuple

    Return the value with the smallest key
    """
    
    if self._items == {}:
      raise PriorityQueueError('Cannot return value from empty Queue')
    
    mini_key = min(self._items.keys()) #get the key with lowest value
    
    #the key and value for that key as a tuple
    mini = (mini_key, self._items[mini_key])
    return mini


  def is_empty(self):
    """(self) -> bool

    Return True iff the Queue is empty
    """
    
    return self._items == {}
    
if __name__ == '__main__':
  import doctest
  doctest.testmod()
  
