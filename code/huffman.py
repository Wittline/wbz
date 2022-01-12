from typing import Dict

class Node:

    def __init__(self, char, freq, left=None, right=None):

        self.char = char
        self.freq = freq
        self.__left_child = left
        self.__right_child = right
        self.dir = ''
    
    def get_right_child(self):
        return self.__right_child

    def set_right_child(self, right_child):
        self.__right_child = right_child

    def get_left_child(self):
        return self.__left_child

    def set_left_child(self, left_child):
        self.__left_child = left_child


class Tree:

    def __init__(self, sequence):

        self.sequence = sequence
        self.frequency = Tree.freq_dict(self.sequence)
        self.root = self.create_tree()
        self.codes = {}


    def freq_dict(sequence):
        f_dict = {}
        for cr in sequence:            
            if cr in f_dict.keys():
                f_dict[cr] += 1
            else:
                f_dict[cr] = 1
        return f_dict

    def create_tree(self):

        leafs = []
        for char, freq in self.frequency.items():
            leafs.append(Node(char, freq))

        while len(leafs) > 1:

            leafs = sorted(leafs, key=lambda x: x.freq)

            left = leafs.pop(0)
            right = leafs.pop(0)

            new_char = left.char + right.char
            new_freq = left.freq + right.freq

            left.dir = "0"
            right.dir = "1"

            new_node = Node(new_char, new_freq, left, right)
            leafs.append(new_node)

        return leafs[0]

    def get_codings(self, node, val =''):

        curr_path = val + node.dir

        if node.left_child:
            self.get_codings(node.left_child, curr_path)
        if node.right_child:
            self.get_codings(node.right_child, curr_path)

        if not node.left_child and not node.right_child:
            self.codes[node.char] = curr_path

    def seq_to_binstr(self):        

        bin_str = ""
        for char in self.sequence:
            bin_str += self.codes[char]

        pad = 8 - len(bin_str) % 8
        if pad != 0:
            for _ in range(0, pad, 1):
                bin_str += '0'

        self.codes['pad'] = str(pad)

        return bin_str

    def binstr_to_unicode(bin_str):        
        unicode = ""
        for bit in range(0, len(bin_str), 8):
            eight_bits = bin_str[bit:bit+8]
            code = int(eight_bits, 2)
            unicode += chr(code)

        return unicode

    def unicode_to_binstr(unicode):

        bin_str = ""
        for uni in unicode:
            code = ord(uni)
            bin_str += '{:08b}'.format(code)

        return bin_str

    def remove_padding(bin_str, pad):
        return bin_str[:-pad]
    
    def binstr_to_seq(bin_str, codes):
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

    def codes_to_header(self):        

        header = ""
        for char, path in self.codes.items():
            header += char + "," + path + ";"

        return header + "\n"
    
    def header_to_codes(header):

        reconstructed_codes = {}
        for code in header.split(";")[:-1]:
            char, path = code.split(",")
            reconstructed_codes[char] = path
        return reconstructed_codes