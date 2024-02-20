import heapq

from log_message import log_message


def dijkstra(server_id, destination_id, relationships_items):
    graph = convert_relationships_to_graph(relationships_items)
    source = "pc" + str(server_id)
    destination = "pc" + str(destination_id)

    queue = [(0, source)]
    visited = {source: (0, None)}

    while queue:
        (cost, current_node) = heapq.heappop(queue)

        if current_node == destination:
            path = [destination]
            while current_node != source:
                (cost, current_node) = visited[current_node]
                path.append(current_node)
            path.reverse()

            return [int(node[2:]) for node in path]

        for neighbor, weight in graph.get(current_node, {}).items():
            new_cost = cost + weight
            if neighbor not in visited or new_cost < visited[neighbor][0]:
                heapq.heappush(queue, (new_cost, neighbor))
                visited[neighbor] = (new_cost, current_node)

    return None


def convert_relationships_to_graph(relationships_items):
    new_graph = {}
    for server_id, neighbors in relationships_items:

        server_key = "pc" + str(server_id)
        new_graph[server_key] = {}
        for neighbor in neighbors:
            neighbor_key = "pc" + str(neighbor)

            new_graph[server_key][neighbor_key] = 1
    return new_graph


def get_graph_path(server_id, from_node, relationships_items):
    path = dijkstra(server_id, from_node, relationships_items)

    if server_id in path:
        path.remove(server_id)

    log_message(f"[Dijsktra] Path from {server_id} to {from_node}: {path}", server_id)

    return path
