// 请求数据库一页的数据
var mytweets_page = 1;
var followedtweets_page = 1;
var notifications_page = 1;
var comments_page = 1;


$(document).ready(function(){
        path = window.location.pathname
        log('path', path)
        username_index = 2
        username = path.split('/')[username_index]
        log('username', username)
        mytweets_url = '/tweets/' + username + '?page=' + mytweets_page
        followedtweets_url = '/followedtweets/' + username + '?page=' + followedtweets_page
        notifications_url = '/notifications/' + username + '?page=' + notifications_page
        get(mytweets_url, mytweets_response);
        get(followedtweets_url, followedtweets_response)
        get(notifications_url, notifications_response)
        __main()


});

var __main = function() {
    setup();
    bindActions();
    $('#id-a-mytweets').click();



};

var setup = function() {
    $('.blog-nav> a').on('click', function () {
              var self = $(this);
              $('.active').removeClass('active');
              self.addClass('active');
          });
    var tabAction = function (show_mytweets, show_followedtweets, show_notifications) {
        $('#id-div-mypage').toggle(show_mytweets);
        $('#id-div-followedpage').toggle(show_followedtweets);
        $('#id-div-notificationpage').toggle(show_notifications);
    };

    $('#id-a-mytweets').on('click', function() {
        var show_notifications = false;
        var show_followedtweets = false;
        var show_mytweets = true;
        tabAction(show_mytweets, show_followedtweets, show_notifications);
    });
    $('#id-a-followedtweets').on('click', function() {
        var show_notifications = false;
        var show_followedtweets = true;
        var show_mytweets= false;
        tabAction(show_mytweets, show_followedtweets, show_notifications);

    });
    $('#id-a-notifications').on('click', function() {
        var show_notifications = true;
        var show_followedtweets = false;
        var show_mytweets= false;
        tabAction(show_mytweets, show_followedtweets, show_notifications);
    });
};

var bindActions = function() {
    $('#id-button-next-mytweets').on('click', function(){
      var increment = 1
      mytweets_page += increment
      mytweets_url = '/tweets/' + username + '?page=' + mytweets_page
      log('m_url',mytweets_url )
      get(mytweets_url, mytweets_response)
    });

    $('#id-button-next-followedtweets').on('click', function(){
        followedtweets_url = '/followedtweets/' + username + '?page=' + followedtweets_page
        get(followedtweets_url, followedtweets_response);
    });

    $('#id-button-next-notifications').on('click', function(){
        var increment = 1
        followedtweets_page += increment
        notifications_url = '/notifications/' + username + '?page=' + notifications_page
        get(notifications_url, notifications_response);
    });

    $('#id-button-addtweet').on('click', add_newtweet);

    $('#id-div-twitter').on('click', '.button-comments', function(){
        single_tweet = $(this).parent()
        log('single_tweet', single_tweet)
        var tweet_id = single_tweet.data('id')
        log('tweet_id', tweet_id);
        comments_url = '/tweet/comments/' + tweet_id + '?page=' + comments_page
        if (single_tweet.find(".div-commentarea").children().length == 0){
          get(comments_url, comments_response);
        }else {
          single_tweet.find(".div-commentarea").toggle();
        }
      });

      $('#id-div-twitter').on('click', '.button-addcomment', add_newcomment);

          $('#id-button-upload').on('click', function() {
              var fileTag =$('#id-input-file')[0];
              log('fileTag', fileTag);
              var files = fileTag.files;
              log('files', files);
              var numberOfFiles = files.length;
              if(numberOfFiles == 0) {
                  alert('还没有选中文件');
              } else {
                  for (var i = 0; i < numberOfFiles; i++) {
                      var file = files[i];
                      console.log('上传的文件: ', file.name);
                      upload(file);
                  }
              }
          });
};

var mytweets_response = function(data){
  if(data.success) {
    var increment = 1
    mytweets_page += increment
    log('success', data);
    var tweets = data.tweets;
    if (tweets.length == 0 && $('#id-div-mytweets').children().length == 0){
      $('#id-div-mytweets').append(none_template)
      var timeout = 3000
      setTimeout(function(){$('p.none').remove()}, timeout)
    }else if (tweets.length == 0 && $('#id-div-mytweets').children().length > 0) {
      $('#id-div-mypage').append(nomore_template)
      var timeout = 1000
      setTimeout(function(){$('p.nomore').remove()}, timeout)
    }else {

      var host = data.host
      var visitor = data.visitor
      mytweets_template(tweets, host, visitor);
    }

}else {
  log('请求失败');
}
};

var followedtweets_response = function(data){
  if(data.success) {
    var increment = 1
    followedtweets_page += increment
    log('success', data);
    var followed_tweets = data.tweets;
    log('followed_tweets', followed_tweets)
    var host = data.host
    var visitor = data.visitor
    followedtweets_template(followed_tweets, host, visitor);
  }else {
    log('请求失败');
  }
};

var notifications_response = function(data){
  if(data.success) {
    var increment = 1
    notifications_page += increment
    log('at success', data);
    var notifications = data.notifications;
    var host = data.host
    var visitor = data.visitor
    notifications_template(notifications, host, visitor);
}else {
  log('请求失败');
}
};

var mytweets_template = function(tweets, host, visitor){
    var t = tweets
    var avatar_path = host.avatar
    for(var i = 0; i < t.length; i++){
      var comments = t[i].comments;
      log('comments1', comments);
      var comments_length = comments.length;
      log('comments_length1', comments_length);
      template = `
                    <div class="media">
                      <div class="media-left">
                        <a href="#">
                          <img class="media-object" src="${avatar_path}" alt="64x64" style="width: 48px; height: 48px;">
                        </a>
                      </div>
                      <div class="media-body clearfix singletweet" data-id="${t[i].id}">
                        ${href_for_personalpage(t[i].user_name)} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
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
                    `
                      ;
                $('#id-div-mytweets').append(template)
                }
}


var followedtweets_template = function(followed_tweets, host, visitor){
    var t = followed_tweets
            for(var i = 0; i < t.length; i++){
              var comments = t[i].comments;
              var comments_length = comments.length;
              log('comments_length', comments_length);
                var template = `
                <div class="media">
                <div class="media-left">
                <a href="#">
                <img class="media-object" src="/static/avatars/1.jpg" alt="64x64" style="width: 48px; height: 48px;">
                </a>
                </div>
                <div class="media-body clearfix singletweet" data-id="${t[i].id}">
                ${href_for_personalpage(t[i].user_name)} · ${formatted_time(t[i].created_time)}
                <br>
                ${t[i].content}
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
                `
                $('#id-div-followedtweets').append(template)
                }
              }

var notifications_template = function(notifications, host, visitor){
  var t = notifications
  var words = '在微博@了你'
    for(var i = 0; i < t.length; i++){
        var template = `
            <div class="well clearfix">
              <span>
              ${t[i].sender_name} ${words}
              </span>
                <div class="list-group-item clearfix singletweet"  data-id="${t[i].tweet_id}">
                  ${t[i].sender_name} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].tweet_content}
                  ${tweet_template}
                  </div>
              </div>
              <hr/>
              `;
        $('#id-div-notification').append(template)
        }
      }
