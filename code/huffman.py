from collections import Counter

class NodeT:
    
    def __init__(self, freq, left, right, isLeaf, valueLeaf):
         self.freq = freq
         self.left = left
         self.right = right
         self.isLeaf = isLeaf
         self.valueLeaf = valueLeaf
         
    def getLeft(self):
        return self.left
        
    def getRight(self):
        return self.right
        
    def F(self):
        return self.freq
        
    def V(self):
        return self.valueLeaf

class Huffman:
  def __init__(self, fileBytes):
    self.fileBytes = fileBytes
    self.huffcodes = {}
    self.codes = []
    self.compressedFile = None
    self.tf = {}

  def encode(self):  

      c = dict(Counter(self.fileBytes))
          
      for k, v in c.items():
            self.tf[k] = v

      lk  = self.tf.keys()      

      tl = [NodeT(self.tf.get(k),None, None, True, k) for k in lk]
      tl.sort(key=lambda x: x.freq)

      while len(tl)> 1:          
          l = tl.pop(0)          
          r = tl.pop(0)                    
          tl.append(NodeT(l.F() + r.F(), l, r, False, None))
          tl.sort(key=lambda x: x.freq)

      self._huffmanCodes(tl.pop(0))

      self.compressedFile = ''.join([self.huffcodes.get(b) for b in self.fileBytes])
      
      #Returning the huffman table, new bytes compressed, remaining in bits
      #return self.huffmancodes, ''.join(cf), remained    
    
  def _huffmanCodes(self, tl):
      if tl.isLeaf == False:  
         l = tl.getLeft()
         r = tl.getRight()
         self.codes.append("0")
         self._huffmanCodes(l)
         self.codes.pop()
         self.codes.append("1")
         self._huffmanCodes(r)
         self.codes.pop()
      else:
         self.huffcodes[tl.V()] = ''.join(self.codes)
