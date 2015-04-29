/**
 * NDN publisher component object provides NDN publish functions
 *
 * Function:
 *   
 * @param self The web component element created from HTMLElement
 * @param window The parent window of the web component
 */

var NDNPublisherComponentObject = function NDNPublisherComponentObject(self, window) {
  this.componentSelf = self;
  this.window = window;
};

NDNPublisherComponentObject.prototype.parseParameters = function () {
  if (this.componentSelf.hasAttribute('face')) {
    this.face = this.componentSelf.getAttribute('face');
  } else if (this.window.face !== undefined && this.window.face !== null) {
    this.face = this.window.face;
  } else {
    console.log('NDNPublisherComponentObject: face is not defined, creating new one for window');
    this.window.face = new Face();
    this.face = this.window.face;
  }

  if (this.componentSelf.hasAttribute('prefix')) {
    this.namePrefix = this.componentSelf.getAttribute('prefix');
  } else if (this.window.prefix !== undefined && this.window.prefix !== null) {
    this.namePrefix = this.window.prefix;
  } else {
    console.log('NDNPublisherComponentObject: prefix is not defined for sunset URL publishing, creating default name for window');
    this.window.prefix = new Name(ndnPrefix);
    this.namePrefix = this.window.prefix;
  }

  if (this.componentSelf.hasAttribute('memoryContentCache')) {
    this.memoryContentCache = this.componentSelf.getAttribute('memoryContentCache');
  } else if (this.window.memoryContentCache !== undefined && this.window.memoryContentCache !== null) {
    this.memoryContentCache = this.window.memoryContentCache;
  } else {
    console.log('NDNPublisherComponentObject: memoryContentCache is not defined, creating new one for window');
    this.window.memoryContentCache = new MemoryContentCache(this.face);
    this.memoryContentCache = this.window.memoryContentCache;
  }

  var registeredPrefix = this.face.getEntryForRegisteredPrefix(this.namePrefix);
  if (registeredPrefix == null || registeredPrefix == 0) {
    console.log("registeredPrefix is not found on Face, reregistering default prefix");
    this.memoryContentCache.registerPrefix(this.namePrefix, function (prefix) {
      console.log("Register failed for prefix: " + prefix.toUri());
    });
  }
};

NDNPublisherComponentObject.prototype.publishContent = function (ndnName, content, appendVersion) {
  var data = new Data(ndnName);
  // Note: for now, the names are hard-coded, since namespace design is not fully discussed

  if (appendVersion) {
    data.getName().appendVersion((new Date).getTime());
  } else {
    
  }
  data.setContent(content);
  
  // TODO: Arbitrary data freshness period
  data.getMetaInfo().setFreshnessPeriod(2000);
  data.sign();
  
  this.memoryContentCache.add(data);
  console.log('NDN content published. Name: ' + data.getName().toUri() + '; Content: ' + data.getContent().buf().toString());
};
