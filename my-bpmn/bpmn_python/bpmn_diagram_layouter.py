# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""
import copy

import bpmn_python.bpmn_python_consts as consts
import bpmn_python.grid_cell_class as cell_class


def generate_layout(bpmn_graph, symmetric=True):
    """
    :param bpmn_graph: an instance of BPMNDiagramGraph class.
    """

    classification = generate_elements_clasification(bpmn_graph)

    nodes_copy_reversed = copy.deepcopy(classification[0])
    flows_copy_reversed = copy.deepcopy(bpmn_graph.sequence_flows)

    start_nodes = []
    for node in classification[0]:
        if "Start Event" in node['classification']:
            start_nodes.append(node)

    back_edges_ids = []

    reversed_anything = True
    while reversed_anything:
        discovered = []
        finished = []
        iteration_back_edges_ids = []
        for start_node in start_nodes:
            classify_edges(start_node, flows_copy_reversed, nodes_copy_reversed, discovered,
                        finished, iteration_back_edges_ids)
        reverse_flows(flows_copy_reversed, nodes_copy_reversed, iteration_back_edges_ids)
        if iteration_back_edges_ids:
            reversed_anything = True
            back_edges_ids += iteration_back_edges_ids
        else:
            reversed_anything = False

    (sorted_nodes_with_classification) = topological_sort(
        flows_copy_reversed, nodes_copy_reversed)

    grid = grid_layout(flows_copy_reversed,
                       sorted_nodes_with_classification, symmetric)
    # interleave(grid)

    set_coordinates_for_nodes(bpmn_graph, grid)
    set_flows_waypoints(bpmn_graph, back_edges_ids,
                        sorted_nodes_with_classification)


def generate_elements_clasification(bpmn_graph):
    """
    :param bpmn_graph:
    :return:
    """
    nodes_classification = []
    node_param_name = "node"
    flow_param_name = "flow"
    classification_param_name = "classification"

    classification_element = "Element"
    classification_boundary = "Boundary"
    classification_join = "Join"
    classification_split = "Split"
    classification_start_event = "Start Event"
    classification_end_event = "End Event"

    task_list = bpmn_graph.get_nodes(consts.Consts.task)
    for element in task_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    subprocess_list = bpmn_graph.get_nodes(consts.Consts.subprocess)
    for element in subprocess_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    complex_gateway_list = bpmn_graph.get_nodes(consts.Consts.complex_gateway)
    for element in complex_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    event_based_gateway_list = bpmn_graph.get_nodes(
        consts.Consts.event_based_gateway)
    for element in event_based_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    inclusive_gateway_list = bpmn_graph.get_nodes(
        consts.Consts.inclusive_gateway)
    for element in inclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    exclusive_gateway_list = bpmn_graph.get_nodes(
        consts.Consts.exclusive_gateway)
    for element in exclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    parallel_gateway_list = bpmn_graph.get_nodes(
        consts.Consts.parallel_gateway)
    for element in parallel_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    start_event_list = bpmn_graph.get_nodes(consts.Consts.start_event)
    for element in start_event_list:
        tmp = [classification_element, classification_start_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    intermediate_catch_event_list = bpmn_graph.get_nodes(
        consts.Consts.intermediate_catch_event)
    for element in intermediate_catch_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    end_event_list = bpmn_graph.get_nodes(consts.Consts.end_event)
    for element in end_event_list:
        tmp = [classification_element, classification_end_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    intermediate_throw_event_list = bpmn_graph.get_nodes(
        consts.Consts.intermediate_throw_event)
    for element in intermediate_throw_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: tmp}]

    boundary_event_list = bpmn_graph.get_nodes(consts.Consts.boundary_event)
    for element in boundary_event_list:
        nodes_classification += [{node_param_name: element,
                                  classification_param_name: [classification_boundary]}]

    flows_classification = []
    flows_list = bpmn_graph.get_flows()
    for flow in flows_list:
        flows_classification += [{flow_param_name: flow,
                                  classification_param_name: ["Flow"]}]

    return nodes_classification, flows_classification


