#!/usr/bin/python3.6
#
# HW1: Pancake Sort
# Remmy Chen 09/26/2018
#
# TO RUN: python3 pancake-astar.py and there will be some
# questions before the pancake sort will be run. There are
# two options: manually inputted or pseudo-randomly generated 
# pancake stack. To run the sort on pseudo-randomly generated
# pancake stacks x times, manually change the value assigned
# to numRuns in main().
#
# The pancake sort is a sorting problem whereby a disordered
# stack of n differently-sized pancakes (sizes from 1 to n) 
# must be sorted with a spatula such that the largest is at 
# the bottom and the smallest is at the top [n,  ... , 1]. 
# Array[0] is the bottom of the pancake stack.
#
# The only operation that may be performed is flipping all 
# the pancakes above the spatula that is inserted into the stack. 
#
# The pancake sort may be defined as a searching problem where 
# the initial state is a disordered stack of pancakes and the 
# final state is an ordered stack of pancakes [n, ... , 1]. 
# Each node is represented by a tuple of (total cost, candidate 
# solution), and nodes may be added to the priority queue that 
# is represented by a heap and sorted by total cost. For a 
# stack of 5 pancakes, 4 nodes exist for each parent node, the 4
#  nodes differing from the parent node by a 2-pancake flip, a 
# 3-pancake flip, a 4-pancake flip, or a 5 pancake flip. The node 
# with the least total cost will be chosen at each step and the 
# solution will have a total cost of 0.
#
# A possible cost function (backward cost) would be the sum of 
# gaps in size between pancakes, where n is the pancake stack:
#
#       g(n) = sum( | n[i] - n[i + 1] | - 1 ) 
# 
# For example, a pancake stack of [2 1 5 3 4] would have a 
# backward cost of sum( [0, 3, 1, 0] ) = 8. 
#
# A possible heuristic function (forward cost) would be the sum
# of costs where if the gap in size between pancakes > 1, the 
# cost = 1, and otherwise the cost = 0:
# 
# 	h(n) = sum( x[i] ) where:
#
#       if | n[i] - n[i + 1] | > 1, 
#		x[i] = 1
#	if | n[i] - n[i + 1] | <= 1,
#		x[i] = 0
#
# The total cost t(n) = g(n) + h(n). When a pancake stack state has
# reached the goal state, t(n) = 0. A comparison of a pancake stack
# state against the goal state ensures that the sorting doesn't stop
# at [1, ... , n] which is also t(n) = 0 and instead stops at
# [n, ... , 1].

import sys
import copy
import heapq
from random import randint
from operator import add

# given a list of integers representing the initial pancake stack and
# given an integer representing the number of pancakes in the pancake
# stack, perform A* search algorithm to sort pancakes to the goal 
# state of [n, ... , 1]
def pancakeSort(initialStack, numPancakes):
	solution = sorted(list(range(1, numPancakes + 1)), key=int, reverse=True)
	print("\ngoal state:\n%s" % solution)
	numFlips = 0
	pqueue = []
	visited = []
	heapq.heappush(pqueue, createNode(initialStack))
	heapq.heappush(visited, createNode(initialStack))
	print("\nnode in heap at initial state:\n%s" % pqueue)
	while True:
		if len(pqueue) == 0:
			break 	
		node = heapq.heappop(pqueue)
		print("\nnode chosen: %s" % node[1])
		if node[1] == solution:
			break
		for i in range(2, (numPancakes + 1)):
			nodex = createNode(flipPancakes(list.copy(node[1]), i, numPancakes))
			j, tc = nodeExists(pqueue, nodex)
			k, tc2 = nodeExists(visited, nodex)
			if tc < 0 and tc2 < 0: 
				heapq.heappush(pqueue, tuple(nodex))
				heapq.heappush(visited, tuple(nodex))
			elif tc > nodex[0]: 
				lst = list(tuple(pqueue[j]))
				lst[0] = nodex[0]
				pqueue[j] = tuple(lst)
		numFlips += 1
		print("\nnodes in heap after %d flips:" % numFlips)
		for j in range(0, len(pqueue)):
			print(pqueue[j], end='\n')
	return numFlips

