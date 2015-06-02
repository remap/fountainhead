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
    if (event.keyCode == 32) {
      if (scriptControl.spaceBarElement !== undefined) {
        var element = scriptControl.spaceBarElement.shadowRoot.querySelector("#cue-go");
        if (element !== undefined && element !== null && event.target == document.body) {
          element.click();
          var originalColor = element.style.color;
          element.style.color = 'blue';
          setTimeout(function () {
            element.style.color = originalColor;
          }, 100);
          event.preventDefault();
          return false;
        }
      }
    }
  });
  
  if (window.DBObject !== undefined) {
    window.dbObject = new window.DBObject();

    window.dbObject.selectRandomFromMediaTable = function () {
      if (window.dbObject.medias !== undefined) {
        var randIdx = Math.floor(Math.random() * window.dbObject.medias.length);
        var serviceUrl = 'https://www.youtube.com/watch?v=' + window.dbObject.medias[randIdx][0];
        return serviceUrl;
      } else {
        return '';
      }
    };

    window.dbObject.loadMediaTable = function () {
      var wholeQueryStr = 'select key, description from media';
      window.dbObject.postToDB(wholeQueryStr, function (responseText) {
        window.dbObject.medias = JSON.parse(responseText);
      });
    };

    window.dbObject.loadParticipantTable = function () {

    };
  
    window.dbObject.loadMediaTable();
  }
  
  console.log("onload");
};