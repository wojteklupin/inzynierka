# coding=utf-8
# Reverse bpmn_graph flows in reverse_flows()
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
    (sorted_nodes_with_classification, flows, backward_flows) = topological_sort(bpmn_graph, classification[0])

    reverse_flows(sorted_nodes_with_classification, flows, backward_flows)
    grid = grid_layout(flows, sorted_nodes_with_classification, symmetric)
    set_coordinates_for_nodes(bpmn_graph, grid)
    set_flows_waypoints(bpmn_graph, backward_flows)

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
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    subprocess_list = bpmn_graph.get_nodes(consts.Consts.subprocess)
    for element in subprocess_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    complex_gateway_list = bpmn_graph.get_nodes(consts.Consts.complex_gateway)
    for element in complex_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    event_based_gateway_list = bpmn_graph.get_nodes(consts.Consts.event_based_gateway)
    for element in event_based_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    inclusive_gateway_list = bpmn_graph.get_nodes(consts.Consts.inclusive_gateway)
    for element in inclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    exclusive_gateway_list = bpmn_graph.get_nodes(consts.Consts.exclusive_gateway)
    for element in exclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    parallel_gateway_list = bpmn_graph.get_nodes(consts.Consts.parallel_gateway)
    for element in parallel_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    start_event_list = bpmn_graph.get_nodes(consts.Consts.start_event)
    for element in start_event_list:
        tmp = [classification_element, classification_start_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    intermediate_catch_event_list = bpmn_graph.get_nodes(consts.Consts.intermediate_catch_event)
    for element in intermediate_catch_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    end_event_list = bpmn_graph.get_nodes(consts.Consts.end_event)
    for element in end_event_list:
        tmp = [classification_element, classification_end_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    intermediate_throw_event_list = bpmn_graph.get_nodes(consts.Consts.intermediate_throw_event)
    for element in intermediate_throw_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    boundary_event_list = bpmn_graph.get_nodes(consts.Consts.boundary_event)
    for element in boundary_event_list:
        nodes_classification += [{node_param_name: element, classification_param_name: [classification_boundary]}]

    flows_classification = []
    flows_list = bpmn_graph.get_flows()
    for flow in flows_list:
        flows_classification += [{flow_param_name: flow, classification_param_name: ["Flow"]}]

    return nodes_classification, flows_classification


def topological_sort(bpmn_graph, nodes_with_classification):
    """
    :return:
    """
    node_param_name = "node"
    attached_param_name = 'attachedToRef'
    classification_param_name = "classification"

    tmp_nodes_with_classification = copy.deepcopy(nodes_with_classification)
    flows = copy.deepcopy(bpmn_graph.sequence_flows)
    sorted_nodes_with_classification = []
    no_incoming_flow_nodes = []
    backward_flows = []

    boundary_events = []
    for node in tmp_nodes_with_classification:
        if "Boundary" in node[classification_param_name]:
            attached_to_id = node[node_param_name][1][attached_param_name]
            flow_id = node[node_param_name][1][consts.Consts.outgoing_flow].pop()
            flows[flow_id][consts.Consts.source_ref] = attached_to_id
            attached_to = next(tmp_node for tmp_node in tmp_nodes_with_classification
                if tmp_node[node_param_name][0] == attached_to_id)
            attached_to[node_param_name][1][consts.Consts.outgoing_flow].append(flow_id)
            boundary_events.append(node)

    for boundary in boundary_events:
        tmp_nodes_with_classification.remove(boundary)

    while tmp_nodes_with_classification:
        for node_with_classification in tmp_nodes_with_classification:
            incoming_list = node_with_classification[node_param_name][1][consts.Consts.incoming_flow]
            if len(incoming_list) == 0:
                no_incoming_flow_nodes.append(node_with_classification)
        if len(no_incoming_flow_nodes) > 0:
            while len(no_incoming_flow_nodes) > 0:
                node_with_classification = no_incoming_flow_nodes.pop()
                tmp_nodes_with_classification.remove(node_with_classification)
                sorted_nodes_with_classification \
                    .append(next(tmp_node for tmp_node in nodes_with_classification
                                 if tmp_node[node_param_name][0] == node_with_classification[node_param_name][0]))

                outgoing_list = list(node_with_classification[node_param_name][1][consts.Consts.outgoing_flow])
                tmp_outgoing_list = list(outgoing_list)

                for flow_id in tmp_outgoing_list:
                    '''
                    - Remove the outgoing flow for source flow node (the one without incoming flows)
                    - Get the target node
                    - Remove the incoming flow for target flow node
                    '''
                    outgoing_list.remove(flow_id)
                    node_with_classification[node_param_name][1][consts.Consts.outgoing_flow].remove(flow_id)

                    flow = flows[flow_id]
                    target_id = flow[consts.Consts.target_ref]
                    target = next(tmp_node[node_param_name]
                                  for tmp_node in tmp_nodes_with_classification
                                  if tmp_node[node_param_name][0] == target_id)
                    target[1][consts.Consts.incoming_flow].remove(flow_id)
        else:
            for node_with_classification in tmp_nodes_with_classification:
                if "Join" in node_with_classification[classification_param_name]:
                    incoming_list = list(node_with_classification[node_param_name][1][consts.Consts.incoming_flow])
                    original_node = next(tmp_node for tmp_node in nodes_with_classification
                        if tmp_node[node_param_name][0] == node_with_classification[node_param_name][0])
                    original_in_list = original_node[node_param_name][1][consts.Consts.incoming_flow]
                    if len(incoming_list) < len(original_in_list):
                        cycling_node = node_with_classification
                        break
            incoming_list = cycling_node[node_param_name][1][consts.Consts.incoming_flow]
            for flow_id in incoming_list:
                flow = flows[flow_id]
                source_id = flow[consts.Consts.source_ref]
                flow[consts.Consts.source_ref] = flow[consts.Consts.target_ref]
                flow[consts.Consts.target_ref] = source_id
                backward_flows.append(flow_id)
                source_node = next(tmp_node for tmp_node in tmp_nodes_with_classification
                        if tmp_node[node_param_name][0] == source_id)
                source_node[node_param_name][1][consts.Consts.incoming_flow].append(flow_id)
                source_node[node_param_name][1][consts.Consts.outgoing_flow].remove(flow_id)
            cycling_node[node_param_name][1][consts.Consts.outgoing_flow] += cycling_node[node_param_name][1][consts.Consts.incoming_flow]
            cycling_node[node_param_name][1][consts.Consts.incoming_flow] = []
    return sorted_nodes_with_classification, flows, backward_flows


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


def reverse_flows(sorted_nodes_with_classification, flows, backward_flows):
    node_param_name = "node"
    for flow_id in backward_flows:
        flow = flows[flow_id]
        source_id = flow[consts.Consts.target_ref]
        target_id = flow[consts.Consts.source_ref]

        source_finished = False
        target_finished = False
        for node in sorted_nodes_with_classification: # TODO possible self-referencing cycle (but doesn't occur in BPMN diagrams)
            if source_finished and target_finished: break

            if node[node_param_name][0] == source_id:
                node[node_param_name][1][consts.Consts.outgoing_flow].remove(flow_id)
                node[node_param_name][1][consts.Consts.incoming_flow].append(flow_id)
                source_finished = True
            elif node[node_param_name][0] == target_id:
                node[node_param_name][1][consts.Consts.incoming_flow].remove(flow_id)
                node[node_param_name][1][consts.Consts.outgoing_flow].append(flow_id)
                target_finished = True

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
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)
        last_row += consts.Consts.grid_column_width
    elif len(node_with_classification[node_param_name][1][consts.Consts.incoming_flow]) == 1: # not join
        # if node is not a Join, put it right from its predecessor (element should only have one predecessor)
        flow_id = incoming_flows[0]
        flow = flows[flow_id]
        predecessor_id = flow[consts.Consts.source_ref]
        predecessor_cell = next(grid_cell for grid_cell in grid if grid_cell.node_id == predecessor_id)
        # insert into cell right from predecessor - no need to insert new column or row
        current_element_col = predecessor_cell.col + 1
        current_element_row = predecessor_cell.row
        if enforced_row_num is not None:
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)
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
        if not enforced_row_num:
            previous_cell = next(node for node in all_nodes_with_classification if node[node_param_name][0] == predecessors_id_list[0])
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
                    
                if forks == 0: break

                if len(predecessors_ids) > 0:
                    previous_cell = next(node for node in all_nodes_with_classification if node[node_param_name][0] == predecessors_ids[0])
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

        if enforced_row_num:
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)

    shift = 0
    shift_all = 0
    if len(node_with_classification[node_param_name][1][consts.Consts.outgoing_flow]) > 1: # if split
        for grid_cell in grid:
            if grid_cell.node_id == node_with_classification[node_param_name][0]:
                current_element_row = grid_cell.row
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
                                                                    flows ,nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row - ((centre - index - shift) * consts.Consts.grid_column_width))
                    shift += tmp_shift
                    nodes_with_classification.remove(successor_node)

                successor_node = successor_node_list[centre]
                (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                flows ,nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + shift * consts.Consts.grid_column_width)
                shift += tmp_shift
                nodes_with_classification.remove(successor_node)
                for index in range(centre + 1, num_of_successors):
                    # place element below split
                    successor_node = successor_node_list[index]
                    (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                    flows ,nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + ((index - centre + shift) * consts.Consts.grid_column_width))
                    shift += tmp_shift
                    nodes_with_classification.remove(successor_node)

            else:
                if symmetric:
                    centre = (num_of_successors // 2)
                    for index in range(0, centre):
                        # place element above split
                        successor_node = successor_node_list[index]
                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                        flows ,nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row - ((centre - index - shift) * consts.Consts.grid_column_width))
                        shift += tmp_shift
                        nodes_with_classification.remove(successor_node)



                    for index in range(centre, num_of_successors):
                        # place element below split
                        successor_node = successor_node_list[index]
                        (grid, last_row, last_col, tmp_shift) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                        flows ,nodes_with_classification, all_nodes_with_classification, symmetric, current_element_row + (index - centre + shift + 1) * consts.Consts.grid_column_width)
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


