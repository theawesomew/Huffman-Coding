from os import sys, path

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


with open(sys.argv[1], 'r') as f:
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

    with open('test.comp', 'wb') as comp:
        b = ''
        for ch in data:
            b += encoding[ch]

        comp.write(int(b, 2).to_bytes((len(b) + 7) // 8, byteorder='big'))
