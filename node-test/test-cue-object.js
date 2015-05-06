var CueObject = require('cue-object').CueObject;

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
    if (testCue.state == cueStates[1]) {
      console.log('Cue execution done.');
    }
  }, 100);
