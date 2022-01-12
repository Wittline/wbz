from typing import Dict

class HuffmanNode:
    """A class to represent heap nodes of a huffman coding tree.
    Attributes
    ----------
    char: str
        The character to be saved as a node value.
    freq: int
        The frequency of the char.
    right_child: HuffmanNode
        The right child of the heap node.
    left_child: HuffmanNode
        The left child of the heap node.
    dir: str
        The path of the current node in the Huffman tree, usually a string of
        0s and 1s.
    """
    def __init__(self: object, char: str, freq: int, left: object=None, right: object=None) -> None:
        """Class constructor
        Parameters
        ----------
        char : str
            A character (Huffman coding characters).
        freq : int
            The frequency of the character.
        left : object, optional
            The left child of the heap node. The default is None.
        right : object, optional
            The right child of the heap node. The default is None.
        Returns
        -------
        None
            A class instance.
        """
        self.char = char
        self.freq = freq
        self.__left_child = left
        self.__right_child = right
        self.dir = ''

    @property
    def right_child(self):
        """The getter of the right child.
        Returns
        -------
        object
        """
        return self.__right_child

    @right_child.setter
    def right_child(self, right_child):
        """The setter of the right child.
        Parameters
        ----------
        right_child : object
            The new child.
        Returns
        -------
        None
        """
        self.__right_child = right_child

    @property
    def left_child(self: object) -> object:
        """The getter of the left child.
        Returns
        -------
        object
        """
        return self.__left_child

    @left_child.setter
    def left_child(self: object, left_child: object) -> None:
        """The setter of the left child.
        Parameters
        ----------
        right_child : object
            The new child.
        Returns
        -------
        None
        """
        self.__left_child = left_child

    def __str__(self: object) -> str:
        """Returns a string representation using print().
        Returns
        -------
        str
            A string to be displayed with print().
        """
        return "Hello! I'm a Huffman coding HeapNode class instance."

    def __repr__(self: object) -> str:
        """A coder friendly representation of the HuffmanNode object.
        Returns
        -------
        str
            A string.
        """
        return "Node(%s, freq=%s, right=%s, left=%s)"%(self.char,
                                                       self.freq,
                                                       self.right_child,
                                                       self.left_child)

