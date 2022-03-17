from collections import Counter

class NodeT:
    
    def __init__(self, freq, left, right, isLeaf, value):
         self.freq = freq
         self.left = left
         self.right = right
         self.isLeaf = isLeaf
         self.value = value            

class Huffman:
    
  def __init__(self):    
    self.huffcodes = {}
    self.codes = []
    self.compressedFile = None
    self.tf = {}

  def encode(self, data):

      c = dict(Counter(data))
          
      for k, v in c.items():
            self.tf[k] = v

      lk  = self.tf.keys()      

      tl = [NodeT(self.tf.get(k),None, None, True, k) for k in lk]
      tl.sort(key=lambda x: x.freq)

      while len(tl)> 1:
          l = tl.pop(0)          
          r = tl.pop(0)
          tl.append(NodeT(l.freq + r.freq, l, r, False, None))
          tl.sort(key=lambda x: x.freq)

      self._huffmanCodes(tl.pop(0))

      self.compressedFile = ''.join([self.huffcodes.get(b) for b in data])

      return self.compressedFile
      
    
  def _huffmanCodes(self, tl):
      if tl.isLeaf == False:  
         l = tl.left
         r = tl.right
         self.codes.append("0")
         self._huffmanCodes(l)
         self.codes.pop()
         self.codes.append("1")
         self._huffmanCodes(r)
         self.codes.pop()
      else:
         self.huffcodes[tl.value] = ''.join(self.codes)
