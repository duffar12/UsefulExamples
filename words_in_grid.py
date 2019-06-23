words = {'hook', 'hope', 'shoe', 'hoe', 'hop'}
grid = ['hop', 'hoe', 'skx']

def check_if_word(so_far):
    if so_far in words:
        print(so_far, ' word found')


def find(idx1, idx2, so_far, visited_idxs):
    if (idx1, idx2) in visited_idxs:
        return
    visited_idxs.add((idx1,idx2))
    so_far = so_far + grid[idx1][idx2]
    check_if_word(so_far)

    if idx1 +1 < 3:
        find(idx1 +1, idx2, so_far, visited_idxs=set(idx for idx in visited_idxs) )
    if idx2 +1 < 3:
        find(idx1, idx2+1, so_far, visited_idxs =set(idx for idx in visited_idxs))
    if idx1 -1 >0:
        find(idx1 -1, idx2, so_far, visited_idxs =set(idx for idx in visited_idxs))
    if idx2 -1 >0:
        find(idx1, idx2-1, so_far, visited_idxs =set(idx for idx in visited_idxs))



for i, w in enumerate(grid):
    for j, l in enumerate(w):
        find(i,j,'', set())

