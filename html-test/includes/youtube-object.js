var YoutubeObject = function YoutubeObject(apiKey, baseUrl) {
  this.apiKey = apiKey;
  if (this.apiKey === undefined) {
    this.apiKey = 'AIzaSyCe8t7PnmWjMKZ1gBouhP1zARpqNwHAs0s';
  }
  this.baseUrl = 'https://www.googleapis.com/youtube/v3/';
  if (baseUrl !== undefined) {
    this.baseUrl = baseUrl;
  }
};

YoutubeObject.prototype.youtubeKeyParser = function (url) {
  var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
  var match = url.match(regExp);
  if (match && match[7].length == 11){
    return match[7];
  } else {
    alert("Youtube video url incorrect");
  }
}

YoutubeObject.prototype.getYoutubeVideoUrl = function (serviceUrl, fetchIfNotExist, callback, onerror) {
  var data = new FormData();
  data.append('url', serviceUrl);
  data.append('fetchIfNotExist', fetchIfNotExist);
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/services/get-youtube-url', true);
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  //xhr.open('POST', 'http://the-archive.la/losangeles/services/get-youtube-url', true);
  
  //console.log(serviceUrl);
  
  xhr.onload = function () {
    if (callback !== undefined) {
      callback(this);
    }
  };
  xhr.onerror = function () {
    if (callback !== undefined) {
      onerror(this);
    }
  };
  xhr.send(data);
}

YoutubeObject.prototype.loadYoutubeVideoUrls = function (serviceUrls, callback, onerror) {
  var data = new FormData();
  data.append('urls', JSON.stringify(serviceUrls));
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', 'http://the-archive.la/losangeles/services/load-youtube-urls', true);
  
  xhr.onload = function () {
    if (callback !== undefined) {
      callback(this);
    }
  };
  xhr.onerror = function () {
    if (onerror !== undefined) {
      onerror(this);
    }
  };
  xhr.send(data);
}

YoutubeObject.prototype.requestYoutubeItem = function(options, nextPageToken, videoData, onDone, linkOnly, onePage, remaining) {
  var storeLinkOnly = typeof linkOnly !== 'undefined' ? linkOnly : true;
  var requestOnePage = typeof onePage !== 'undefined' ? onePage : false;
  var requestNum = typeof remaining !== 'undefined' ? remaining : undefined;
  
  if (!options.hasOwnProperty('query')) {
    console.log('Request word not specified, returned.');
    return;
  }
  var self = this;
  var listRequest = new XMLHttpRequest();
  listRequest.onreadystatechange = function() {
	if (listRequest.readyState == 4 && listRequest.status == 200) {
	  var result = JSON.parse(listRequest.responseText);
	  for (var i = 0; i < result.items.length; i++) {
	    if (storeLinkOnly) {
	      if (options.hasOwnProperty('videoIdPath')) {
	        // TODO: performance note: youtubeObject slows things down by eval
	        eval('var videoId = result.items[i].' + options.videoIdPath);
	        // For query: search, we can get channelId and playlistId, too
	        if (videoId !== undefined) {
	          videoData.push(videoId);
	        }
	      }
	    } else {
	      if (result.items[i].snippet.description[result.items[i].snippet.description.length-1] == ".")	      
            result.items[i].snippet.description = result.items[i].snippet.description.substring(0, result.items[i].snippet.description.length - 1);
          videoData.push(result.items[i]);
	    }
	  }
	  
	  if (requestNum !== undefined) {
	    requestNum -= result.items.length;
      }
      
	  if ((result.nextPageToken !== undefined && result.nextPageToken !== null) && !requestOnePage && (requestNum > 0 || requestNum === undefined)) {
		self.requestYoutubeItem(options, result.nextPageToken, videoData, onDone, storeLinkOnly, requestOnePage, requestNum);
	  } else {
	    if (onDone !== undefined) {
	      // we return the last result only, so for list/channel fetching, videoData can be relied upon while result cannot
	      onDone(result);
	    }
	  }
	}
  }
  
  // TODO: API key is hard coded in the function at this point
  var url = this.baseUrl + options.query + '?';
  var reservedOptions = ['key', 'query', 'videoIdPath']
  
  for (option in options) {
    if (! (option.toString() in reservedOptions)) {
      url += option.toString() + '=' + options[option] + '&';
    }
  }
  if (options.hasOwnProperty('key')) {
    url += 'key=' + options.key;
  } else {
    url += 'key=' + this.apiKey;
  }
  
  if (nextPageToken != undefined) {
	url += '&pageToken=' + nextPageToken;
  }
  
  listRequest.open('GET', url, true);
  listRequest.send();
  
  return url;
};

if (typeof exports !== 'undefined') {
  exports.YoutubeObject = YoutubeObject;
}