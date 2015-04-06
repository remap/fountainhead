/**
 * Script control Javascript containing UI control functions.
 */

var ScriptControl = function ScriptControl(doc) {
  this.document = doc;
  this.links = this.document.querySelectorAll('link[rel="import"]');
  
  this.importedDocuments = [];
};

/**
 * Toggle 'display' in plain JS by class name
 *
 * Note: Difference between display and visibility: a hidden element is still taking up the space
 * while a 'none' display element is not; Implementing the function as 'display:none' for now.
 *
 * Note: this execution does not affect the elements in web component generated documents.
 */
ScriptControl.prototype.toggleClassVisibility = function(className, visible) {
  var flag = visible;
  var elements = this.document.getElementsByClassName(className);
  
  if (elements == undefined || elements.length == 0) {
    console.log("No elements of such class " + className);
    return ;
  }
  
  if (flag == undefined) {
    flag = elements[0].style.display;
  }
  
  if (flag != 'none' || flag == false) {
    flag = 'none';
  } else if (flag == 'none' || flag == true) {
    flag = 'inline';
  } else {
    console.log("Unrecognized toggle flag option: " + flag);
  }
  
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = flag;
  }
};

/**
 * TODO: This does not work yet, debugging
 */
ScriptControl.prototype.loadComponentDocs = function()
{
  var self = this;
  
  for (var i = 0; i < this.links.length; i++) {
    this.links[i].addEventListener('load', function(e) {
      self.importedDocuments.push(self.links[i].import);
      console.log("*** imported load ***" + i);
    });
  }
};

exports.ScriptControl = ScriptControl;
