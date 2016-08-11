var comments_response = function(data){
  if(data.success) {
    var increment = 1
    comments_page += increment
    log('success', data);
    var comments = data.comments;
    log('comments', comments)
    comments_template(comments);
  }else {
    log('server error');
  }
};

var comments_template = function(comments){
    var t = comments
      single_tweet.find(".div-commentarea").append(addcomment_textarea_template);
      log('this',single_tweet)
        for(var i = 0; i < t.length; i++){
          var template = `
                <hr />
                <div class="well well-sm clearfix" data-id="${t[i].id}">
                  ${t[i].user_name} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                </div>
              `;
          single_tweet.find(".div-commentarea").append(template)
          }
        }
