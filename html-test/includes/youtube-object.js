var YoutubeObject = function YoutubeObject(apiKey, baseUrl) {
  this.apiKey = apiKey;
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

YoutubeObject.prototype.getYoutubeVideoUrl = function (serviceUrl, fetchIfNotExist, callback) {
  var data = new FormData();
  data.append('url', serviceUrl);
  data.append('fetchIfNotExist', fetchIfNotExist);
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/services/get-youtube-url', true);
  
  xhr.onload = function () {
    callback(this);
  };
  xhr.send(data);
}

YoutubeObject.prototype.loadYoutubeVideoUrls = function (serviceUrls, callback) {
  var data = new FormData();
  data.append('urls', JSON.stringify(serviceUrls));
  
  var xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/query', true);
  xhr.open('POST', 'http://archive-dev.remap.ucla.edu/app/services/load-youtube-urls', true);
  
  xhr.onload = function () {
    callback(this);
  };
  xhr.send(data);
}

YoutubeObject.prototype.requestYoutubeItem = function(options, nextPageToken, videoLinks, onDone) {
  if (!options.hasOwnProperty('query')) {
    console.log('Request word not specified, returned.');
    return;
  }
  
  var self = this;
  var listRequest = new XMLHttpRequest();
  listRequest.onreadystatechange = function() {
	if (listRequest.readyState == 4 && listRequest.status==200) {
	  var result = JSON.parse(listRequest.responseText);
	  for (var i = 0; i < result.items.length; i++) {
	    if (options.hasOwnProperty('videoIdPath')) {
	      eval('var videoId = result.items[i].' + options.videoIdPath);
	      // For query: search, we can get channelId and playlistId, too
	      if (videoId !== undefined) {
	        videoLinks.push(videoId);
	      }
	    }
	  }
  
	  if (result.nextPageToken !== undefined && result.nextPageToken !== null) {
		self.requestYoutubeItem(options, result.nextPageToken, videoLinks, onDone);
	  } else {
	    if (onDone !== undefined) {
	      // we return the last result only, so for list/channel fetching, videoLinks can be relied upon while result cannot
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
};