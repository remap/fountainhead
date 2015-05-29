/**
 * ComponentObject is the parent class of web components, which includes basic component functions
 *
 * Function:
 *   
 * @param self The web component element created from HTMLElement
 * @param window The parent window of the web component
 */

var ComponentObject = function ComponentObject(document, window) {
  this.window = window;
  this.document = document;
};

ComponentObject.prototype.createComponent = function(componentName, createdCallback, attributeChangedCallback) {
  var thatDoc = document;
  var thisDoc = (thatDoc._currentScript || thatDoc.currentScript).ownerDocument;
  if (thisDoc.querySelector('template') === null) {
    console.log('Warning: createComponent halted because of no <template> in this document');
    return;
  }
  var template = thisDoc.querySelector('template').content;
  
  var element = Object.create(HTMLElement.prototype);
  var self = this;
  
  element.createdCallback = function() {
    this.shadowRoot = this.createShadowRoot();
    var clone = thatDoc.importNode(template, true);
    this.shadowRoot.appendChild(clone);
    
    this.componentObject = self;
    
    var createdSelf = this;
    
    this.toggleClassVisibility = function (className, visible) {
      var normalizedClass = className;
      if (!normalizedClass.startsWith('.')) {
        normalizedClass = '.' + normalizedClass;
      }
  
      var eles = createdSelf.shadowRoot.querySelectorAll(normalizedClass);

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
    
    this.getAttributeByListName = function (listAlias, defaultValue) {
      for (var i = 0; i < listAlias.length; i++) {
        if (this.hasAttribute(listAlias[i])) {
          return this.getAttribute(listAlias[i]);
        }
      }
      var ret = null;
      if (defaultValue !== undefined) {
        ret = defaultValue;
      }
      return ret;
    };
    
    createdCallback(this);
    
    if (self.window.scriptControl.importedElements != undefined) {
      self.window.scriptControl.importedElements.push(this);
    } else {
      console.log('Warning: scriptControl on window not defined; createdElement may not be accessible from parent document');
    }
  };
  element.attributeChangedCallback = function(attr, oldVal, newVal) {
    if (attributeChangedCallback !== undefined) {
      attributeChangedCallback(attr, oldVal, newVal);
    }
  };
  thatDoc.registerElement(componentName, {
    prototype: element
  });
};

/**
 * Styling functions for general web components goes here
 */
ComponentObject.prototype.applyStyleFromParentDocumentAll = function(createdElement) {
  var all = createdElement.shadowRoot.querySelectorAll('*');
  
  for (var i = 0; i < all.length; i++) {
    this.applyStyleFromParentDocument(all[i]);
  }
};
 
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
  for(var attr in result) {
    s += attr + ':' + ' ' + result[attr] + '; ';
  }
  return s.trim();
};
// This function takes the existing class names of given element,
// and apply the class definitions in the parent document to this document
// TODO: This class does not recognize styling options per element type, or element types in classes/divs
//   (such as divid > p)
ComponentObject.prototype.applyStyleFromParentDocument = function(ele) {
  var classNames = ele.className.split(" ");
  for (var i = 0; i < classNames.length; i++) {
    var elementStyle = this.getStyle("." + this.htmlClassFromName(classNames[i]));
    if (elementStyle != undefined) {
      this.copyStyleToElement(elementStyle.style, ele);
    }
  }
};
// This desanitizes texts such as sent chat messages, so that they get interpreted correctly on receiving side as html tags;
// Reverse operation of similar call in Python
ComponentObject.prototype.desanitizeText = function (text) {
  return text.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#32;/g, ' ').replace(/&#34;/g, '\"').replace(/&#39;/g, '\'');
};

if (typeof exports !== 'undefined') {
  exports.ComponentObject = ComponentObject;
}