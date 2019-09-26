# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 17:18:50 2018

@author: stojk
"""

import random
import sys
import time
import mysql.connector

cnx = mysql.connector.connect(user='root', password='matija',
                              host='localhost',
                              database='mydb')
cursor = cnx.cursor()
"""
# definition of my network with a dictionary. Each key has its adjecent nodes listed
net = {										
	'A': ['B','D'],
	'B': ['A','C','E'],
	'C': ['B','F'],
	'D': ['A','E','G'],
	'E': ['B','D','F','H'],
	'F': ['C','E','I'],
	'G': ['D','H','J'],
	'H': ['E','G','I','K'],
	'I': ['F','H','L'],
	'J': ['G','K','M'],
	'K': ['H','J','L','N'],
	'L': ['I','K','O'],
	'M': ['J','N'],
	'N': ['K','M','O'],
	'O': ['L','N'],
}
# list of jamed path
jamed = []
"""
# finds shortest path between 2 nodes of a graph using BFS
def bfs_shortest_path(start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = your_choices(node)
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path
 
            # mark node as explored
            explored.append(node)
 
    # in case there's no path between the 2 nodes
    print ("Oh snap, a connecting path does not exist :(")
    sys.exit() 
    # stop the script most paths have been jamed
"""
def your_choices2(curr): 
	choices = list(net[curr])
	for j in jamed:
		if (j[0] == curr):
			if (j[1] in choices):
				choices.remove(j[1])
		if (j[1] == curr):
			if (j[0] in choices):
				choices.remove(j[0])
	if not choices:
		print ("Oh snap, jams all around me!")
		sys.exit()
		# stop the script, all the paths from our node are jamed
	return choices
"""
# lists all neighbours for a given node that are possible to get to (no jams in that road)
def your_choices(curr):
    query = "SELECT Susjedi FROM nova WHERE idCvora='{}'".format(curr)
    cursor.execute(query)
    
    choices = cursor.fetchone()
    print (choices)
    choices = ''.join(choices)
    choices = choices.split(",")
    
    if not choices:
       cursor.close()
       cnx.close() 
       print ("Oh snap, jams all around me!")
       sys.exit()
		# stop the script, all the paths from our node are jamed
    return choices 

# gives our next node at random from neighbours
def next_step(prev, curr):
	choices = your_choices(curr)
	return random.choice(choices)

# gives a random number in range [0,999]. If the number is smaller than a 100 the road is jamed
def jam_chance():
	return random.randint(0,999)

# find an alternate path for the car that wants to go from curr node to nxt but the road is blocked
def alternate_path(prev, curr, nxt):
	print ("Jam between " + curr + " and " + nxt)
	choices = your_choices(curr)
	if (nxt in choices):
		choices.remove(nxt)
	time.sleep(2)
	pth = bfs_shortest_path(curr, nxt)
	for i in pth:
		print (i)
		time.sleep(2)
	return pth[-2], pth[-1]
	cursor.close()
	cnx.close()
	print ("Could not find a route :(")
	sys.exit()
    
def remove_from_db(curr, nxt):
    query = "SELECT Susjedi FROM nova WHERE idCvora='{}';".format(curr)
    cursor.execute(query)

    res = cursor.fetchone()
    res = ''.join(res)
    res = res.split(',')
    
    res.remove(nxt)
    res = ','.join(res)
    
    query = "UPDATE mydb.nova SET Susjedi='{}' WHERE idCvora='{}';".format(res,curr)
    cursor.execute(query)
    cnx.commit()

start = 'A'
current = start
previous = start


print (start)

while (1):
	next = next_step(previous, current)
	if (jam_chance() > 100):
		previous = current
		current = next
		print (current)
	else:
		remove_from_db(current, next)
		previous, current = alternate_path(previous, current, next)
	time.sleep(2)
