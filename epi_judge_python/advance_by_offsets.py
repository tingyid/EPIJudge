import sys
from typing import List

from test_framework import generic_test

# In a particular board game, a player has to try to advance through a sequence of positions. Each
# position has a nonnegative integer associated with it, representing the maximum you can advance
# from that position in one move. You begin at the first position, and win by getting to the last
# position. For example,let A = (3,3,1,0,2,0,1) represent the board game, i.e., the ith entry in A is
# the maximum we can advance from i. Then the game can be won by the following sequence of
# advances through A: take 1 step from A[0] to A[1], then 3 steps from A[1] to A[4], then 2 steps from
# A[4] to A[6],which is the last position. Note that A[0]=3>=1,A[1]=3>=3,and A[4]=2>=2,so all
# moves are valid. If A instead was (3,2,0,0,2,0,1), it would not possible to advance past position 3,
# so the game cannot be won.

# Write a program which takes an array of n integers, where A[i] denotes the maximum you can
# advance from index i, and returns whether it is possible to advance to the last index starting from
# the beginning of the array.

# brute-force: analyze each location starting from the beginning. 
# e.g. (3,3,1,0,2,0,1) => @i, try from 1:A[i], if any returns true stop & return immediate, otherwise keep trying. 
# O(n^2) for time and space

def can_reach_end_from(pos, A):
    # terminate if either reach the end
    if pos == len(A)-1: 
        return True
    elif A[pos] == 0: 
        return False

    # traverse the rest of the array
    max_from_cur_pos = A[pos]
    for step in range(1, max_from_cur_pos+1): 
        if can_reach_end_from(pos+step, A):
            return True
    return False
    
def can_reach_end_brute_force(A: List[int]) -> bool:
    return can_reach_end_from(0, A)

# optimize: greedy. 
#   iterate through the array keeping track of whether the furthest position we can reach so far is >= current position 
#   aka whether the current position is reachable, aka max(current position, furthest reached so far from any previous position)
#   furthest from a position i is i + A[i]; 
# if, for some i before the end of the array, i is the furthest, we cannot reach the end; otherwise we can. 
# e.g (3,3,1,0,2,0,1) => 0,3,4,4,4,6,6 >= last index, true
# e.g (3,2,0,0,2,0,1) => 0,3,3,3 => i = 4 > 3, false

def can_reach_end(A: List[int]) -> bool:
    furthest_reach_so_far = 0
    last_index = len(A)-1

    for i in range(len(A)): 
        if i > furthest_reach_so_far or furthest_reach_so_far >= last_index: 
            break
       
        furthest_reach_so_far = max(furthest_reach_so_far, i+A[i])
    
    return furthest_reach_so_far >= last_index
        
# if __name__ == '__main__':
#     exit(
#         generic_test.generic_test_main('advance_by_offsets.py',
#                                        'advance_by_offsets.tsv',
#                                        can_reach_end))


# Variant: Write a program to compute the minimum number of steps needed to advance to the last
# location.
# brute-force with recursion: try all possible steps <= max distance, choose the minimum. O(N^N) TC, O(1) SC
def min_steps_to_reach_end_brute_force(A: List[int], cur_pos: int) -> int:
    # terminate if reached the end
    if cur_pos == len(A) - 1: 
        return 0
    
    max_from_cur_pos = A[cur_pos]
    min_steps = sys.maxsize # or 9999999
    for step in reversed(range(1, max_from_cur_pos+1)): 
        min_steps = min(min_steps, 1 + min_steps_to_reach_end_brute_force(A, cur_pos + step))
        
    return min_steps

def min_steps_to_reach_end(A: List[int]) -> int: 
    min_steps = min_steps_to_reach_end_brute_force(A, 0)
    
    # not able to reach the end
    if min_steps > len(A):
        return -1
    return min_steps

# print(min_steps_to_reach_end([0,0]))
# print(min_steps_to_reach_end([3,2,1,0,2,0,1]))
# print(min_steps_to_reach_end([3,3,1,0,2,0,1]))

# optimize 1: memoization O(N^2) TC, O(1) SC
# https://www.youtube.com/watch?v=cETfFsSTGJI
# min jump to reach i from a previous position

def min_steps_to_reach_end_2(A: List[int]) -> int: 
    min_steps = [9999999999] * len(A)
    min_steps[0] = 0
    pos_of_jumps = [-1] * len(A)
    pos_of_jumps[0] = -1

    for i in range(1, len(A)): 
        for j in range(i): 
            if j + A[j] >= i: 
                min_steps[i] = min(min_steps[i], min_steps[j] + 1)
                pos_of_jumps[i] = j
    # print(min_steps)
    # print(pos_of_jumps)

    return min_steps[len(min_steps)-1]

# print(min_steps_to_reach_end_2([3,3,1,0,2,0,1]))

# optimize 2: greedy with moving boundary. 
# it was observed that if we are at position i, the maximum one can jump is (i,  i + nums[i])

# Consider three variables, jumps, which stores the number of jumps, end, which denotes the end of the array and 
# farthest denoting the farthest one can jump and initialise them to 0.
# Traverse over the given array and perform the following operation:
# farthest = i + nums[i]
# If end is reached, then ith jump is finished, therefore update end = farthest.
# Return total jumps.
# TC O(N), where N is the total elements in the array. SC O(1)
def min_steps_to_reach_end_3(A: List[int]) -> int: 
    jumps = 0
    curr_jump_end = 0
    farthest = 0
    last_index = len(A) - 1 

    for i in range(last_index):
        farthest = max(farthest, i + A[i])
        if i == curr_jump_end:
            jumps += 1
            if farthest <= curr_jump_end: 
                return -1
            curr_jump_end = farthest
            
    return jumps
        
print(min_steps_to_reach_end_3([3,3,1,0,2,0,1]))
print(min_steps_to_reach_end_3([3,2,1,0,2,0,1]))