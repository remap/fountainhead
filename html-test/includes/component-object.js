/**
 * ComponentObject is the parent class of web components, which includes basic component functions
 *
 * TODO: maybe better to have components inherit from two parent classes? One for HTMLElement, The other one for style related functions?
 *
 * Function:
 *   
 * @param self The web component element created from HTMLElement
 * @param window The parent window of the web component
 */

var ComponentObject = function ComponentObject(self, window) {
  this.window = window;
  this.shadowRoot = self.shadowRoot;
};

/**
 * Styling functions for general web components goes here
 */
ComponentObject.prototype.htmlClassFromName = function(fromName) {
  str = fromName.toLowerCase().replace(' ', '-');
  return str;
};
ComponentObject.prototype.getStyle = function(className) {
  var classes = this.window.document.styleSheets[0].rules || this.window.document.styleSheets[0].cssRules;
  for (var i = 0; i < classes.length; i++) {
    if (classes[i].selectorText == className) {
      return classes[i];
    }
  }
};
ComponentObject.prototype.copyStyleToElement = function(cs, to) {
  for (var prop in cs) {
    if (cs[prop] != undefined && cs[prop].length > 0 && 
      typeof cs[prop] !== 'object' && typeof cs[prop] !== 'function' && 
      prop != parseInt(prop) ) {
      
      // Per current observation, cssText (which contains width and color) is copied directly as string;
      // which means, without string merging, either width or color is maintained.
      if (prop == 'cssText') {
        to.style[prop] = this.mergeCSSText([to.style[prop], cs[prop]]);
      } else {
        to.style[prop] = cs[prop];
      }
    }
  }
};
ComponentObject.prototype.createObjectFromCSSStr = function(str) {
  var obj = {};
  var properties = str.split(';');
  for(var i = 0; i < properties.length; i++){
    var property = properties[i].split(':');
    if(property.length == 2){
      obj[property[0].trim()] = property[1].trim();
    }
  }
  return obj;
}
ComponentObject.prototype.mergeCSSText = function(texts) {
  var result = {};
  for(var i in texts){
    var cssProperties = this.createObjectFromCSSStr(texts[i]);
    for (var attr in cssProperties) {
      result[attr] = cssProperties[attr];
    }
  }
  var s = '';
  for(var attr in result){
    s += attr + ':' + ' ' + result[attr] + '; ';
  }
  return s.trim();
};
// This function takes the existing class names of given element,
// and apply the class definitions in the parent document to this document
ComponentObject.prototype.applyStyleFromParentDocument = function(ele) {
  var classNames = ele.className.split(" ");
  for (var i = 0; i < classNames.length; i++) {
    var elementStyle = this.getStyle("." + this.htmlClassFromName(classNames[i]));
    if (elementStyle != undefined) {
      this.copyStyleToElement(elementStyle.style, ele);
    }
  }
};
// This is a specific function for the visibility of the paragraph known to this web component
ComponentObject.prototype.toggleClassVisibility = function (className, visible) {
  var normalizedClass = className;
  if (!normalizedClass.startsWith('.')) {
    normalizedClass = '.' + normalizedClass;
  }
  
  var eles = this.shadowRoot.querySelectorAll(normalizedClass);

  var flag = visible;
  
  if (flag == undefined && eles.length > 0) {
    flag = eles[0].style.display;        
    if (flag == 'none') {
      flag = 'block';
    } else {
      flag = 'none';
    }
  }
  
  for (var i = 0; i < eles.length; i++) {
    eles[i].style.display = flag;
  }
};

exports.ComponentObject = ComponentObject;