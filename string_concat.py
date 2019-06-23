import time


# String is immutable. So when you add two strings together python needs to create a whole new copy of theh string in a
# new buffer.  If you add multiple strings together it makes new copies at every step. each step is an O(N) operation
# if the string is large this takes a long time

# Using join, python just calculates the size of buffer needed and then copies every thing in at once. Much more efficient

x = 'a'


now = int(time.time() *1000)
for i in range(100000):
    x = x + 'a' + 'a' + 'a'
finish = int(time.time() *1000)
print('+ took {} ms'.format(finish - now))

x = ['a']

now = int(time.time() *1000)
for i in range(100000):
    x.append('a')
    x.append('a')
    x.append('a')

'.'.join(x)
finish = int(time.time() *1000)
print('join took {} ms'.format(finish - now))