def set_coordinates_for_nodes(bpmn_graph, grid):
    """

    :param bpmn_graph:
    :param grid:
    """

    nodes = bpmn_graph.get_nodes()
    for node in nodes:
        try:
            cell = next(grid_cell for grid_cell in grid if grid_cell.node_id == node[0])
            node[1][consts.Consts.x] = str(cell.col * 150 + 50)
            node[1][consts.Consts.y] = str(cell.row * 150 + 50)
        except: # boundary events
            pass
    boundary_events = bpmn_graph.get_nodes(consts.Consts.boundary_event)
    for boundary in boundary_events:
        attached_to_id = boundary[1][consts.Consts.attached_to_ref]
        attached_to = next(tmp_node for tmp_node in nodes
            if tmp_node[0] == attached_to_id)
        successor_id = bpmn_graph.get_flow_by_id(boundary[1][consts.Consts.outgoing_flow][0])[2][consts.Consts.target_ref]
        successor = next(tmp_node for tmp_node in nodes
            if tmp_node[0] == successor_id)

        succ_y = successor[1][consts.Consts.y]
        att_y = attached_to[1][consts.Consts.y]
        if att_y < succ_y:
            boundary[1][consts.Consts.x] = str( int(attached_to[1][consts.Consts.x]) + 30 )
            boundary[1][consts.Consts.y] = str( int(attached_to[1][consts.Consts.y]) + 80 )
        elif att_y == succ_y:
            boundary[1][consts.Consts.x] = str( int(attached_to[1][consts.Consts.x]) + 80 )
            boundary[1][consts.Consts.y] = str( int(attached_to[1][consts.Consts.y]) + 30 )
        else:
            boundary[1][consts.Consts.x] = str( int(attached_to[1][consts.Consts.x]) + 30 )
            boundary[1][consts.Consts.y] = str( int(attached_to[1][consts.Consts.y]) - 20 )