def classify_edges(start_node, flows, nodes, discovered, finished, back_edges_ids):
    discovered.append(start_node[consts.Consts.node][0])
    reversed =  False

    for edge_id in start_node[consts.Consts.node][1][consts.Consts.outgoing_flow]:
        edge = flows[edge_id]
        successor_id = edge[consts.Consts.target_ref]
        if successor_id not in discovered:
            successor = next(node for node in nodes if node[consts.Consts.node][0] == successor_id)
            reversed = classify_edges(successor, flows, nodes, discovered, finished, back_edges_ids)
            if reversed:
                back_edges_ids.append(edge_id)
                if len(start_node[consts.Consts.node][1][consts.Consts.outgoing_flow]) > 1:
                    reversed = False
        elif successor_id not in finished:
            back_edges_ids.append(edge_id)
            reversed = True
            if len(start_node[consts.Consts.node][1][consts.Consts.outgoing_flow]) > 1:
                reversed = False
    finished.append(start_node[consts.Consts.node][0])
    return reversed

def topological_sort(flows, tmp_nodes_with_classification):
    """
    :return:
    """
    node_param_name = "node"
    attached_param_name = 'attachedToRef'
    classification_param_name = "classification"

    sorted_nodes_with_classification = []
    no_incoming_flow_nodes = []

    boundary_events = []
    for node in tmp_nodes_with_classification:
        if "Boundary" in node[classification_param_name]:
            attached_to_id = node[node_param_name][1][attached_param_name]
            flow_id = node[node_param_name][1][consts.Consts.outgoing_flow].pop()
            flows[flow_id][consts.Consts.source_ref] = attached_to_id
            attached_to = next(tmp_node for tmp_node in tmp_nodes_with_classification
                               if tmp_node[node_param_name][0] == attached_to_id)
            attached_to[node_param_name][1][consts.Consts.outgoing_flow].append(
                flow_id)
            boundary_events.append(node)

    for boundary in boundary_events:
        tmp_nodes_with_classification.remove(boundary)
    tmp_nodes_with_classification_copy = copy.deepcopy(
        tmp_nodes_with_classification)

    while tmp_nodes_with_classification:
        for node_with_classification in tmp_nodes_with_classification:
            incoming_list = node_with_classification[node_param_name][1][consts.Consts.incoming_flow]
            if len(incoming_list) == 0:
                no_incoming_flow_nodes.append(node_with_classification)
        if len(no_incoming_flow_nodes) > 0:
            while len(no_incoming_flow_nodes) > 0:
                node_with_classification = no_incoming_flow_nodes.pop()
                tmp_nodes_with_classification.remove(node_with_classification)
                sorted_nodes_with_classification.append(next(tmp_node for tmp_node in tmp_nodes_with_classification_copy
                                                             if tmp_node[node_param_name][0] == node_with_classification[node_param_name][0]))

                outgoing_list = list(
                    node_with_classification[node_param_name][1][consts.Consts.outgoing_flow])
                tmp_outgoing_list = list(outgoing_list)

                for flow_id in tmp_outgoing_list:
                    '''
                    - Remove the outgoing flow for source flow node (the one without incoming flows)
                    - Get the target node
                    - Remove the incoming flow for target flow node
                    '''
                    outgoing_list.remove(flow_id)
                    node_with_classification[node_param_name][1][consts.Consts.outgoing_flow].remove(
                        flow_id)

                    flow = flows[flow_id]
                    target_id = flow[consts.Consts.target_ref]
                    target = next(tmp_node[node_param_name]
                                  for tmp_node in tmp_nodes_with_classification
                                  if tmp_node[node_param_name][0] == target_id)
                    target[1][consts.Consts.incoming_flow].remove(flow_id)
    return sorted_nodes_with_classification


def grid_layout(flows, sorted_nodes_with_classification, symmetric):
    """

    :param sorted_nodes_with_classification:
    :param bpmn_graph:
    :return:
    """
    tmp_nodes_with_classification = list(sorted_nodes_with_classification)

    last_row = consts.Consts.grid_column_width
    last_col = 1
    grid = []
    while tmp_nodes_with_classification:
        node_with_classification = tmp_nodes_with_classification.pop(0)
        (grid, last_row, last_col, _) = place_element_in_grid(node_with_classification, grid, last_row, last_col,
                                                              flows, tmp_nodes_with_classification, sorted_nodes_with_classification, symmetric)
    return grid


