var scriptControl = new ScriptControl(document);

// Firefox does not give an import error if web component's not enabled.
function onImportError(event) {
  console.log('Error loading import: ' + event.target.href);
  return;
}

function getYoutubeVideoUrl(serviceUrl, fetchIfNotExist) {
  var data = new FormData();
  data.append('url', serviceUrl);
  data.append('fetchIfNotExist', fetchIfNotExist);
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', 'http://localhost:5000/services/get-youtube-url', true);
  
  xhr.onload = function () {
    console.log('Got response from server: ' + this.responseText);
  };
  xhr.send(data);
}

function loadYoutubeVideoUrls(serviceUrls) {
  var data = new FormData();
  data.append('urls', JSON.stringify(serviceUrls));
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', 'http://localhost:5000/services/load-youtube-urls', true);
  
  xhr.onload = function () {
    console.log('Got response from server: ' + this.responseText);
  };
  xhr.send(data);
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
  
  // Tests for loadYoutubeVideoUrls and getYoutubeVideoUrl
  var ytUrls = ['https://www.youtube.com/watch?v=77rHEjXj-b8', 
                'https://www.youtube.com/watch?v=XJqm2irnYlM', 
                'https://www.youtube.com/watch?v=pY54WU0C3i4', 
                'https://www.youtube.com/watch?v=kr7MDoWLQ14', 
                'https://www.youtube.com/watch?v=2od2GZg7-88'];
  
  loadYoutubeVideoUrls(ytUrls);
  
  for (var i = 0; i < ytUrls.length; i++) {
    getYoutubeVideoUrl(ytUrls[i], true);
  }
  
  console.log("onload");
};