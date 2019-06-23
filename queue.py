

class Queue(object):



    def __init__(self):
        self.first = None
        self.last = None


    def pop(self):
        first = self.first
        if first:
            self.first = self.first.right
            return first.data
        return None

    def add(self, element):
        if self.first is None:
            self.first = element
            self.last = element

        self.last.right = element
        self.last = element



class element(object):

    def __init__(self, data):
        self.data = data
        self.right = None



if __name__ == '__main__':

    q = Queue()
    for i in range(5):
        q.add(element(i))

    for i in range(6):
        print(q.pop())
