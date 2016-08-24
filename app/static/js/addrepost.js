var add_newrepost = function(){
  var $tweet = $(this).closest(".singletweet")
  var $repost_input = $tweet.children('.div-interact-area').find('.text-addrepost')
  var content = $repost_input.val();
  var form = {
    'content': content,
  };
  log('form', form)
  var tweet_id = $tweet.data('id')
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/repost/add' + '/' + tweet_id;
  post(url, form, new_repost, $repost_input);
};

var new_repost = function(data, $object){
  if(data.success) {
    $object.val('')
    var u = data.user
    var tweet = data.tweet;
    var avatar_path = u.avatar
    var comments_length = tweet.comments_length;
      template = tweet_template(avatar_path, tweet, comments_length)
    // $('#id-div-mytweets').prepend(template);
    $('#id-a-mytweets').click();
    $(template).hide().prependTo('#id-div-mytweets').fadeIn("slow");
    }else{
        log('请求失败');
      }
    };
