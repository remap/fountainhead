var ndnURLPublisherFactory = new URLPublisherFactory(window, document);

var scriptControl = new ScriptControl(document);
scriptControl.loadComponentDocs();

window.onload = function() {
  //scriptControl.toggleClassVisibility('dialogue');
  
  // Pressing t to toggle the visibility of the ugly floating menu
  var floatingMenuDiv = 'floating-menu';
  document.addEventListener('keydown', function (event) {
    // ASCII of 't' or 'T'
    if (event.keyCode == 84 || event.keyCode == 116) {
      scriptControl.toggleDivIdVisibility(floatingMenuDiv);
    }
  });
  
  console.log("onload");
};