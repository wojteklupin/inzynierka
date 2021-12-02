import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram

output_directory = "./"
output_file_with_di = "complex.xml"
output_file_no_di = "complex-no-di.xml"
output_dot_file = "complex"
output_png_file = "complex"

bpmn_graph = diagram.BpmnDiagramGraph()
bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
process_id = bpmn_graph.add_process_to_diagram()

[start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="")
[task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task1")
[exc_fork1_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
    gateway_name="")
[task2a_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="")
[task2b_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="")
[exc_join1_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
    gateway_name="")

[end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="")

bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exc_fork1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork1_id, task2a_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork1_id, task2b_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task2a_id, exc_join1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task2b_id, exc_join1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_join1_id, end_id)

layouter.generate_layout(bpmn_graph)

bpmn_graph.export_xml_file(output_directory, output_file_with_di)
bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)
# Uncomment line below to get a simple view of created diagram
# visualizer.visualize_diagram(bpmn_graph)
visualizer.bpmn_diagram_to_dot_file(bpmn_graph, output_directory + output_dot_file)
visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)