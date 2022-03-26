import os

class FileHandler:

    def __init__(self):
        pass

    def read(self, filename):

            seq = None
            with open(filename, 'r') as file:
                seq = file.read()
            return seq

    def read_bytes(self, filename):

        data = None
        with open(filename, 'rb') as file:
                data = file.read()
        return data

    def write(self, content, filename):
        with open(filename, 'w') as file:
            file.writelines(content)

    def write_bytes(self, output, filename):
        with open(filename, 'wb') as file:
            file.write(output)

