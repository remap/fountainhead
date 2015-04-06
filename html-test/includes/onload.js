var ndnURLPublisherFactory = new URLPublisherFactory(window, document);

var scriptControl = new ScriptControl(document);
scriptControl.loadComponentDocs();  

window.onload = function() {
  //scriptControl.toggleClassVisibility('dialogue');
  console.log("onload");
};