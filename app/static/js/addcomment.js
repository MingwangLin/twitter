var add_newcomment = function(){
  parent_tweet = $(this).closest(".singletweet")
  var content = parent_tweet.find(".text-addcomment").val();
  var form = {
    'content': content,
  };
  log('content', content)
  log('pt', parent_tweet)
  var tweet_id = parent_tweet.data('id')
  log('tid', tweet_id)
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/comment/add' + '/' + tweet_id;
  post(url, form, new_comment);
};

var new_comment = function(data){
  if(data.success) {
    parent_tweet.find(".text-addcomment").val('')
    var t = data.comment;
    var u = data.user
    var template = `
                    <hr />
                    <div class="well well-sm clearfix" data-id="${t.id}">
                        ${u.username} · ${formatted_time(t.created_time)}
                        <br>
                        ${t.content}
                    </div>
                    `;
        parent_tweet.find(".div-commentarea").prepend(template);
        }else {
        log('请求失败');
      }
    };
