from util import Stack, Queue

def parents(ancestors, node):
    # return a list of parents of node
    result = []

    # loop through ancestors and look for those pairs where 
    # node is the second element and add the first element to result
    for pair in ancestors:
        if pair[1] == node:
            result.append(pair[0])

    return result


def earliest_ancestor(ancestors, starting_node):
    queue = Queue()
    queue.enqueue([starting_node])
    full_paths = []

    while queue.size() > 0:
        cur_path = queue.dequeue()

        # create all possible paths that extend cur_path
        # by interating over the parents of the last element in the cur_path
        all_parents = parents(ancestors, cur_path[-1])

        if len(all_parents) == 0 and cur_path == [starting_node]:
            return -1

        if len(all_parents) > 0:
            for parent in all_parents:
                # enqueue each of them
                new_path = cur_path + [parent]
                queue.enqueue(new_path)
        else:
            # if we cannot extend the cur_path, add cur_path to full_paths
            full_paths.append(cur_path)

    # take the longest path in full_paths
    cur_max = []
    for path in full_paths:
        if len(path) > len(cur_max):
            cur_max = path
        elif len(path) == len(cur_max):
            if path[-1] < cur_max[-1]:
                cur_max = path

    # return the last element
    return cur_max[-1]
