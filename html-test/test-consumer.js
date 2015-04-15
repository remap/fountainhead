var Face = require('ndn-js').Face;
var Name = require('ndn-js').Name;
var Interest = require('ndn-js').Interest;
var Exclude = require('ndn-js').Exclude;
var UnixTransport = require('ndn-js').UnixTransport;

var excludeComponent = undefined;

var onData = function(interest, data) {
  console.log("Got data packet with name " + data.getName().toUri());
  excludeComponent = data.getName().get(-1);
  console.log(data.getContent().buf().toString('binary'));
  console.log(data.getMetaInfo().getFreshnessPeriod() + " ***");
};


var onTimeout = function(interest) {
  //console.log("Time out for interest " + interest.getName().toUri());
};

// Connect to the local forwarder with a Unix socket.
var face = new Face(new UnixTransport());

var name = new Name("/ndn/edu/ucla/remap/losatlantis/chocolate_cookie_show/");

setInterval(function () {
  var interest = new Interest(name);
  
  interest.setMustBeFresh(true);
  interest.setChildSelector(1);
  
  // TODO: exclusions like this is problematic since the timestamp is not the first component after the prefix
  /*
  if (excludeComponent != undefined) {
    var exclude = new Exclude();
    exclude.appendAny();
    exclude.appendComponent(excludeComponent);
    interest.setExclude(exclude);
    
    console.log(interest.getName().toUri());
  }
  */
  
  interest.setInterestLifetimeMilliseconds(150);
  face.expressInterest(interest, onData, onTimeout);
  
}, 100);
