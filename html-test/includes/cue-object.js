/**
 * Implementation of cue parent object which does similar timing as Python code. (Jeff's DayCue, LanternCue, Cue object and so on.)
 */
 
/**
 * Question: (cue) state management and timing should happen in only one place? Since it's the state of only one actual show; (or synchronized across all nodes); However, right now we seem to want timing and state management in Touch, active script browser, (and probably in show memory, too)
 *
 * The active script has a state, Touch patch has a state, and these does not necessarily correspond with the state of the show, if there is such a thing.
 *
 * Right now can we assume only one instance of the active script being loaded to control the show?
 */

// Do we want to make cue states and cue commands customizable on child classes?
//var cueCmds = ['LOAD', 'GO', 'PAUSE', 'RESET', 'UNLOAD']

// Note: need to keep the states in order when adding new states
var CueObject = function CueObject(events) {
  this.state = CueObject.cueStates[1];

  this.timelineState = '';
  this.currentTime = 0;
  
  this.events = events;
  this.scheduledEvents = {};
  
  this.remainingEvents = 0;
};

CueObject.cueStates = ['PAUSED', 'STOPPED', 'ACTIVE'];

/**
 * (Re)start execution from 'time' milliseconds
 */
CueObject.prototype.run = function(time) {
  var startTime = 0;
  if (time !== undefined) {
    startTime = time;
  }
  this.state = CueObject.cueStates[2];
  this.remainingEvents = 0;
  
  for (key in this.events) {
    if (this.events.hasOwnProperty(key)) {
      if (this.scheduledEvents.hasOwnProperty(key)) {
        clearTimeout(this.scheduledEvents[key].event);
      }
      
      var adjustedTime = this.events[key].time - startTime;
      if (adjustedTime > 0) {
        // Note: passing parameters to setTimeout like this may not work on all browsers, for example IE
        this.scheduledEvents[key] = { 
          event: setTimeout(this.executeCallback.bind(this), adjustedTime, key),
          remaining: adjustedTime,
          start: Date.now()
        }
        this.remainingEvents ++;
      }
    }
  }
  
  if (this.remainingEvents == 0) {
    this.state = CueObject.cueStates[1];
  }
};

CueObject.prototype.executeCallback = function(eventKey) {
  this.timelineState = this.events[eventKey].state;
  this.events[eventKey].callback();
  this.scheduledEvents[eventKey].remaining = -1;
  this.remainingEvents --;
  if (this.remainingEvents == 0) {
    this.state = CueObject.cueStates[1];
  }
};

CueObject.prototype.stop = function() {
  for (key in this.scheduledEvents) {
    if (this.scheduledEvents.hasOwnProperty(key)) {
      clearTimeout(this.scheduledEvents[key].event);
      this.scheduledEvents[key].remaining = -1;
    }
  }
  
  this.state = CueObject.cueStates[1];
  this.timelineState = '';
  this.currentTime = 0;
  this.remainingEvents = 0;
};

/**
 * Pause execution at 'time' milliseconds
 * TODO: Pause implementation
 */
CueObject.prototype.pause = function(time) { 
  if (this.state == CueObject.cueStates[2]) {
    var pauseTime = 0;
    if (time !== undefined) {
      console.log('Pause at arbitrary time not implemented yet.');
    } else {
      this.state = CueObject.cueStates[0];
      var currentTime = Date.now();
      
      for (key in this.scheduledEvents) {
        var newRemaining = this.scheduledEvents[key].start + this.scheduledEvents[key].remaining - currentTime;
        
        if (newRemaining > 0 && this.scheduledEvents[key].remaining != -1) {
          this.scheduledEvents[key].remaining = newRemaining;
          clearTimeout(this.scheduledEvents[key].event);
        }
      }
    }
  } else {
    console.log('Warning: current state of cue is not running; pause ignored.');
  }
};

CueObject.prototype.resume = function() {
  if (this.state == CueObject.cueStates[0]) {
    var self = this;
    for (key in this.scheduledEvents) {
      if (this.scheduledEvents[key].remaining > 0) {
        this.scheduledEvents[key].event = setTimeout(this.executeCallback.bind(this), this.scheduledEvents[key].remaining, key);
        this.scheduledEvents[key].start = Date.now();
      }
    }
    this.state = CueObject.cueStates[2];
  } else {
    console.log('Warning: current state of cue is not paused; resume ignored.')
  }
};

exports.CueObject = CueObject;