# content of conftest.py
from test_foocompare import Foo
import pandas as pd
def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return ['Comparing Foo instances:',
                '   vals: %s != %s' % (left.val, right.val)]
