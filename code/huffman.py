import time
import os.path
import heapq as heap
from operator import itemgetter
from bitarray import bitarray


class Node(object):

    def __init__(self, value, frequency):
        self.left = None
        self.right = None
        self.value = value
        self.frequency = frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def set_children(self, left, right):
        self.left = left
        self.right = right


class Huffman(object):

    def __init__(self):
        pass

    def write_code_lengths(self, current_node, code_size, code_lengths):

        if current_node.value is not None: 
            code_lengths[current_node.value] = code_size
        else:  
            self.write_code_lengths(current_node.left, code_size + 1, code_lengths)
            self.write_code_lengths(current_node.right, code_size + 1, code_lengths)


    def write_code_book(self, ordered_code_lengths):

        code_book = []
        current_length = ordered_code_lengths[0][1]
        code_int = 0

        for char_length in ordered_code_lengths:
            
            code_int = code_int << (char_length[1] - current_length)
            current_length = char_length[1]
            
            code = format(code_int, "0" + str(current_length) + "b")
            code_book.append((char_length[0], code)) 
            code_int += + 1

        code_book.sort()
        return code_book


    def code_book_output_canonical(self, code_book_list):

        code_book_output = ""
        previous_val = 0
        for char_length in code_book_list:
            for _ in range(previous_val, char_length[0] - 1):
                code_book_output += "0"  
            previous_val = char_length[0]
            code_book_output += "1"  
            code_book_output += format(len(char_length[1]), "06b")

        for _ in range(previous_val, 256):
            code_book_output += "0"
        return code_book_output


    def code_book_output_tradition(self, code_book_list):

        code_book_output = ""
        for char_length in code_book_list:
            code_book_output += format(char_length[0], "08b")
            code_book_output += format(len(char_length[1]), "04b")
        return code_book_output


    def encode(self, data):


        frequencies = {}
        for character in data:        
            if character in frequencies.keys():
                frequencies[character] += 1
            else:
                frequencies[character] = 1


        node_list = []
        for val, freq in frequencies.items():
            added_node = Node(val, freq)
            node_list.append(added_node)

        heap.heapify(node_list)

        while len(node_list) > 1:
            right = heap.heappop(node_list)
            left = heap.heappop(node_list)
            new_node = Node(None, right.frequency + left.frequency)
            new_node.set_children(left, right)
            heap.heappush(node_list, new_node)
        root = node_list[0]

        code_lengths = {}
        self.write_code_lengths(root, 0, code_lengths)

        ordered_code_lengths = sorted(code_lengths.items(), key=itemgetter(1, 0)) 
        code_book_list = self.write_code_book(ordered_code_lengths)
        code_book_dict = {}

        for i in code_book_list:
            code_book_dict[i[0]] = bitarray(i[1])  

        output_can = self.code_book_output_canonical(code_book_list)
        output_trad = self.code_book_output_tradition(code_book_list)

        if len(output_can) > len(output_trad):
            code_book_output = "0" + format(len(output_trad), "011b") + output_trad
        else:
            code_book_output = "1" + output_can

        header_book_list = bitarray(code_book_output)
        book_add = header_book_list.buffer_info()[3]
        book_add_binary = format(book_add, "08b") 
        header_book_list = bitarray(bitarray(book_add_binary + "0" * book_add) + header_book_list)

        text_list = bitarray(endian="little")
        text_list.encode(code_book_dict, data) 
        text_add = text_list.buffer_info()[3]  
        text_add_binary = format(text_add, "08b")
        text_list = bitarray(bitarray(text_add_binary + "0" * text_add) + text_list) 

        return header_book_list, text_list


    def decode(self, data):

        code = ""
        for i in data:
            code += format(i, "08b")

        book_buffer = int(code[0:8], 2) + 8
        code = code[book_buffer:]

        binary_lengths = []
        ordered_codelengths = []
        book_format = code[0]
        code = code[1:]

        if book_format == "1":
            for i in range(0, 256):
                bit = code[0]
                code = code[1:]
                if bit == "1":
                    binary_lengths.append(code[0:6])
                    code = code[6:]
                else:
                    binary_lengths.append("0")

            lengths = []
            for code_length in binary_lengths:
                lengths.append(int(code_length, 2))

            for i in range(0, 255):
                if lengths[i] != 0:
                    ordered_codelengths.append((i + 1, lengths[i]))
        else:                
            code_book_length = int(code[:11], 2) + 11
            code_book_string = code[11:code_book_length]
            code = code[code_book_length:]
            while code_book_string:
                ordered_codelengths.append(
                    (int(code_book_string[:8], 2), int(code_book_string[8:12], 2)))
                code_book_string = code_book_string[12:]


        code_book_list = self.write_code_book(sorted(ordered_codelengths, key=itemgetter(1, 0)))
        code_book_dict = {}
        
        for i in code_book_list:
            code_book_dict[chr(i[0])] = bitarray(i[1])

        text_buffer = int(code[0:8], 2) + 8
        code = code[text_buffer:]
        text = bitarray(code)
        output_file = ''.join(text.decode(code_book_dict))


        return output_file