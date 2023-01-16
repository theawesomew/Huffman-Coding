from os import sys, path
import argparse
import pickle

class Node ():

    # every node has a frequency, not every node has a character
    def __init__ (self, frequency, character=None):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None
        self.parent = None

    def addLeft (self, node):
        self.left = node
        node.parent = self

    def addRight (self, node):
        self.right = node
        node.parent = self

    def __lt__ (self, node):
        return self.frequency < node.frequency

    def __gt__ (self, node):
        return self.frequency > node.frequency

    def __eq__ (self, node):
        return self.frequency == node.frequency

    def __lte__ (self, node):
        return self.frequency <= node.frequency

    def __gte__ (self, node):
        return self.frequency >= node.frequency

    def __add__ (self, node):
        newNode = Node(self.frequency + node.frequency)
        if self.frequency <= node.frequency:
            newNode.addLeft(self)
            newNode.addRight(node)
        else:
            newNode.addLeft(node)
            newNode.addRight(self)

        return newNode

    def __repr__ (self):
        return f"({self.character}, {self.frequency})"

def label (node, current, encoding):
    if (node.left is None) and (node.right is None):
        encoding[node.character] = current
    else:
        current += '0'
        label(node.left, current, encoding)
        current = current[:-1]
        current += '1'
        label(node.right, current, encoding)
        current = current[:-1]

def decompress (filename):
    with open(filename, 'rb') as f:
        length = int.from_bytes(f.read(4), byteorder='big')
        encoding = pickle.loads(f.read(length))

        s = ''

        values = bin(int.from_bytes(f.read(), byteorder='big'))
        current = encoding
        i = 0
        while i < len(values[2:]):
            if (current.left is None) and (current.right is None):
                s += current.character
                current = encoding
                continue
            elif values[2:][i] == '0':
                current = current.left
            else:
                current = current.right

            i += 1

        print(s)

        

def compress (filename):
    with open(filename, 'r') as f:
        freq = {}

        for ch in (data := f.read()):
            if ch not in freq:
                freq[ch] = 1
            else:
                freq[ch] += 1

        q = []

        for (character, frequency) in freq.items():
            q.append(Node(frequency, character))

        q = sorted(q)

        while len(q) > 1:
            n = q[0] + q[1]
            q = q[2:]
            q.append(n)
            q = sorted(q)

        encoding = {}

        label(q[0], '', encoding)

        with open(f'{filename.split(".")[0]}.comp', 'wb') as comp:
            b = ''
            for ch in data:
                b += encoding[ch]
            
            serialized_encoding = pickle.dumps(q[0])

            comp.write(len(serialized_encoding).to_bytes(4, byteorder='big'))
            comp.write(serialized_encoding)
            comp.write(int(b, 2).to_bytes((len(b) + 7) // 8, byteorder='big'))

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('--compress', dest='compress', action='store_true', default=True, required=False) 
parser.add_argument('--decompress', dest='decompress', action='store_true', default=False, required=False)
arguments = parser.parse_args()

if arguments.decompress:
    decompress(arguments.filename)
else:
    compress(arguments.filename)
