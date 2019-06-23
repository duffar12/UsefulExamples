import asyncio
import bisect
from collections import deque



class LinkedList(object):

    def __init__(self, data):

        self.start = Link(None, None, data[0])
        prev = self.start
        for i in range(1,len(data)):
            nxt = Link(prev, None, data[i])
            prev.set_right(nxt)
            prev = nxt
        self.end = nxt

    def get_index(self, index):
        nxt = self.start
        for i in range(index-1):
            nxt = nxt.right
        return nxt

    def insert(self, idx, new_link):
        link = self.get_index(idx)
        new_link.set_left(link.left)
        link.set_left(new_link)
        new_link.set_right(link)

    def remove(self, idx):
        link = self.get_index(idx)
        if not link.start:
            link.left.set_right(link.right)
        if not link.end:
            link.right.set_left(link.left)

    def get_next(self):
        nxt = self.start
        while True:
            yield nxt
            if nxt.end:
                break
            nxt = nxt.right


class Link(object):

    def __init__(self, left, right, data=None):
        self.data = data
        self.left = left
        self.right = right
        self.end = False
        self.start = False
        if right == None:
            self.end = True
        if left == None:
            self.start = True

    def set_left(self, left):
        self.left = left
        self.start = False

    def set_right(self, right):
        self.right = right
        self.end = False



if __name__ == '__main__':
    ll = LinkedList([1,2,3,4])

    for nxt in ll.get_next():
        print(nxt.data)


