
from queue import Queue

def coro1():
    for i in range(3):
        yield i

def coro2():
    for i in range(3):
        x = yield
        print('coro2',x)

def coro(cro):
     yield from cro



class Task():
    task_id = 0
    def __init__(self, target):
        Task.task_id += 1
        self.task_id = Task.task_id
        self.target = target

    def run(self):
        self.target.send('x')

class Scheduler():

    def __init__(self):
        self.ready = Queue()
        self.task_map = dict()

    def add_new_task(self, target):
        task = Task(target)
        target.send(None)
        self.task_map[task.task_id] = task
        self.schedule(task)
        return task.task_id

    def schedule(self,task):
        self.ready.put(task)

    def exit(self, task):
        del self.task_map[task.task_id]

    def mainloop(self):
         while self.task_map:
             try:
                 task = self.ready.get()
                 result = task.run()
                 self.schedule(task)
             except StopIteration:
                 self.exit(task)
                 continue
             self.schedule(task)

if __name__ == '__main__':

    s = Scheduler()
    s.add_new_task(coro(coro1()))

    s.mainloop()
    c = coro(coro1())
    c.send(None)
    i = c.send('x')
    print(i)
    i = c.send('x')
    print(i)