# given a heap and a node, check if node exists. if node
# exists, return an int that represents the node's location
# in the heap and an int that represents the total cost of
# the node. otherwise, return -1.
def nodeExists(heap, node):
	for j in range(0, len(heap)):
		if node[1] == heap[j][1]:
			return j, heap[j][0]
	return -1, -1

# the node is a tuple of (totalCost, candidateSolution), 
# where totalCost is an int and candidateSolution is a list
# representing a pancake stack. given a list that represents
# a pancake stack, calculate the total cost of the stack, 
# create node, and return it. 
def createNode(stack):
	tc = totalCost(stack)
	node = (tc, stack)
	#print(node, end='\n') 
	return node

# given a list representing a pancake stack, return the total
# cost of the stack.
def totalCost(stack):
	tc = [i + j for i, j in zip(backwardCost(stack), forwardCost(stack))]
	#print(tc, end='\n')
	tcSum = sum(tc)
	#print(tcSum, end='\n')
	return tcSum

# given a list representing a pancake stack, return the 
# backward cost of the stack.
def backwardCost(stack):
	bc = []
	gap = 0
	for i in range(0, len(stack) - 1):
		gap = abs(stack[i] - stack[i + 1]) - 1
		bc.append(gap)
	return bc

# given a list representing a pancake stack, return the
# forward cost of the stack.
def forwardCost(stack):
	fc = []
	gap = 0
	cost = 0
	for i in range(0, len(stack) - 1):
		gap = abs(stack[i] - stack[i + 1])
		if gap > 1:
			cost = 1
		else:
			cost = 0 
		fc.append(cost)
	return fc

# given a list representing a pancake stack, and two ints,
# reverse stack[i...(numPancakes - 1)]
def flipPancakes(stack, i, numPancakes):
	j = numPancakes - 1
	k = i
	index = abs(numPancakes - i)
	tmp = 0
	while k // 2 != 0:
		tmp = stack[index]
		stack[index] = stack[j]
		stack[j] = tmp
		index += 1
		j -= 1
		k = (k + 1) / 2
	#print("flipped %s" % stack)
	return stack

# given an int representing the number of pancakes in a stack,
# return a psuedo-randomly generated stack of i pancakes
def createPancakeStack(i):
	stack = []
	while len(stack) != i:
		j = randint(1, i)
		if not j in stack:
			stack.append(j)	
	return stack


def main():
	numFlips = 0
	numRuns = 1
	try:
		numPancakes=int(input('Hi, how many pancakes would you like in your stack?\n'))
		stackOption=int(input('\nWould you like to input your own pancake stack or get a pseudo-randomly generated pancake stack?\nInput 0 to create your own, 1 to get a generated stack.\n'))
		if stackOption == 0:
			initVals=input('\nPlease enter your pancake values, with square brackets and commas excluded.\nValues should be in the range of 1 to %d (inclusive) and each value should only appear once.\nValues will not be checked, so use at your own risk.\n' % numPancakes)
			initialStack=list(map(int, initVals.split()))
			print('\nThanks. Pancake sorting will now begin.\n')
			if numPancakes == len(initialStack):
				numFlips += pancakeSort(initialStack, len(initialStack))
				print("\n%d flips were used to sort pancake stack %s" % ((numFlips / numRuns), initialStack))
			else:
				print("Error")
		elif stackOption == 1:
			print('\nThanks. Pancake sorting will now begin.\n')
			for i in range(0, numRuns):
				initialStack = createPancakeStack(numPancakes)
				numFlips += pancakeSort(initialStack, len(initialStack))
				print("\n%d flips were used to sort pancake stack %s" % ((numFlips / numRuns), initialStack))
		else:
			print("Error")
	except:
    		print("Error")
	print("\n%.2f flips on average were used to sort pancakes, based on %d runs" % ((numFlips / numRuns), numRuns))


if __name__ == "__main__":
	main()
