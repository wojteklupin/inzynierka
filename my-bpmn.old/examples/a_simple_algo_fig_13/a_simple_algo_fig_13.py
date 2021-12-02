import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram

output_directory = "./"
output_file_with_di = "complex.xml"
output_file_no_di = "complex-no-di.xml"
output_dot_file = "complex"
output_png_file = "complex"

bpmn_graph = diagram.BpmnDiagramGraph()
bpmn_graph.create_new_diagram_graph(diagram_name="a_simple_algo_fig_13")
process_id = bpmn_graph.add_process_to_diagram()

[start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event")
[login_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Login")
[paral_fork1_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
    gateway_name="2")
[show_new_msgs_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Show new messages")
[show_new_tasks_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Show new tasks")
[paral_join1_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
    gateway_name="7")

[exc_fork2_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="8")
[accept_task_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="9")
[exc_join2_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="10")
[exc_join3_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="13")
[read_msg_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="14")
[exc_fork3_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="15")
[logout_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="11")
[end_id1, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="12")

[cancel_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Cancel")
[end_id2, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="end_event2")

bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, login_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, login_id, paral_fork1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, paral_fork1_id, show_new_msgs_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, paral_fork1_id, show_new_tasks_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, show_new_msgs_id, paral_join1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, show_new_tasks_id, paral_join1_id)

bpmn_graph.add_sequence_flow_to_diagram(process_id, paral_join1_id, exc_fork2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork2_id, accept_task_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork2_id, exc_join2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork2_id, exc_join3_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, accept_task_id, exc_join2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork3_id, exc_join2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_fork3_id, exc_join3_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_join3_id, read_msg_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, read_msg_id, exc_fork3_id)

bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_join2_id, logout_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, logout_id, end_id1)

bpmn_graph.add_sequence_flow_to_diagram(process_id, login_id, cancel_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, cancel_id, end_id2)

layouter.generate_layout(bpmn_graph)

bpmn_graph.export_xml_file(output_directory, output_file_with_di)
bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)
# Uncomment line below to get a simple view of created diagram
# visualizer.visualize_diagram(bpmn_graph)
visualizer.bpmn_diagram_to_dot_file(bpmn_graph, output_directory + output_dot_file)
visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)
