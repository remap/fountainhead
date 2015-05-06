var URLPublisherFactory = function URLPublisherFactory(window, document) {
  this.Config = {
    xhrHost : 'http://archive-dev.remap.ucla.edu:5003/query',
  
    // Default prefix registered for window.face (createVideoControlComponent calls this if not already registered) 
    ndnPrefix: '/ndn/edu/ucla/remap/losatlantis'
  };
  
  this.document = document;
  this.window = window;
};

/**
 * Create and register a web component of given name, which queries a given table in 
 * the database, selects an URL, and publish that URL under given name when clicked
 *
 * For example, the name for published content: [Config.ndnPrefix]/[ndnSuffix]/<version>
 * The suffix usually consists of 'ritual/1A/1A_sunset_1/url'.
 *
 * @param componentName String name of the component
 * @param ndnSuffix String suffix of the NDN name, appended after Config.ndnPrefix
 * @param urlTableName String table name which the backend should query
 * @param window The Window object of the parent page (from which environment variables should be accessed)
 * @param document The document object of the parent page
 */
 
URLPublisherFactory.prototype.createVideoControlComponent = function (componentName, ndnSuffix, urlTableName, textElementId, chunkElementId) {
  var thatDoc = this.document;
  var window = this.window;
  
  var thisDoc =  (thatDoc._currentScript || thatDoc.currentScript).ownerDocument;
  var template = thisDoc.querySelector('template').content;

  var VideoControlElement = Object.create(HTMLElement.prototype);
  
  var ndnPrefix = this.Config.ndnPrefix;
  var xhrHost = this.Config.xhrHost;
  
  VideoControlElement.createdCallback = function() {
    var shadowRoot = this.createShadowRoot();
    var clone = thatDoc.importNode(template, true);
    shadowRoot.appendChild(clone);
    
    this.innerElement = shadowRoot.querySelector(textElementId);
    this.chunkElement = shadowRoot.querySelector(chunkElementId);
    
    if (Name === undefined || Name === null) {
      console.log(componentName + ': Name is undefined; include ndn-js?');
      return;
    }
  
    if (this.hasAttribute('description')) {
      this.innerElement.textContent = this.getAttribute('description');
    } else {
      console.log(componentName + ': description is not defined for video control component, using default description');
      this.innerElement.textContent = 'Default description for ' + componentName + '.';
    }
  
    // Styling for text and chunk element
    this.applyStyleFromParentDocument(this.innerElement);
    this.applyStyleFromParentDocument(this.chunkElement);
  
    // TODO: Face setup's different from the online version, which hardcoded the server's IP address.
    if (this.hasAttribute('face')) {
      this.face = this.getAttribute('face');
    } else if (window.face !== undefined && window.face !== null) {
      this.face = window.face;
    } else {
      console.log(componentName + ': face is not defined, creating new one for window');
      window.face = new Face();
      this.face = window.face;
    }
  
    // Note: very weird that here I can't seem to set this.prefix...
    if (this.hasAttribute('prefix')) {
      this.namePrefix = this.getAttribute('prefix');
    } else if (window.prefix !== undefined && window.prefix !== null) {
      this.namePrefix = window.prefix;
    } else {
      console.log(componentName + ': prefix is not defined for sunset URL publishing, creating default name for window');
      window.prefix = new Name(ndnPrefix);
      this.namePrefix = window.prefix;
    }
  
    if (this.hasAttribute('memoryContentCache')) {
      this.memoryContentCache = this.getAttribute('memoryContentCache');
    } else if (window.memoryContentCache !== undefined && window.memoryContentCache !== null) {
      this.memoryContentCache = window.memoryContentCache;
    } else {
      console.log(componentName + ': memoryContentCache is not defined, creating new one for window');
      window.memoryContentCache = new MemoryContentCache(this.face);
      this.memoryContentCache = window.memoryContentCache;
    }
  
    var registeredPrefix = this.face.getEntryForRegisteredPrefix(this.namePrefix);
    if (registeredPrefix == null || registeredPrefix == 0) {
      console.log("registeredPrefix is not found on Face, reregistering default prefix");
      this.memoryContentCache.registerPrefix(this.namePrefix, function (prefix) {
        console.log("Register failed for prefix.");
      });
    }
  
    if (this.hasAttribute('showid')) {
      this.showid = this.getAttribute('showid');
    } else if (window.showid !== undefined && window.showid !== null) {
      this.showid = window.showid;
    } else {
      console.log(componentName + ': showid is not defined for sunset URL publishing, creating default for window');
      window.showid = 'default';
      this.showid = window.showid;
    }
  
    // Queries the Cassandra database for related video links
    this.resultURLs = [];
    // videoURL is the random selected URL among all that's returned.
    this.videoURL = '';
    // right now we are not using youtube Data API for video thumbnails
    this.imgURL = '';
    // Javascript parser for getting key from youtube URL
    // ref: http://stackoverflow.com/questions/3452546/javascript-regex-how-to-get-youtube-video-id-from-url
    this.youtubeKeyParser = function (url) {
      var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
      var match = url.match(regExp);
      if (match && match[7].length == 11){
        return match[7];
      } else {
        console.log("Url incorrect");
      }
    }
    
    var self = this;
    
    var data = new FormData();
    data.append('query', 'select * from ' + urlTableName + ';');
    
    var xhr = new XMLHttpRequest();
    // Note: POST is using hardcoded URL with my test server; server currently set to accept request originated from all.
    // Note: seems that right now the random video URL should be chosen onLoad, instead of onClick; need to confirm
    xhr.open('POST', xhrHost, true);
    xhr.onload = function () {
      var result = JSON.parse(this.responseText);
      if (result !== undefined && result !== null && result.length > 0) {
        for (var i = 0; i < result.length; i++) {
          self.resultURLs.push(result[i][0]);
        }
      
        var index = Math.floor((Math.random() * (self.resultURLs.length)));
        self.videoURL = self.resultURLs[index];
        self.imgURL = 'http://img.youtube.com/vi/' + self.youtubeKeyParser(self.videoURL) + '/0.jpg';
        
        console.log(componentName + ': chosen URL: ' + self.videoURL);
      }
    };
    xhr.send(data);
    
    this.empty = false;
    // TODO: unique ID is not updated to the given window right now.
    // TODO: what happens when multiple producers.
  
    this.innerElement.addEventListener('click', function(){
      // Note: Right now we don't do randomize video onClick; for thumbnail display
      //var index = Math.floor((Math.random() * (self.resultURLs.length)));
      //self.videoURL = self.resultURLs[index];
      
      if (self.videoURL && self.videoURL != '') {
        var data = new Data(self.namePrefix);
        // Note: for now, the names are hard-coded, since namespace design is not fully discussed
        var suffixName = new Name(ndnSuffix);
        data.getName().append(self.showid).append(suffixName).appendVersion((new Date).getTime());
        if (!self.empty) {
          data.setContent(self.videoURL);
          self.empty = true;
        } else {
          data.setContent('');
          self.empty = false;
        }
        // TODO: Arbitrary data freshness period
        data.getMetaInfo().setFreshnessPeriod(2000);
        data.sign();
        
        console.log(data.getName().toUri());
        
        self.memoryContentCache.add(data);
        console.log('NDN content published. Name: ' + data.getName().toUri() + '; Content: ' + data.getContent().buf().toString());
      } else {
        console.log(componentName + ': no relevant entries found or loaded');
      }
    });
    
    // Added for example of chunk html display: 
    // We'll need a parameter interface for html chunk display
    this.innerElement.addEventListener('mouseover', function() {
      if (self.imgURL && self.imgURL != '') {
        self.chunkElement.innerHTML = '<img src=' + self.imgURL + '></img>';
      } else {
        console.log(componentName + ': no relevant thumbnail entries found or loaded');
      }
    });
    
    this.innerElement.addEventListener('mouseout', function() {
      self.chunkElement.innerHTML = '';
    });
    
  };
  // TODO: resolve duplication of these methods in here, OLF and chat style control.
  
  VideoControlElement.attributeChangedCallback = function(attr, oldVal, newVal) {
  
  };
  
  // Added methods for CSS styling
  VideoControlElement.htmlClassFromName = function(fromName) {
    str = fromName.toLowerCase().replace(' ', '-');
    return str;
  };
  VideoControlElement.getStyle = function(document, className) {
    var classes = document.styleSheets[0].rules || document.styleSheets[0].cssRules;
    for (var i = 0; i < classes.length; i++) {
      if (classes[i].selectorText == className) {
        return classes[i];
      }
    }
  };
  VideoControlElement.copyStyleToElement = function(cs, to) {
    for (var prop in cs) {
      if (cs[prop] != undefined && cs[prop].length > 0 && 
        typeof cs[prop] !== 'object' && typeof cs[prop] !== 'function' && 
        prop != parseInt(prop) ) {
        
        to.style[prop] = cs[prop];
      }
    }
  };
  // This function takes the existing class name of given element
  VideoControlElement.applyStyleFromParentDocument = function(ele) {
    var classNames = ele.className.split(" ");
    
    for (var i = 0; i < classNames.length; i++) {
      var elementStyle = this.getStyle(window.document, "." + this.htmlClassFromName(classNames[i]));
    
      if (elementStyle != undefined) {
        this.copyStyleToElement(elementStyle.style, ele);
      }
    }
  };
  // Note: untested function
  VideoControlElement.applyStyleFromParentDocumentForClass = function (className) {
    var eles = this.shadowRoot.querySelectorAll('.' + className);
    for (var i = 0; i < eles.length; i++) {
      this.applyStyleFromParentDocument(eles[i]);
    }
  };
  
  // Note: web component registered names should not begin with numeric characters;
  //     web component names should always have a dash. (https://github.com/divshot/ele-web/issues/22)
  //     web component names should not have slash in them.
  //window.sunsetElement = 
  thatDoc.registerElement(componentName, {
    prototype: VideoControlElement
  });
};

exports.URLPublisherFactory = URLPublisherFactory;