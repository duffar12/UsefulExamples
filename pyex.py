import math
from collections import deque


class Trie(object):
    def __init__(self):
        self.root = Node(None)

    def add_word(self, word):
        node =  self.root
        for i in range(len(word)):
            next_node = None
            for n in node.children:
                if n.text == word[i]:
                    next_node =  n
                    break
            if not next_node:
                last = Node('*')
                for j in range(len(word)-1, i, -1):
                    next_node = Node(word[j])
                    next_node.add_child(last)
                    last = next_node
                node.add_child(last)
            else:
                node = next_node





class Node(object):

    def __init__(self, text):
        self.text = text
        self.children = []

    def add_child(self, child):
        self.children.append(child)




M = ['HOOL'
    ,'UPKN'
    ,'OERO']

w1 = Node('H')
w1.add_child('O')

