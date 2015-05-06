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
 
/**
 * States: STOPPED, ACTIVE, PAUSED
 * Timeline position: UNLOADED, READY, WAIT_IN, FADE_IN, RUN, WAIT_OUT, FADE_OUT, WAIT_AF, COMPLETE
 * Cue command messages in NDN name: LOAD, GO, PAUSE, RESET, UNLOAD
 
    def trans_READY(self):    pass # UNLOADED/COMPLETE => READY  (PREP GOES HERE)
    def trans_GO(self):       pass # READY => WAIT_IN  (GO-SYNC AUTOFOLLOW HERE)
    def trans_FADE_IN(self):  pass # WAIT_IN => FADE_IN
    def trans_RUN(self):      pass # FADE_IN => RUN
    def trans_WAIT_OUT(self): pass # RUN => WAIT_OUT
    def trans_FADE_OUT(self): pass # WAIT_OUT => FADE_OUT
    def trans_WAIT_AF(self):  pass # FADE_OUT => WAIT_AF
    def trans_COMPLETE(self): pass # WAIT_AF => COMPLETE  (POST-CUE AUTOFOLLOW HERE)
 */
 
// Do we want to make cue states and cue commands customizable on child classes?
//var cueCmds = ['LOAD', 'GO', 'PAUSE', 'RESET', 'UNLOAD']

// Note: need to keep the states in order when adding new states
var cueStates = ['PAUSED', 'STOPPED', 'ACTIVE']

var CueObject = function CueObject(events) {
  this.state = cueStates[1];

  this.timelineState = '';
  this.currentTime = 0;
  
  this.events = events;
  this.scheduledEvents = {};
  
  this.remainingEvents = 0;
};

/**
 * (Re)start execution from 'time' milliseconds
 */
CueObject.prototype.run = function(time) {
  var startTime = 0;
  if (time !== undefined) {
    startTime = time;
  }
  this.state = cueStates[2];
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
    this.state = cueStates[1];
  }
};

CueObject.prototype.executeCallback = function(eventKey) {
  this.timelineState = this.events[eventKey].state;
  this.events[eventKey].callback();
  this.scheduledEvents[eventKey].remaining = -1;
  this.remainingEvents --;
  if (this.remainingEvents == 0) {
    this.state = cueStates[1];
  }
};

CueObject.prototype.stop = function() {
  for (key in this.scheduledEvents) {
    if (this.scheduledEvents.hasOwnProperty(key)) {
      clearTimeout(this.scheduledEvents[key].event);
      this.scheduledEvents[key].remaining = -1;
    }
  }
  
  this.state = cueStates[1];
  this.timelineState = '';
  this.currentTime = 0;
  this.remainingEvents = 0;
};

/**
 * Pause execution at 'time' milliseconds
 * TODO: Pause implementation
 */
CueObject.prototype.pause = function(time) { 
  console.log('Pause called');
  if (this.state == cueStates[2]) {
    var pauseTime = 0;
    if (time !== undefined) {
      console.log('Pause at arbitrary time not implemented yet.');
    } else {
      this.state = cueStates[0];
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
  if (this.state == cueStates[0]) {
    var self = this;
    for (key in this.scheduledEvents) {
      if (this.scheduledEvents[key].remaining > 0) {
        this.scheduledEvents[key].event = setTimeout(this.executeCallback.bind(this), this.scheduledEvents[key].remaining, key);
        this.scheduledEvents[key].start = Date.now();
      }
    }
    this.state = cueStates[2];
  } else {
    console.log('Warning: current state of cue is not paused; resume ignored.')
  }
};

exports.CueObject = CueObject;


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