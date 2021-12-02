var AutoLayout = require('./AutoLayout.js');

var autoLayout = new AutoLayout();

var fs = require('fs')
var fsPromises = fs.promises;


(async () => {

  var diagramXML = fs.readFileSync("complex.xml").toString();
  var layoutedDiagramXML = await autoLayout.layoutProcess(diagramXML);

  // or write to file
  await fsPromises.writeFile('./layouted.bpmn', layoutedDiagramXML);
})();

// console.log("effdv")
// console.log("effdv")