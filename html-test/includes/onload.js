var scriptControl = new ScriptControl(document);

// Firefox does not give an import error if web component's not enabled.
function onImportError(event) {
  console.log('Error loading import: ' + event.target.href);
  return;
}

window.onload = function() {
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