def reverse_flows(flows, tmp_nodes_with_classification, back_edges_ids):
    node_param_name = "node"
    for flow_id in back_edges_ids:
        flow = flows[flow_id]
        source_id = flow[consts.Consts.source_ref]
        target_id = flow[consts.Consts.target_ref]
        flow[consts.Consts.source_ref] = target_id
        flow[consts.Consts.target_ref] = source_id

        source_finished = False
        target_finished = False
        for node in tmp_nodes_with_classification:
            if node[node_param_name][0] == source_id:
                node[node_param_name][1][consts.Consts.outgoing_flow].remove(
                    flow_id)
                node[node_param_name][1][consts.Consts.incoming_flow].append(
                    flow_id)
                source_finished = True
            elif node[node_param_name][0] == target_id:
                node[node_param_name][1][consts.Consts.incoming_flow].remove(
                    flow_id)
                node[node_param_name][1][consts.Consts.outgoing_flow].append(
                    flow_id)
                target_finished = True
            if source_finished and target_finished:
                break

def place_element_in_grid(node_with_classification, grid, last_row, last_col, flows, nodes_with_classification, all_nodes_with_classification, symmetric, enforced_row_num=None):
    """

    :param node_with_classification:
    :param grid:
    :param last_row:
    :param last_col:
    :param bpmn_graph:
    :param nodes_with_classification:
    :param enforced_row_num:
    :return:
    """
    node_param_name = "node"

    node_id = node_with_classification[node_param_name][0]
    incoming_flows = node_with_classification[node_param_name][1][consts.Consts.incoming_flow]
    outgoing_flows = node_with_classification[node_param_name][1][consts.Consts.outgoing_flow]

    if len(incoming_flows) == 0:
        # if node has no incoming flow, put it in new row
        current_element_row = last_row
        current_element_col = last_col
        if enforced_row_num:
            insert_into_grid(grid, enforced_row_num,
                             current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row,
                             current_element_col, node_id)
        last_row += consts.Consts.grid_column_width
    # not join
    elif len(node_with_classification[node_param_name][1][consts.Consts.incoming_flow]) == 1:
        # if node is not a Join, put it right from its predecessor (element should only have one predecessor)
        flow_id = incoming_flows[0]
        flow = flows[flow_id]
        predecessor_id = flow[consts.Consts.source_ref]
        predecessor_cell = next(
            grid_cell for grid_cell in grid if grid_cell.node_id == predecessor_id)
        # insert into cell right from predecessor - no need to insert new column or row
        current_element_col = predecessor_cell.col + 1
        current_element_row = predecessor_cell.row
        if enforced_row_num is not None:
            insert_into_grid(grid, enforced_row_num,
                             current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row,
                             current_element_col, node_id)
    # TODO consider rule for split/join node
    else:
        # find the rightmost predecessor - put into next column
        # if last_split was passed, use row number from it, otherwise compute mean from predecessors
        predecessors_id_list = []
        for flow_id in incoming_flows:
            flow = flows[flow_id]
            predecessors_id_list.append(flow[consts.Consts.source_ref])

        max_col_num = 0
        for grid_cell in grid:
            if grid_cell.node_id in predecessors_id_list:
                if grid_cell.col > max_col_num:
                    max_col_num = grid_cell.col
        current_element_col = max_col_num + 1

        # find corresponding split:
        if enforced_row_num is None:
            previous_cell = next(
                node for node in all_nodes_with_classification if node[node_param_name][0] == predecessors_id_list[0])
            forks = 1
            found = True
            while True:
                predecessors_ids = []
                in_flows = previous_cell[node_param_name][1][consts.Consts.incoming_flow]
                for flow_id in in_flows:
                    flow = flows[flow_id]
                    predecessors_ids.append(flow[consts.Consts.source_ref])

                successors_ids = []
                out_flows = previous_cell[node_param_name][1][consts.Consts.outgoing_flow]
                for flow_id in out_flows:
                    flow = flows[flow_id]
                    successors_ids.append(flow[consts.Consts.target_ref])

                if len(predecessors_ids) > 1:
                    forks += 1
                if len(successors_ids) > 1:
                    forks -= 1

                if forks == 0:
                    break

                if len(predecessors_ids) > 0:
                    previous_cell = next(
                        node for node in all_nodes_with_classification if node[node_param_name][0] == predecessors_ids[0])
                else:
                    found = False
                    break

            if found:
                for grid_cell in grid:
                    if grid_cell.node_id == previous_cell[node_param_name][0]:
                        current_element_row = grid_cell.row
            else:
                row_num_sum = 0
                for grid_cell in grid:
                    if grid_cell.node_id in predecessors_id_list:
                        row_num_sum += grid_cell.row
                current_element_row = row_num_sum // len(predecessors_id_list)

            insert_into_grid(grid, current_element_row,
                             current_element_col, node_id)
        else:
            insert_into_grid(grid, enforced_row_num,
                             current_element_col, node_id)

    shift = 0
    shift_all = 0
    # if split
    if len(node_with_classification[node_param_name][1][consts.Consts.outgoing_flow]) > 1:
        for grid_cell in grid:
            if grid_cell.node_id == node_with_classification[node_param_name][0]:
                current_element_row = grid_cell.row
                break
        successors_id_list = []
        for flow_id in outgoing_flows:
            flow = flows[flow_id]
            successors_id_list.append(flow[consts.Consts.target_ref])
        successor_node_list = [successor_node for successor_node in nodes_with_classification
                               if successor_node[node_param_name][0] in successors_id_list]
        num_of_successors = len(successor_node_list)

        if num_of_successors != 0:
            shift_all = num_of_successors // 2
            for cell in grid:
                if cell.row < current_element_row:
                    cell.row -= shift_all
                elif cell.row > current_element_row:
                    cell.row += shift_all
            if num_of_successors % 2 != 0:
                # if number of successors is even, put one half over the split, second half below
                # proceed with first half
                centre = (num_of_successors // 2)
                for index in range(0, centre):
                    # place element above split
                    successor_node = successor_node_list[index]
                    (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                  flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row - ((centre - index - shift) * consts.Consts.grid_column_width))
                    shift += tmp_shift
                    nodes_with_classification.remove(successor_node)

                successor_node = successor_node_list[centre]
                (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                              flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + shift * consts.Consts.grid_column_width)
                shift += tmp_shift
                nodes_with_classification.remove(successor_node)
                for index in range(centre + 1, num_of_successors):
                    # place element below split
                    successor_node = successor_node_list[index]
                    (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                  flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + ((index - centre + shift) * consts.Consts.grid_column_width))
                    shift += tmp_shift
                    nodes_with_classification.remove(successor_node)

            else:
                if symmetric:
                    centre = (num_of_successors // 2)
                    for index in range(0, centre):
                        # place element above split
                        successor_node = successor_node_list[index]
                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                      flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row - ((centre - index - shift) * consts.Consts.grid_column_width))
                        shift += tmp_shift
                        nodes_with_classification.remove(successor_node)

                    for index in range(centre, num_of_successors):
                        # place element below split
                        successor_node = successor_node_list[index]

                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                      flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + (index - centre + shift + 1) * consts.Consts.grid_column_width)
                        shift += tmp_shift
                        nodes_with_classification.remove(successor_node)
                else:
                    centre = (num_of_successors // 2)
                    for index in range(0, centre):
                        # place element above split
                        successor_node = successor_node_list[index]
                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                      flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row - ((centre - index - shift - 1) * consts.Consts.grid_column_width))
                        shift += tmp_shift
                        nodes_with_classification.remove(successor_node)

                    for index in range(centre, num_of_successors):
                        # place element below split
                        successor_node = successor_node_list[index]
                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                                      flows, nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + (index - centre + shift + 1) * consts.Consts.grid_column_width)
                        shift += tmp_shift
                        nodes_with_classification.remove(successor_node)

    return grid, last_row, last_col, shift + shift_all


