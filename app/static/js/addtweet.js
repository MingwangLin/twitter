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
      var template = `
              <div class="media">
                <div class="media-left">
                  <a href="#">
                    <img class="media-object" src="${avatar_path}" alt="64x64" style="width: 48px; height: 48px;">
                  </a>
                </div>
                <div class="media-body clearfix singletweet" data-id="${t.id}">
                  ${href_for_personalpage(t.user_name)} · ${formatted_time(t.created_time)}
                  <br>
                  ${t.content}
                  <hr/>
                <button class="btn btn-default btn-xs pull-right button-comments">
                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                  </span>
                  评论${comments_length}
                </button>
                <button class="btn btn-default btn-xs pull-right id-button-retweets">
                  <span class="glyphicon glyphicon-share" aria-hidden="true">
                  </span>
                  转发
                </button>
                <div class="clearfix div-commentarea">
                </div>
                <hr />
              </div>
              </div>
          `;
        $('#id-div-mytweets').prepend(template);
}else {
  log('请求失败');
}
}
