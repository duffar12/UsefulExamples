

class Stack(object):

    def __init__(self):
        self.last = None

    def push(self, data):
        if self.last:
             data.left = self.last
        self.last = data

    def pop(self):
        if self.last:
            last = self.last
            self.last = last.left

        return last.data


class element(object):

    def __init__(self, data):
        self.data = data
        self.left = None



if __name__ == '__main__':

    s = Stack()

    for i in range(6):
        s.push(element(i))

    for i in range(6):
        print(s.pop())

