/**
 * Script control Javascript containing UI control functions.
 */

var ScriptControl = function ScriptControl(doc) {
  this.document = doc;
  this.links = [];
  
  this.importedElements = [];
  this.spaceBarElement = undefined;
};

/**
 * Toggle 'display' in plain JS by class name
 *
 * Note: Difference between display and visibility: a hidden element is still taking up the space
 * while a 'none' display element is not; Implementing the function as 'display:none' for now.
 *
 */
ScriptControl.prototype.toggleClassVisibility = function(className, visible) {
  var flag = visible;
  
  // This is one way to locate the element by class in the web component's shadow dom
  // Investigating why it's not working (importedDocuments is an array of the documents of the web components)
  /*
  var elements = [].slice.call(this.document.getElementsByClassName(className));
  for (var i = 0; i < this.importedDocuments.length; i++) {
    elements.push.apply(elements, [].slice.call(this.importedDocuments[i].querySelector('template').content.querySelectorAll("." + className)));
  }
  */
  
  // Note: Apply toggle by class names for imported documents;
  for (var i = 0; i < this.importedElements.length; i++) {
    if (this.importedElements[i].toggleClassVisibility !== undefined) {
      this.importedElements[i].toggleClassVisibility(className);
    }
  }
  
  var elements = this.document.getElementsByClassName(className);
  
  if (elements == undefined || elements.length == 0) {
    console.log("No elements of such class " + className + " in parent");
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
    console.log('Unrecognized toggle flag option: ' + flag);
  }
  
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = flag;
  }
};

/**
 * Toggle the display of floating toolbar
 */
ScriptControl.prototype.toggleDivIdVisibility = function(divId, visible)
{
  var flag = visible;
  var element = document.getElementById(divId);
  
  if (element == undefined) {
    console.log("No element by such id " + divId);
    return ;
  }
  
  if (flag == undefined) {
    flag = element.style.display;
  }
  
  if (flag != 'none' || flag == false) {
    flag = 'none';
  } else if (flag == 'none' || flag == true) {
    flag = 'inline';
  } else {
    console.log('Unrecognized toggle flag option: ' + flag);
  }
  
  element.style.display = flag;
};

/**
 * One document would have one '#cue-load' green at most.
 */
ScriptControl.prototype.cueStandByClicked = function (createdElement)
{
  for (var i = 0; i < this.importedElements.length; i++) {
    if (this.importedElements[i] === createdElement) {
      this.spaceBarElement = createdElement;
    } else {
      var loadElement = this.importedElements[i].shadowRoot.querySelector("#cue-load");
      if (loadElement !== undefined && loadElement !== null) {
        if (loadElement.className.indexOf('video-control-problem') !== -1) {
          loadElement.className = 'video-control-text video-control-problem';
        } else {
          loadElement.className = 'video-control-text';
        }
        this.importedElements[i].componentObject.applyStyleFromParentDocument(loadElement);
      }
    }
  }
};

exports.ScriptControl = ScriptControl;
