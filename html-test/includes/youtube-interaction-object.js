var YoutubeObject = function YoutubeObject() {
  
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