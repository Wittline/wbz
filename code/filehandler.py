import os

class FileHandler:

    def __init__(self, path):
        self.path = path
        self.output_file =  os.path.splitext(self.path)[0] + '_compressed.txt'

    def read(self):

            seq = ""
            with open(self.path, 'r', encoding='utf-8' ) as file:
                for line in file:
                    seq += line.strip("\n")
            return seq

    def read_bytes(self):

        seq = ""
        with open(self.output_file, 'rb') as file:
            for line in file:
                seq += line.decode("utf-8")
        return seq

    def write(self, content):
        with open(self.path, 'w') as file:
            file.writelines(content)

    def write_bytes(self, content):
        with open(self.output_file, 'wb') as file:
            file.write(content.encode("utf-8"))