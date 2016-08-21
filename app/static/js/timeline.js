// 请求数据库一页的数据
var mytweets_page = 1;
var followedtweets_page = 1;
var notifications_page = 1;
var comments_page = 1;

$(document).ready(function(){
        path = window.location.pathname
        username_index = 2
        username = path.split('/')[username_index]
        mytweets_url = '/tweets/' + username + '?page=' + mytweets_page
        followedtweets_url = '/followedtweets/' + username + '?page=' + followedtweets_page
        notifications_url = '/notifications/' + username + '?page=' + notifications_page
        get(mytweets_url, mytweets_response);
        get(followedtweets_url, followedtweets_response);
        get(notifications_url, notifications_response);
        __main();
        // 页面加载完毕后js会向服务器发送一个ajax请求一页的微博数，服务器会从数据库拿一页的微博数返回，默认是20条。
        // 如果返回的微博没超过20的话，就不需要显示翻页按钮。
        // 下面的函数会做一个判断 ，决定隐藏还是显示翻页按钮。
        // 需要等页面的第一页微博加载完毕后再执行函数，所以做了一个延时。
        setTimeout(function(){pageturning_button_show_hide($('#id-div-mytweets'), $('#id-button-next-mytweets'))}, 3000)
        setTimeout(function(){pageturning_button_show_hide($('#id-div-followedtweets'), $('#id-button-next-followedtweets'))}, 3000)
        setTimeout(function(){pageturning_button_show_hide($('#id-div-notification'), $('#id-button-next-notifications'))}, 3000)
});

var __main = function() {
    setup();
    bindActions();
    $('#id-a-mytweets').click();

  }

var pageturning_button_show_hide = function (jquery_page_object, jquery_button_object){
    var entries_perpage = 20;
    if (jquery_page_object.children().length < 20 ) {
      jquery_button_object.hide()
    }else if (jquery_page_object.children().length == 20) {
      jquery_button_object.show()
    }
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
        single_tweet = $(this).closest(".singletweet")
        log('single_tweet', single_tweet)
        var tweet_id = single_tweet.data('id')
        log('tweet_id', tweet_id);
        comments_url = '/tweet/comments/' + tweet_id + '?page=' + comments_page
        if (single_tweet.find(".div-commentarea").children().length == 0){
          get(comments_url, comments_response);
          // 评论区展开后，评论按钮显示“收起评论”；评论区收起后，评论按钮显示“评论（评论数量）”
          single_tweet.find(".comments-toggle").toggle();
        }else {
          single_tweet.find(".div-commentarea").toggle("fast");
          single_tweet.find(".comments-toggle").toggle();
        }
      });

      $('#id-div-twitter').on('click', '.button-reposts', function(){
            // 转发区展开后，评论按钮显示“收起转发”
            single_tweet = $(this).closest(".singletweet")
            single_tweet.find(".div-repostarea").toggle("fast");
            single_tweet.find(".reposts-toggle").toggle();
        });

      $('#id-div-twitter').on('click', '.button-addcomment', add_newcomment);

      $('#id-div-twitter').on('click', '.button-addrepost', add_newrepost);

      $('#id-button-avatars').on('click', function() {
        $('.file-wrapper').toggle("slow");
      });

      $('#id-button-addpicture').on('click', function() {
        $('.upload-wrapper').toggle("slow");
      });

      $('#id-button-upload-avatar').on('click', function() {
        var fileTag = $('#id-input-file')[0];
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
                upload_avatar(file);
            }
        }
    });

    $('#id-button-upload-picture').on('click', function() {
      var fileTag = $('#id-input-file')[0];
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
              upload_picture(file);
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
      setTimeout(function(){$('.none').remove()}, timeout)
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
    for(var i = 0; i < t.length; i++){
      tweet = t[i];
        var comments = tweet.comments;
        var avatar_path = tweet.avatar;
        var comments_length = comments.length;
          template = tweet_template(avatar_path, tweet, comments_length);
      $('#id-div-mytweets').append(template)
                }
              }

var followedtweets_template = function(followed_tweets, host, visitor){
    var t = followed_tweets
      for(var i = 0; i < t.length; i++){
        tweet = t[i];
          var comments = tweet.comments;
          var avatar_path = tweet.avatar;
          var comments_length = comments.length;
          template = tweet_template(avatar_path, tweet, comments_length);
          $('#id-div-followedtweets').append(template)
                }
              }

var notifications_template = function(notifications, host, visitor){
  var t = notifications
  var words = '在微博@了你'
    for(var i = 0; i < t.length; i++){
      tweet = t[i].t
      var comments_length = tweet.comments.length
      var avatar_path = tweet.avatar
        var template = `
            <div class="well tweetbox clearfix">
              <span>
              ${t[i].sender_name} ${words}
              </span>
                ${tweet_template(avatar_path, tweet, comments_length)}
              </div>
              `;
        $('#id-div-notification').append(template)
        }
      }
