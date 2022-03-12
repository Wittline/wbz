from collections import Counter

class NodeT:
    
    def __init__(self, frequency, left, right, isLeaf, valueLeaf):
         self.frequency = frequency
         self.left = left
         self.right = right
         self.isLeaf = isLeaf
         self.valueLeaf = valueLeaf
         
    def getLeft(self):
        return self.left
        
    def getRight(self):
        return self.right
        
    def F(self):
        return self.frequency
        
    def V(self):
        return self.valueLeaf

class Huffman:
  def __init__(self, fileBytes):
    self.fileBytes = fileBytes
    self.huffmancodes = {}
    self.codes = []
    self.compressedFile = None
    self.tablefrequency = {}
    self.realLength = 0
    self.remained=0
    self.base_table = None

  def compress(self):  

      self.realLength = len(self.fileBytes)

      c = dict(Counter(self.fileBytes))
          
      for key, value in c.items():
            self.tablefrequency[key] = value                                        
      tl = []
      lk  = self.tablefrequency.keys()             
      
      for k in lk:          
          n  = NodeT(self.tablefrequency.get(k),None, None, True, k)
          tl.append(n)                
                
      tl.sort(key=lambda x: x.frequency)
                  
      while len(tl)> 1:          
          l = tl.pop(0)          
          r = tl.pop(0)          
          tn = NodeT(l.F() + r.F() ,l, r, False, None)     
          tl.append(tn)
          tl.sort(key=lambda x: x.frequency)
                  
      self._huffmanCodes(tl.pop(0))            
            
      cf = []
      for b in self.fileBytes:
          cf.append(self.huffmancodes.get(b))  
      
      self.compressedFile = ''.join(cf)
      #Returning the huffman table, new bytes compressed, remaining in bits
      #return self.huffmancodes, ''.join(cf), remained
    
  def _huffmanCodes(self, tl):       
      if tl.isLeaf == False:         
         l = tl.getLeft()
         r = tl.getRight()
         self.codes.append("0")
         self._huffmanCodes(l);
         self.codes.pop()
         self.codes.append("1")
         self._huffmanCodes(r) 
         self.codes.pop()
      else:                        
         self.huffmancodes[tl.V()] = ''.join(self.codes)
