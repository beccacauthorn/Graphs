from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


def bfs(original_room, explored_rooms):
    # Create an empty queue
    q = Queue()
    # Init: enqueue the starting node
    q.enqueue((original_room, []))
    # Create a set to store visited nodes
    visited = set()

    # While the queue isn't empty
    while q.size() > 0:
        # Dequeue the first item
        pair = q.dequeue()
        currentNode = pair[0]
        path_currentNode = pair[1]

        if currentNode.id not in explored_rooms:
            return path_currentNode

        # If it's not been visited:
        if currentNode not in visited:
            # Do something with the node
            # Add all neighbors to the queue
            visited.add(currentNode)

            # Add all neighbors to the queue
            for direction in currentNode.get_exits():
                new_room = currentNode.get_room_in_direction(direction)
                pathto_neighbor = path_currentNode + [direction]
                q.enqueue((new_room, pathto_neighbor))

    return None


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
alreadyvisited = {}
movementOptions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# save current room as visited as a key, 
# with each possible exit direction as values 
#alreadyvisited[player.current_room.id] = player.current_room.get_exits()


#looping through until every room has been explored
while len(alreadyvisited) < len(room_graph):
    #if room has not been visited, save it to alreadyvisited, check
    #which direction you came from and where you can move to
    if player.current_room.id not in alreadyvisited:
        #save current room in alreadyvisited 
        alreadyvisited[player.current_room.id] = player.current_room.get_exits()

    # look at all possible directions
    next_direction = None
    for direction in player.current_room.get_exits():
        if player.current_room.get_room_in_direction(direction).id not in alreadyvisited:
            # choose one that has not been visited
            next_direction = direction
            break

    if next_direction is None:
        print('did not find a new direction')
        # need to search for the closest unexplored room
        path = bfs(player.current_room, alreadyvisited)
        # and move there, which may involve manuy steps
        if path is not None:
            for step in path:
                traversal_path.append(step)
                player.travel(step)
        else:
            print('all rooms have been visited')

    else:
        # move to the found direction
        print('moving to {}'.format(next_direction))
        traversal_path.append(next_direction)
        player.travel(next_direction)


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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
