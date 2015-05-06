// Test of cue object timing/pause/resume in node
//export NODE_PATH=$NODE_PATH:/Users/zhehaowang/projects/fos/fountainhead/html-test/includes/

var CueObject = require('cue-object').CueObject;

// Sample test cue object.
function onLoad(param) {
  var currentTime = Date.now();
  console.log('onLoad:\t' + (currentTime - startTime) + ' since start; Param ' + param);
}

function onRun(param) {
  var currentTime = Date.now();
  console.log('onRun:\t' + (currentTime - startTime) + ' since start; Param ' + param);
}

var testEvents = {
  'load': {
    time: 1000,
    callback: function () {
      onLoad('test param');
    }, 
    state: 'loaded'
  },
  'run': {
    time: 2000,
    callback: function () {
      onRun('test run param');
    }, 
    state: 'running'
  }
};

var testCue = new CueObject(testEvents);
var startTime = Date.now();

testCue.run();
console.log('Started:\t' + startTime);

// Test stopping
/*
setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Stop: ' + (currentTime - startTime) + ' since start');
    testCue.stop();
  }, 250);
*/
// Test pause and resume
setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Pause:\t' + (currentTime - startTime) + ' since start');
    testCue.pause();
  }, 1250);

setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Resume:\t' + (currentTime - startTime) + ' since start');
    testCue.resume();
  }, 1500);
  
setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Pause:\t' + (currentTime - startTime) + ' since start');
    testCue.pause();
  }, 1750);

setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Resume:\t' + (currentTime - startTime) + ' since start');
    testCue.resume();
  }, 2000);
/*
setTimeout(
  function(){
    var currentTime = Date.now();
    console.log('Rerun:\t' + (currentTime - startTime) + ' since start');
    testCue.run();
  }, 2250);
*/
// Keep this running forever
setInterval(
  function(){
    if (testCue.state == CueObject.cueStates[1]) {
      console.log('Cue execution done.');
    }
  }, 100);
