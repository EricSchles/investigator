def generate_connected_graph(list_of_keys):
    graph = {}.fromkeys(list_of_keys,[])
    seen_keys = []
    for index,key in enumerate(list_of_keys):
        if index != len(list_of_keys) - 1:
            graph[key] = list_of_keys[index+1:]
    return graph



