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

[start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="Start")
[exc_split1_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="1")
[exc_join1_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="2")
[exc_split2_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="3")
[exc_join2_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                    gateway_name="4")

[task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="1")
[task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="2")
[task3_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="3")
[task4_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="4")

[end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="End")

bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, exc_split1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_split1_id, task1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_split1_id, task2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exc_join1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, exc_join1_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_join1_id, exc_split2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_split2_id, task3_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_split2_id, task4_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task3_id, exc_join2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, task4_id, exc_join2_id)
bpmn_graph.add_sequence_flow_to_diagram(process_id, exc_join2_id, end_id)

layouter.generate_layout(bpmn_graph, symmetric=True)

bpmn_graph.export_xml_file(output_directory, output_file_with_di)
