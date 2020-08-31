from room import Room
from player import Player
from util import Stack
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# append the first rooms to get possible exits
# then loop for as long as as len(stack) > 0
# append the first direction prioritizing n
# create a dict of all visited rooms
#  n, s, w, and  e.
# array which is a stack and holds the directions we take and pops off to go backwards.

# track return path to last room that still has unexplored exits
# returnPath = Stack()

# a function that makes the path the opposite direction
# def rev_dir(direction):
#     if direction == "n":
#         return "s"
#     if direction == "s":
#         return "n"
#     if direction == "w":
#         return "e"
#     if direction == "e":
#         return "w"

# changing format a bit, keeping above just in case

# makes paths the reverse direction
rev_dir = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

#  rooms visited + first room in dict with the list of exits
current_path = player.current_room
# graph to traverse through exits and graph to match this format:
# {
#   0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
# }
traversal_graph = {current_path.id: {i: '?' for i in current_path.get_exits()}}
# to track backtracking
backtracking = []

# length of visited rooms < than the number of rooms in the graph
while len(traversal_graph) < len(room_graph):

    # if current_room is not in graph, change to '?'
    if current_path.id not in traversal_graph:
        traversal_graph = {current_path.id: {i: '?' for i in current_path.get_exits()}}

    if '?' not in traversal_graph[current_path.id].values():
        #  grab from backtrack and assign to next
        next_path = current_path.get_room_in_direction(backtracking[-1])

        # next path is not in graph, then repeat as above: change to '?'
        if next_path.id not in traversal_graph:
            traversal_graph = {next_path.id: {i: '?' for i in next_path.get_exits()}}

        traversal_path.append(backtracking[-1])
        # remove from backtrack
        backtracking = backtracking[:-1]
        # reset the path
        current_path = next_path

    else:

        for move in traversal_graph[current_path.id]:

            # if '?' then we'll move into that direction
            if traversal_graph[current_path.id][move] == '?':
                # assign that path to the assigned path to the direction
                next_path = current_path.get_room_in_direction(move)

                # if next path is not in graph
                if next_path.id not in traversal_graph:
                    # assign the value to that direction
                    traversal_graph[next_path.id] = {i: '?' for i in next_path.get_exits()}

                # assign current to next
                traversal_graph[current_path.id][move] = next_path.id
                # assign that move to the current
                traversal_graph[next_path.id][rev_dir[move]] = current_path.id
                # reset the path
                current_path = next_path
                # append the move to the main path
                traversal_path.append(move)
                # append the backtracking
                backtracking.append(rev_dir[move])

                # stop the loop
                break

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
