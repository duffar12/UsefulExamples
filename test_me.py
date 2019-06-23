
from unittest import mock
from unittest.mock import patch

def run_test():
    mockMyClass = MyClass()
    for i in range(2):
        print(mockMyClass.response)

class MyClass():
    def __init__(self):
        self.response = Prop()

def get_response(x):
    for i in x:
        yield i

r = get_response([10,20])

def test_stuff():
    with mock.patch.object(MyClass, 'response', 1, create=True):
        run_test()
    assert False

class Prop(object):




