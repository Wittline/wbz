class FileHandler:

    def __init__(self, path):
        self.path = path

    def read(self):
            """This method is used to read the contents of the file into a python
            string.
            Returns
            -------
            str
                The contents of the file, i.e. the sequence.
            """
            seq = ""
            with open(self.path, 'r') as file:
                for line in file:
                    seq += line.strip("\n")
            return seq

    def read_bytes(self):
        """This method is used to read a file that has been written in bytes,
        it will be useful when reading files that has been compressed with
        Huffman coding.
        Returns
        -------
        str
            The contents of the file, i.e. the sequence.
        """
        seq = ""
        with open(self.path, 'rb') as file:
            for line in file:
                seq += line.decode("utf-8")
        return seq

    def write(self, content):
        """This method is used to write out to a file.
        Parameters
        ----------
        content : str
            The contents of the file.
        Returns
        -------
        None
            Writes out to a new file.
        """
        with open(self.path, 'w') as file:
            file.writelines(content)

    def write_bytes(self, content):
        """This method is used to write out to a new file into a bytes format,
        UTF-8 encoding, useful when we want to write out the contents of the
        Huffman compression to a file.
        Parameters
        ----------
        content : str
            The contents of the file.
        Returns
        -------
        None
            Writes out to a new file in a bytes format.
        """
        with open(self.path, 'wb') as file:
            file.write(content.encode("utf-8"))