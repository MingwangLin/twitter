var comments_response = function(data){
  if(data.success) {
    var increment = 1
    comments_page += increment
    log('success', data);
    var comments = data.comments;
    log('comments', comments)
    comments_template(comments);
  }else {
    log('请求失败');
  }
};

var comments_template = function(comments){
    var t = comments
    var addcomment_template = `
      <div id='id-div-addcomment'>
      <textarea name="content" id="id-text-comment" class="form-control" placeholder="评论点什么"></textarea>
      <button class="btn btn-default pull-right" id="id-button-addcomment">
      <span class="glyphicon glyphicon-send" aria-hidden="true">
      </span>
      评论
      </button>
      </div>
      `
      single_tweet.append(addcomment_template);
      log('this',single_tweet)
        for(var i = 0; i < t.length; i++){
          var template = `
                <div class="well" data-id="${t[i].id}">
                  ${t[i].user_name} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                </div>
                <hr/>
              `;
          $(this).parent().append(template)
          }
        }
