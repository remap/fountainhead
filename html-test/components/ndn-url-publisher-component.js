Config = {
    xhrHost : 'http://archive-dev.remap.ucla.edu:5003/query',
  
    // Default prefix registered for window.face (createVideoControlComponent calls this if not already registered) 
    ndnPrefix: '/ndn/edu/ucla/remap/losatlantis'
};

// Turn a parameter string into an array
function JSONStringToArray(string) {
    var array = JSON.parse(string);
    return array;
}

// Name for published content: [Config.ndnPrefix]/[ndnSuffix]/<version>
// The suffix usually consists of 'ritual/1A/1A_sunset_1/url'

function createVideoControlComponent(componentName, ndnSuffix, urlTableName, window, document) {
    var thatDoc = document;
    var thisDoc =  (thatDoc._currentScript || thatDoc.currentScript).ownerDocument;
    var template = thisDoc.querySelector('template').content;

    var VideoControlElement = Object.create(HTMLElement.prototype);

    VideoControlElement.createdCallback = function() {
        var shadowRoot = this.createShadowRoot();
        var clone = thatDoc.importNode(template, true);
        shadowRoot.appendChild(clone);
    
        // We may not want to contain these in a paragraph at some point
        this.innerElement = shadowRoot.querySelector('p');
    
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
    
        if (this.hasAttribute('style')) {
            var style = this.getAttribute('style');
            this.innerElement.setAttribute("style", style);
        }
        else {
            this.innerElement.setAttribute("class", componentName);
        }
    
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
            window.prefix = new Name(Config.ndnPrefix);
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
        var self = this;
        
        var data = new FormData();
        data.append('query', 'select * from ' + urlTableName + ';');
        
        var xhr = new XMLHttpRequest();
        // Note: POST is using hardcoded URL with my test server; server currently set to accept request originated from all.
        // Note: seems that right now the random video URL should be chosen onLoad, instead of onClick; need to confirm
        xhr.open('POST', Config.xhrHost, true);
        xhr.onload = function () {
            var result = JSON.parse(this.responseText);
            if (result !== undefined && result !== null && result.length > 0) {
                for (var i = 0; i < result.length; i++) {
                    self.resultURLs.push(result[i][0]);
                }
            
                var index = Math.floor((Math.random() * (self.resultURLs.length)));
                self.videoURL = self.resultURLs[index];
                console.log('com-1a-sunset: chosen URL: ' + self.videoURL);
            }
        };
        xhr.send(data);
        
        this.empty = false;
        // TODO: unique ID is not updated to the given window right now.
        // TODO: what happens when multiple producers.
    
        this.innerElement.addEventListener('click', function(){
            var index = Math.floor((Math.random() * (self.resultURLs.length)));
            self.videoURL = self.resultURLs[index];
            
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
                console.log('com-1a-sunset: no relevant entries found or loaded');
            }
        });
    };
    VideoControlElement.attributeChangedCallback = function(attr, oldVal, newVal) {
    
    };
    // Note: web component registered names should not begin with numeric characters;
    //       web component names should always have a dash. (https://github.com/divshot/ele-web/issues/22)
    //       web component names should not have slash in them.
    //window.sunsetElement = 
    thatDoc.registerElement(componentName, {
        prototype: VideoControlElement
    });
}