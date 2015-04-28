/**
 * ComponentObject is the parent class of web components, which includes basic component functions
 *
 * TODO: maybe better to have components inherit from two parent classes? One for HTMLElement, The other one for style related functions?
 *
 * Function:
 *   
 */

ComponentObject.prototype = Object.create(HTMLElement.prototype);

/**
 * The static functions for web components goes here
 */
ComponentObject.prototype.htmlClassFromName = function(fromName) {
  str = fromName.toLowerCase().replace(' ', '-');
  return str;
};
ComponentObject.prototype.getStyle = function(document, className) {
  var classes = document.styleSheets[0].rules || document.styleSheets[0].cssRules;
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
      
      to.style[prop] = cs[prop];
    }
  }
};
// This function takes the existing class names of given element,
// and apply the class definitions in the parent document to this document
ComponentObject.prototype.applyStyleFromParentDocument = function(ele) {
  var classNames = ele.className.split(" ");

  for (var i = 0; i < classNames.length; i++) {
    var elementStyle = this.getStyle(this.window.document, "." + this.htmlClassFromName(classNames[i]));

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

/**
 * Component object takes the template element of this page to operate on, 
 * and the parent document
 */
ComponentObject.prototype.constructor = function ComponentObject(template, thatDoc, window) {
    this.template = template;
    this.thatDoc = thatDoc;
    this.thisDoc = (this.thatDoc._currentScript || this.thatDoc.currentScript).ownerDocument;
    this.window = window;
};
 
// TODO: get element by id (querySelector/querySelectorAll) function?
ComponentObject.prototype.createdCallback = function() {
    this.shadowRoot = this.createShadowRoot();
    
    var clone = undefined;
    if (this.template) {
        clone = this.thatDoc.importNode(this.template, true);
    } else {
        console.log('ComponentObject: template does not exist.');
    }
    
    this.shadowRoot.appendChild(clone);
    
    // Append thisDoc to parent's importedDocs:
    // Note: This assumes the knowledge of window's scriptControl element name
    if (this.window.scriptControl.importedElements != undefined) {
        this.window.scriptControl.importedElements.push(this);
    }
};
ComponentObject.prototype.applyValueForElementAttr = function(ele, eleAttr, compParam) {
    if (compParam == undefined) {
        console.log('ComponentObject: component parameter does not exist.')
        return;
    } else if (this.hasAttribute(compParam)) {
        // double check this part:
        if (ele && ele.eleAttr) {
          ele.eleAttr = this.getAttribute(compParam);
        }
    } else {
        console.log('ComponentObject: attribute does not exist: ' + attr);
        return;
    }
};
ComponentObject.prototype.attributeChangedCallback = function(attr, oldVal, newVal) {
    console.log('ComponentObject: onAttributeChanged stub');
};
ComponentObject.prototype.htmlClassFromName = function(fromName) {
    str = fromName.toLowerCase().replace(' ', '-');
    return str;
};
ComponentObject.prototype.getStyle = function(document, className) {
    var classes = document.styleSheets[0].rules || document.styleSheets[0].cssRules;
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
            
            to.style[prop] = cs[prop];
        }
    }
};
// This function takes the existing class names of given element,
// and apply the class definitions in the parent document to this document
ComponentObject.prototype.applyStyleFromParentDocument = function(ele) {
    var classNames = ele.className.split(" ");

    for (var i = 0; i < classNames.length; i++) {
        var elementStyle = this.getStyle(window.document, "." + this.htmlClassFromName(classNames[i]));

        if (elementStyle != undefined) {
            this.copyStyleToElement(elementStyle.style, ele);
        }
    }
};
// Note: untested function
ComponentObject.prototype.applyStyleFromParentDocumentForClass = function (className) {
    var eles = this.shadowRoot.querySelectorAll('.' + className);
    for (var i = 0; i < eles.length; i++) {
        this.applyStyleFromParentDocument(eles[i]);
    }
};
// This is a specific function for the visibility of given class name
ComponentObject.prototype.toggleClassVisibility = function (className, visible, display = 'block') {
    var normalizedClass = className;
    if (!normalizedClass.startsWith('.')) {
        normalizedClass = '.' + normalizedClass;
    }
    
    var eles = this.shadowRoot.querySelectorAll(normalizedClass);

    var flag = visible;
    
    if (flag == undefined && eles.length > 0) {
        flag = eles[0].style.display;                
        if (flag == 'none') {
            flag = display;
        } else {
            flag = 'none';
        }
    }
    
    for (var i = 0; i < eles.length; i++) {
        eles[i].style.display = flag;
    }
};

var co = new ComponentObject(undefined, undefined);

exports.ComponentObject = ComponentObject;