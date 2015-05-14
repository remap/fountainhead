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
  
  /*
  // Tests for loadYoutubeVideoUrls and getYoutubeVideoUrl
  var ytUrls = ['https://www.youtube.com/watch?v=77rHEjXj-b8', 
                'https://www.youtube.com/watch?v=XJqm2irnYlM', 
                'https://www.youtube.com/watch?v=pY54WU0C3i4', 
                'https://www.youtube.com/watch?v=kr7MDoWLQ14', 
                'https://www.youtube.com/watch?v=2od2GZg7-88'];
  
  // This preloads the list of service urls, and store their corresponding video urls on server 
  loadYoutubeVideoUrls(ytUrls);
  */
  console.log("onload");
};