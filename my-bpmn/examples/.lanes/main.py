import os.path
import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_python.bpmn_diagram_visualizer as visualizer

output_directory = "./"
example_path = "lanes.bpmn"
output_file_with_di = "lanes-example-output.xml"
output_file_no_di = "lanes-example-output-no-di.xml"
output_png_file = "old"

bpmn_graph = diagram.BpmnDiagramGraph()
bpmn_graph.load_diagram_from_xml_file(os.path.abspath(example_path))
bpmn_graph.export_xml_file(output_directory, output_file_with_di)
bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)
visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)
