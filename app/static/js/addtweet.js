var add_newtweet = function(){
  var content = $('#id-text-content').val();
  var form = {
    'content': content,
  };
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/tweet/add';
  log('content', content)
  post(url, form, new_tweet);
}

var new_tweet = function(data){
  if(data.success) {
      $('#id-text-content').val('')
      var t = data.tweet;
      var u = data.user
      var avatar_path = u.avatar
      var comments = t.comments;
      var comments_length = comments.length;
      template = tweet_template(avatar_path, tweet=t, comments_length)
      $(template).hide().prependTo('#id-div-mytweets').show("slow");
}else {
  log('请求失败');
}
}
