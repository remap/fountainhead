// This prototype knows the structure of the database in the backend

var DBObject = function DBObject(hostUrl) {
  this.hostUrl = hostUrl;
  if (hostUrl == undefined) {
    this.hostUrl = 'http://archive-dev.remap.ucla.edu/app';
  }
  
  this.getFirstTransferUrl = this.hostUrl + '/querydb/get-first-transfer';
  this.genericQueryUrl = this.hostUrl + '/query';
};

// param @encoding, the result encoding for session.execute used by the backend; supported json, pickle, and str
DBObject.prototype.postToDB = function (queryStr, successCallback, encoding) {
  var data = new FormData();
  data.append('query', queryStr);
  
  if (encoding === undefined) {
    encoding = 'json';
  }
  data.append('encoding', encoding);
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', this.genericQueryUrl, true);
  xhr.onload = function () {
    successCallback(this.responseText);
  };
  xhr.send(data); 
};

DBObject.prototype.queryParticipant = function (participantObject, parts, whereClause, successCallback) {
  var queryParts = parts;
  if (parts === undefined) {
    queryParts = 'username, first_name, last_name, hashtags, photo_file, favorite_angeleno, favorite_time_of_day, neighborhood, email';
  }
  var queryStr = 'select ' + queryParts + ' from participant';
  var queryWhereClause = whereClause;
  if (queryWhereClause !== undefined) {
    queryStr += ' where ' + whereClause;
  }
  this.postToDB(queryStr, function(response) {
    successCallback(response);
  });
};

// Queries the DB for specific event names in a specific show, and pass the filtered results to callback.
DBObject.prototype.queryShowEvents = function (showId, eventName, callback) {
  var queryStr = 'select unixTimestampOf(event_id), act, params, participants, show_id from events_log where name = \'' + eventName + '\'';
  
  this.postToDB(queryStr, function (responseText) {
    if (responseText != '') {
      try {
        var resultObj = JSON.parse(responseText);
        var filteredObj = [];
        
        if (resultObj.length > 0) {
          for (var i = 0; i < resultObj.length; i++) {
            if (resultObj[i][4] === showId || showId === undefined) {
              filteredObj.push(resultObj[i]);
            }
          }
        }
        callback(filteredObj);
      } catch (e) {
        console.log(e);
      }
    }
  }, 'json');
}

if (typeof exports !== 'undefined') {
  exports.DBObject = DBObject;
}