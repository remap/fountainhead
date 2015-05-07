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

YoutubeObject.prototype.requestYoutubeItem = function(options, nextPageToken, videoLinks, onDone) {
  var listRequest = new XMLHttpRequest();
  
  if (!options.hasOwnProperty('query')) {
    console.log('Request word not specified, returned.');
    return;
  }
  
  if (!options.hasOwnProperty('videoIdPath')) {
    console.log('Option object does not have videoId JSON path for the fetched results.');
    return;
  }
  var self = this;
  listRequest.onreadystatechange = function() {
	if (listRequest.readyState == 4 && listRequest.status==200) {
	  var result = JSON.parse(listRequest.responseText);
	  for (var i = 0; i < result.items.length; i++) {
	    eval('var videoId = result.items[i].' + options.videoIdPath);
	    // For query: search, we can get channelId and playlistId, too
	    if (videoId !== undefined) {
	      videoLinks.push(videoId);
	    }
	  }
  
	  if (result.nextPageToken !== undefined && result.nextPageToken !== null) {
		self.requestYoutubeItem(options, result.nextPageToken, videoLinks, onDone);
	  } else {
	    if (onDone !== undefined) {
	      onDone(videoLinks);
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
