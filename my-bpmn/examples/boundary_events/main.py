import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_rep as diagram

output_directory = "./"
output_file_with_di = "complex.xml"
output_file_no_di = "complex-no-di.xml"
output_dot_file = "complex"
output_png_file = "complex"

bpmn_graph = diagram.BpmnDiagramGraph()
bpmn_graph.create_new_diagram_graph(diagram_name="nested")
process_id = bpmn_graph.add_process_to_diagram()

[start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="Start", node_id="start")

[task_id, _] = bpmn_graph.add_task_to_diagram(process_id, "", node_id="task")
[bnd_id, _] = bpmn_graph.add_boundary_event_to_task(process_id, task_id, "message")
[end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id,node_id="end")

bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, bnd_id, end_id)

layouter.generate_layout(bpmn_graph)

bpmn_graph.export_xml_file(output_directory, output_file_with_di)
# bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)
# Uncomment line below to get a simple view of created diagram
# visualizer.visualize_diagram(bpmn_graph)
# visualizer.bpmn_diagram_to_dot_file(bpmn_graph, output_directory + output_dot_file)
# visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)
