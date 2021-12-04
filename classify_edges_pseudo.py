def classify_edges(start_node, discovered, finished, back_edges):
    discovered.append(start_node)
    reversed = False

    for edge in out_edges(start_node):
        successor = target(edge)
        if successor not in discovered:
            back_edges[edge] = False
            reversed = classify_edges(successor, discovered, finished, back_edges)
            if reversed:
                back_edges[edge] = True
                if len(out_edges(start_node)) > 1:
                    reversed = False
        elif successor not in finished:
            back_edges[edge] = True
            reversed = True
        else:
            back_edges[edge] = False
    finished.append(start_node)
    return reversed

# nie zapomnij zmienic liste back_edges na np. mapę true/false