class HuffmanTree:
    """A class to represent a huffman tree.
    Attributes
    ----------
    sequence: str
        The sequence to be encoded, i.e; the Burros-Wheeler transform of the
        sequence.
    frequency: Dict[str, int]
        A dictionary to store frequency values for each character of the
        sequence, the character as a key and its frequency as a value.
    root: HuffmanNode
        The root node of the Huffman tree.
    codes: Dict[str, str]
        The Huffman codes for a given sequence, The character as a key and
        its tree path as a value(a string).
    pad: int
        The padding of the sequence, i.e; the number of zeroes that was added
        to the end of sequence until it was divisible by 8 (coding in 8 bits).
    """
    def __init__(self, sequence):
        """The class constructor.
        Parameters
        ----------
        sequence : str
            The sequence to be coded.
        Returns
        -------
        None
            A class instance.
        """
        self.sequence = sequence
        self.frequency = HuffmanTree.freq_dict(self.sequence)
        self.root = self.create_tree()
        self.codes = {}


    def freq_dict(sequence):
        f_dict = {}
        for n in sequence:
            cr = chr(n)
            if cr in f_dict.keys():
                f_dict[cr] += 1
            else:
                f_dict[cr] = 1
        return f_dict

    def create_tree(self):
        """The main algorithm for creating The Huffman tree.
        Returns
        -------
        HuffmanNode
            The root node of the tree.
        """
        leafs = [] # creating a list for leafs of the tree
        for char, freq in self.frequency.items():
            leafs.append(HuffmanNode(char, freq))

        while len(leafs) > 1: # while there is more than one element, do the algoritm

            leafs = sorted(leafs, key=lambda x: x.freq) # sort the leafs by frequency

            left = leafs.pop(0) # taking the first least frequency node as the left node
            right = leafs.pop(0) # taking the second  least frequency node as the right node

            new_char = left.char + right.char # the new character
            new_freq = left.freq + right.freq # the new frequency is the sum

            left.dir = "0" # assign 0 as a direction for the left node
            right.dir = "1" # assign 1 as a direction for the right node 

            new_node = HuffmanNode(new_char, new_freq, left, right) # create a new node and then append it
            leafs.append(new_node)

        return leafs[0]

    def get_codings(self: object, node: HuffmanNode, val: str='') -> None:
        """A depth-first search recursive algorithm to find the paths of each
        character in the tree.
        Parameters
        ----------
        node : HuffmanNode
            The starting node, the root of the tree.
        val : str, optional
            The path of the current recursion in a tree. The default is ''.
        Returns
        -------
        None
            Fills the codes dictionary property of the Huffman Tree.
        """

        curr_path = val + node.dir # the current path in the recursion

        if node.left_child:
            self.get_codings(node.left_child, curr_path)
        if node.right_child:
            self.get_codings(node.right_child, curr_path)

        if not node.left_child and not node.right_child:
            self.codes[node.char] = curr_path

    def seq_to_binstr(self: object) -> str:
        """This method transforms the current sequence of the Huffman tree
        to a binary sequence using the codes (paths of every character), it
        also adds a padding to the end of the binary sequence (a variable
        number of zeroes, when sequence is divisible by 8 then add 8 zeroes
        by default). The binary sequence will be coded in 8-bits later.
        It saves the padding in the codes property.
        Returns
        -------
        str
            The binary sequence.
        """

        bin_str = ""
        for char in self.sequence:
            bin_str += self.codes[char]

        pad = 8 - len(bin_str) % 8
        if pad != 0:
            for _ in range(0, pad, 1):
                bin_str += '0'

        self.codes['pad'] = str(pad) #Save the padding value to codes

        return bin_str

    def binstr_to_unicode(bin_str):
        """This method codes a binary sequence in 8-bits in UTF-8.
        Parameters
        ----------
        bin_str : str
            The binary sequence to be coded.
        Returns
        -------
        str
            The unicode string that corrsponds to the binary sequence.
        """

        unicode = ""
        for bit in range(0, len(bin_str), 8): # cut the sequence to 8-bits
            eight_bits = bin_str[bit:bit+8]
            code = int(eight_bits, 2)
            unicode += chr(code)

        return unicode

    def unicode_to_binstr(unicode: str):
        """Transforms a unicode sequence to a binary sequence.
        Parameters
        ----------
        unicode : str
            The unicode sequence to be transformed.
        Returns
        -------
        str
            The corrsponding binary string.
        """

        bin_str = ""
        for uni in unicode:
            code = ord(uni)
            bin_str += '{:08b}'.format(code)

        return bin_str

    def remove_padding(bin_str, pad):
        """This function removes the padding from a given binary sequence,
        the padding is normally a variable number of zeroes added when coding
        in 8-bits.
        Parameters
        ----------
        bin_str : str
            The binary string to be stripped from a sequence of zeroes.
        pad : int
            The padding, the number of zeroes at the end of the binary
            sequence.
        Returns
        -------
        str
            The no-padded binary string.
        """
        return bin_str[:-pad] # take all the sequence without the padding

    @staticmethod
    def binstr_to_seq(bin_str: str, codes: Dict[str, str]) -> str:
        """Transforms a binary string to a sequence given a codes dictionary
        of paths.
        Parameters
        ----------
        bin_str : str
            The binary string to be transformed.
        codes : Dict[str, str]
            A dictionary of characters alongside their paths.
        Returns
        -------
        str
            The original sequence.
        """

        original_seq = ""
        reading_stream = ""
        for num in bin_str:
            reading_stream += num
            for char, path in codes.items():
                if path == reading_stream:
                    original_seq += char
                    reading_stream = ""
                    break

        return original_seq

    def codes_to_header(self: object) -> str:
        """This method transforms the codes of a given Huffman tree object
        into a header to be saved in the compressed file (useful for
        when decompressing later).
        Returns
        -------
        str
            The header of the compressed file.
        """

        header = ""
        for char, path in self.codes.items():
            header += char + "," + path + ";"

        return header + "\n"

    @staticmethod
    def header_to_codes(header: str) -> Dict[str, str]:
        """This method takes the header of a compressed file and transforms
        it into a codes dictionary that's useful when decompressing a sequence.
        Parameters
        ----------
        header : str
            The header of the compressed file.
        Returns
        -------
        Dict[str, str]
            A codes dictionary which maps from characters to thier given paths.
        """
        reconstructed_codes = {}
        for code in header.split(";")[:-1]:
            char, path = code.split(",")
            reconstructed_codes[char] = path
        return reconstructed_codes