def insert_into_grid(grid, row, col, node_id):
    """

    :param grid:
    :param row:
    :param col:
    :param node_id:
    """
    # if row <= 0:
    #     row = 1
    grid.append(cell_class.GridCell(row, col, node_id))


def partition(array, start, end):
    pivot = array[start].col
    low = start + 1
    high = end

    while True:
        while low <= high and array[high].col >= pivot:
            high = high - 1
        while low <= high and array[low].col <= pivot:
            low = low + 1
        if low <= high:
            array[low], array[high] = array[high], array[low]
        else:
            break
    array[start], array[high] = array[high], array[start]

    return high


def sort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    sort(array, start, p-1)
    sort(array, p+1, end)


def interleave(grid):
    """
    :param grid:
    """
    rows = {}
    first_row = 1
    last_row = 1

    for cell in grid:
        if cell.row < first_row:
            first_row = cell.row
        elif cell.row > last_row:
            last_row = cell.row
        try:
            rows[cell.row].append(cell)
        except KeyError:
            rows[cell.row] = [cell]

    for row in rows.values():
        sort(row, 0, len(row) - 1)

    shift = 0
    for i in range(first_row, last_row+1):
        if i not in rows:
            shift += 1
        elif shift > 0:
            for cell in rows[i]:
                cell.row -= shift
            rows[i-1] = rows.pop(i)
    last_row -= shift

    i = first_row
    while i < last_row:
        prev_row = rows[i]
        next_row = rows[i+1]

        j = 0
        k = 0
        continue_next_row = False
        prev_len = len(prev_row)
        next_len = len(next_row)
        while j < prev_len and k < next_len:
            col1 = prev_row[j].col
            col2 = next_row[k].col
            if col1 == col2:
                i += 1
                continue_next_row = True
                break
            elif col1 < col2:
                j += 1
            else:
                k += 1
        if continue_next_row:
            continue
        # interleaving needed:
        # merge two rows:
        for cell in rows[i+1]:
            cell.row -= 1
        rows[i] += rows[i+1]
        sort(rows[i], 0, len(rows[i])-1)
        del rows[i+1]

        # shift all from below one row up:
        for j in range(i+2, last_row+1):
            for cell in rows[j]:
                cell.row -= 1
            rows[j-1] = rows.pop(j)
        last_row -= 1


