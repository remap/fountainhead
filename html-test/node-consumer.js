var Face = require('ndn-js').Face;
var Name = require('ndn-js').Name;
var Interest = require('ndn-js').Interest;
var Exclude = require('ndn-js').Exclude;
var UnixTransport = require('ndn-js').UnixTransport;

var excludeComponent = undefined;

var onData = function(interest, data) {
  console.log('Got data packet with name ' + data.getName().toUri());
  // -1 for CueID, -2 for timestamp
  excludeComponent = data.getName().get(-2);
  
  try {
    dataObject = JSON.stringify(JSON.parse(data.getContent().buf().toString('binary')));
    console.log("Data object: " + dataObject);
  } catch (error) {
    console.log('Data content: ' + data.getContent().buf().toString('binary'));
  }
  
  if (excludeComponent != undefined) {
    var exclude = new Exclude();
    exclude.appendAny();
    exclude.appendComponent(excludeComponent);
    interest.setExclude(exclude);
  }
  
  face.expressInterest(interest, onData, onTimeout);
};

var onTimeout = function(interest) {  
  face.expressInterest(interest, onData, onTimeout);
};

// Connect to the local forwarder with a Unix socket.
var face = new Face(new UnixTransport());

var name = new Name("/ndn/edu/ucla/remap/losatlantis/chocolate_cookie_show/cues");

// Instead of expressing interest periodically with setInterval, 
// we maintain one outstanding interest, and refresh it every 150ms
setTimeout(function () {
  var interest = new Interest(name);
  
  interest.setMustBeFresh(true);
  interest.setChildSelector(1);
  
  interest.setInterestLifetimeMilliseconds(150);
  face.expressInterest(interest, onData, onTimeout);
  
}, 100);
