var add_newrepost = function(){
  parent_tweet = $(this).closest(".singletweet")
  var content = parent_tweet.find('.text-addrepost').val();
  var form = {
    'content': content,
  };
  log('form', form)
  var tweet_id = parent_tweet.data('id')
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/repost/add' + '/' + tweet_id;
  post(url, form, new_repost);
};

var new_repost = function(data){
  if(data.success) {
    parent_tweet.find('.text-addrepost').val('')
    var u = data.user
    var t = data.tweet;
    var avatar_path = u.avatar
    var comments_length = t.comments.length;
    template = tweet_template(avatar_path, tweet=t, comments_length)
    $('#id-div-mytweets').prepend(template);
    $('#id-a-mytweets').click();
    }else{
        log('请求失败');
      }
    };