def set_coordinates_for_nodes(bpmn_graph, grid):
    """

    :param bpmn_graph:
    :param grid:
    """

    nodes = bpmn_graph.get_nodes()
    for node in nodes:
        try:
            cell = next(
                grid_cell for grid_cell in grid if grid_cell.node_id == node[0])
            node[1][consts.Consts.x] = str(
                cell.col * 150 + (100 - int(node[1][consts.Consts.width]))//2)
            node[1][consts.Consts.y] = str(
                cell.row * 150 + (100 - int(node[1][consts.Consts.height]))//2)
        except:  # boundary events
            pass
    boundary_events = bpmn_graph.get_nodes(consts.Consts.boundary_event)
    for boundary in boundary_events:
        attached_to_id = boundary[1][consts.Consts.attached_to_ref]
        attached_to = next(tmp_node for tmp_node in nodes
                           if tmp_node[0] == attached_to_id)
        successor_id = bpmn_graph.get_flow_by_id(
            boundary[1][consts.Consts.outgoing_flow][0])[2][consts.Consts.target_ref]
        successor = next(tmp_node for tmp_node in nodes
                         if tmp_node[0] == successor_id)

        successor_y_center = int(
            successor[1][consts.Consts.y]) + int(successor[1][consts.Consts.height])//2
        att_y_center = int(
            attached_to[1][consts.Consts.y]) + int(attached_to[1][consts.Consts.height])//2
        if att_y_center < successor_y_center:
            boundary[1][consts.Consts.x] = str(
                int(attached_to[1][consts.Consts.x]) + 30)
            boundary[1][consts.Consts.y] = str(
                int(attached_to[1][consts.Consts.y]) + 80)
        elif att_y_center == successor_y_center:
            boundary[1][consts.Consts.x] = str(
                int(attached_to[1][consts.Consts.x]) + 80)
            boundary[1][consts.Consts.y] = str(
                int(attached_to[1][consts.Consts.y]) + 30)
        else:
            boundary[1][consts.Consts.x] = str(
                int(attached_to[1][consts.Consts.x]) + 30)
            boundary[1][consts.Consts.y] = str(
                int(attached_to[1][consts.Consts.y]) - 20)


def set_flows_waypoints(bpmn_graph, back_edges_ids, reversed_nodes):
    """

    :param bpmn_graph:
    """
    # TODO get rid of string cast
    flows = bpmn_graph.get_flows()
    node_param_name = "node"
    for flow in flows:
        if flow[2][consts.Consts.id] in back_edges_ids:
            reversed = True
            source_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
            try:
                source_node_copy = next(node for node in reversed_nodes if node[node_param_name][0] == flow[2][consts.Consts.target_ref])[node_param_name]
                source_outgoing = len(source_node_copy[1][consts.Consts.outgoing_flow])
            except StopIteration: # boundary event
                attached_to_id = source_node[1][consts.Consts.attached_to_ref]
                attached_to = next(tmp_node for tmp_node in reversed_nodes if tmp_node[node_param_name][0] == attached_to_id)[node_param_name]
                source_outgoing = len(attached_to[1][consts.Consts.outgoing_flow])
            target_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.source_ref])
        else:
            reversed = False
            source_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.source_ref])
            try:
                source_node_copy = next(node for node in reversed_nodes if node[node_param_name][0] == flow[2][consts.Consts.source_ref])[node_param_name]
                source_outgoing = len(source_node_copy[1][consts.Consts.outgoing_flow])
            except StopIteration: # boundary event
                attached_to_id = source_node[1][consts.Consts.attached_to_ref]
                attached_to = next(tmp_node for tmp_node in reversed_nodes if tmp_node[node_param_name][0] == attached_to_id)[node_param_name]
                source_outgoing = len(attached_to[1][consts.Consts.outgoing_flow])
            target_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
        source_width = int(source_node[1][consts.Consts.width])
        source_height = int(source_node[1][consts.Consts.height])
        source_x = int(source_node[1][consts.Consts.x])
        source_y = int(source_node[1][consts.Consts.y])

        target_width = int(target_node[1][consts.Consts.width])
        target_height = int(target_node[1][consts.Consts.height])
        target_x = int(target_node[1][consts.Consts.x])
        target_y = int(target_node[1][consts.Consts.y])

        if source_y + source_height//2 == target_y + target_height//2:
            # TODO what if an element is between source and target?
            if reversed:
                flow[2][consts.Consts.waypoints] = [(str(target_x),
                                                     str(target_y + target_height // 2)),
                                                    (str(source_x + source_width),
                                                     str(source_y + source_height // 2))]
            else:
                flow[2][consts.Consts.waypoints] = [(str(source_x + source_width),
                                                     str(source_y + source_height // 2)),
                                                    (str(target_x),
                                                     str(target_y + target_height // 2))]
        elif source_y < target_y:
            if source_outgoing > 1:  # split
                if reversed:
                    flow[2][consts.Consts.waypoints] = [(str(target_x),
                                                         str(target_y + target_height // 2)),
                                                        (str(source_x + source_width//2),
                                                         str(target_y + target_height // 2)),
                                                        (str(source_x + source_width//2), str(source_y + source_height))]
                else:
                    flow[2][consts.Consts.waypoints] = [(str(source_x + source_width//2),
                                                         str(source_y + source_height)),
                                                        (str(source_x + source_width//2),
                                                         str(target_y + target_height // 2)),
                                                        (str(target_x),
                                                         str(target_y + target_height // 2))]
            else:
                if reversed:
                    flow[2][consts.Consts.waypoints] = [(str(target_x + target_width//2),
                                                     str(target_y)),
                                                    (str(target_x + target_width//2),
                                                     str(source_y + source_height//2)),
                                                     (str(source_x + source_width),
                                                     str(source_y + source_height//2))]
                else:
                    flow[2][consts.Consts.waypoints] = [(str(source_x + source_width),
                                                     str(source_y + source_height//2)),
                                                    (str(target_x + target_width//2),
                                                     str(source_y + source_height//2)),
                                                    (str(target_x + target_width//2),
                                                     str(target_y))]
        else:
            if source_outgoing > 1:  # split
                if reversed:
                    flow[2][consts.Consts.waypoints] = [(str(target_x),
                                                        str(target_y + target_height // 2)),
                                                        (str(source_x + source_width//2),
                                                        str(target_y + target_height // 2)),
                                                        (str(source_x + source_width//2),
                                                        str(source_y))]
                else:
                    flow[2][consts.Consts.waypoints] = [(str(source_x + source_width//2),
                                                        str(source_y)),
                                                        (str(source_x + source_width//2),
                                                        str(target_y + target_height // 2)),
                                                        (str(target_x),
                                                        str(target_y + target_height // 2))]
            else:
                if reversed:
                    flow[2][consts.Consts.waypoints] = [(str(target_x + target_width//2),
                                                        str(target_y + target_height)),
                                                        (str(target_x + target_width//2),
                                                        str(source_y + source_height//2)),
                                                        (str(source_x + source_width),
                                                        str(source_y + source_height//2))]
                else:
                    flow[2][consts.Consts.waypoints] = [(str(source_x + source_width),
                                                        str(source_y + source_height//2)),
                                                        (str(target_x + target_width//2),
                                                        str(source_y + source_height//2)),
                                                        (str(target_x + target_width//2),
                                                        str(target_y + target_height))]