def set_flows_waypoints(bpmn_graph, backward_flows):
    """

    :param bpmn_graph:
    """
    # TODO hardcoded node center, better compute it with x,y coordinates and height/width
    # TODO get rid of string cast
    flows = bpmn_graph.get_flows()
    id_param = "id"
    for flow in flows:
        backward = False
        flow_id = flow[2][id_param]
        if flow[2][id_param] in backward_flows:
            backward = True
        source_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.source_ref])
        source_width = int(source_node[1][consts.Consts.width])
        source_height = int(source_node[1][consts.Consts.height])

        target_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
        target_width = int(target_node[1][consts.Consts.width])
        target_height = int(target_node[1][consts.Consts.height])
        if source_node[1][consts.Consts.y] == target_node[1][consts.Consts.y]:
            if backward:
                source_node, target_node = target_node, source_node
                source_width, target_width = target_width, source_width
                source_height, target_height = target_height, source_height
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x])),
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width),
                                                    str(int(target_node[1][consts.Consts.y]) + target_height // 2))]
            else:
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x]) + source_width),
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x])),
                                                    str(int(target_node[1][consts.Consts.y]) + target_height // 2))]

        elif len(target_node[1][consts.Consts.incoming_flow]) > 1:
            if backward:
                source_node, target_node = target_node, source_node
                source_width, target_width = target_width, source_width
                source_height, target_height = target_height, source_height
                if int(target_node[1][consts.Consts.y]) > int(source_node[1][consts.Consts.y]):
                    offset = 0
                else:
                    offset = target_height
                if int(target_node[1][consts.Consts.x]) > int(source_node[1][consts.Consts.x]):
                    offset2 = source_width
                else:
                    offset2 = 0
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x]) + offset2),
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width // 2),
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width // 2),
                                                    str(int(target_node[1][consts.Consts.y]) + offset))]
            else:
                if int(target_node[1][consts.Consts.y]) > int(source_node[1][consts.Consts.y]):
                    offset = 0
                else:
                    offset = target_height
                # if int(target_node[1][consts.Consts.x]) < int(source_node[1][consts.Consts.x]):
                #     offset2 = 0
                # else:
                #     offset2 = source_width
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x]) + source_width), # offset2
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width // 2),
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width // 2),
                                                    str(int(target_node[1][consts.Consts.y]) + offset))]
        else:
            if backward:
                source_node, target_node = target_node, source_node
                source_width, target_width = target_width, source_width
                source_height, target_height = target_height, source_height
                if int(target_node[1][consts.Consts.y]) > int(source_node[1][consts.Consts.y]):
                    offset = target_height
                else:
                    offset = 0
                # if int(target_node[1][consts.Consts.x]) > int(source_node[1][consts.Consts.x]):
                #     offset2 = source_width
                # else:
                #     offset2 = 0
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x])), # offset2
                                                    str(int(source_node[1][consts.Consts.y]) + source_height // 2)),
                                                (str(int(source_node[1][consts.Consts.x]) + source_width // 2),
                                                    str(int(target_node[1][consts.Consts.y]) + target_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + target_width // 2),
                                                    str(int(target_node[1][consts.Consts.y]) + offset))]
            else:
                if int(target_node[1][consts.Consts.y]) > int(source_node[1][consts.Consts.y]):
                    offset = source_height
                else:
                    offset = 0
                if int(target_node[1][consts.Consts.x]) < int(source_node[1][consts.Consts.x]):
                    offset2 = target_width
                else:
                    offset2 = 0
                flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x]) + source_width // 2),
                                                    str(int(source_node[1][consts.Consts.y]) + offset)),
                                                (str(int(source_node[1][consts.Consts.x]) + source_width // 2),
                                                    str(int(target_node[1][consts.Consts.y]) + target_height // 2)),
                                                (str(int(target_node[1][consts.Consts.x]) + offset2),
                                                    str(int(target_node[1][consts.Consts.y]) + target_height // 2))]
        if backward:
            flow[2][consts.Consts.source_ref], flow[2][consts.Consts.target_ref] = flow[2][consts.Consts.target_ref], flow[2][consts.Consts.source_ref]
            source_node[1][consts.Consts.incoming_flow].remove(flow_id)
            source_node[1][consts.Consts.outgoing_flow].append(flow_id)
            target_node[1][consts.Consts.outgoing_flow].remove(flow_id)
            target_node[1][consts.Consts.incoming_flow].append(flow_id)
