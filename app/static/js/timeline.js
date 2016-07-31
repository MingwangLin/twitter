// 请求数据库一页的数据
var mytweets_page = 1;
var followedtweets_page = 1;
var notifications_page = 1;

$(document).ready(function(){
        username = $('#id-button-next-mytweets').attr('data-name');
        log('username', username)
        mytweets_url = '/tweets/' + username + '?page=' + mytweets_page
        followedtweets_url = '/followedtweets/' + username + '?page=' + followedtweets_page
        notifications_url = '/notifications/' + username + '?page=' + notifications_page
        show_tweets(mytweets_url, mytweets_response);
        show_tweets(followedtweets_url, followedtweets_response)
        show_notification(notifications_url, notifications_response)
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
      show_tweets(mytweets_url, mytweets_response)
    });
    $('#id-button-next-followedtweets').on('click', function(){
        followedtweets_url = '/followedtweets/' + username + '?page=' + followedtweets_page
        show_tweets(followedtweets_url, followedtweets_response);
    });
    $('#id-button-next-notifications').on('click', function(){
        var increment = 1
        followedtweets_page += increment
        notifications_url = '/notifications/' + username + '?page=' + notifications_page
        show_tweets(notifications_url, notifications_response);
    });

    $('#id-button-addtweet').on('click', add_newtweet);

};

var show_tweets = function(url,response){
  get(url, response);
}

var show_notification = function(url,response){
  get(url, response);
}

var mytweets_response = function(data){
  if(data.success) {
    var increment = 1
    mytweets_page += increment
    log('success', data);
    var tweets = data.tweets;
    if (tweets.length == 0) {
      $('#id-div-mypage').append(none_template)
      setTimeout(function(){$('p.nomore').remove()}, 1000)
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
    if (visitor.id === host.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                  <div class="well" id = "${i}">
                  ${host.username} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                  ${basic_template}
                </div>
                <hr />

                `;
                $('#id-div-mytweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                      <div class="well">
                        ${host.username} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        ${basic_template}
                      </div>
                      <hr />
                    `;
                $('#id-div-mytweets').append(template)
                }
                }
}


var followedtweets_template = function(followed_tweets, host, visitor){
    var t = followed_tweets
            for(var i = 0; i < t.length; i++){
                var template = `
                      <div class="well">
                        ${t[i].user_name} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        ${basic_template}
                      </div>
                      <hr/>
                    `;
                $('#id-div-followedtweets').append(template)
                }
              }

var notifications_template = function(notifications, host, visitor){
  var t = notifications
  var words = '在微博@了你'
    for(var i = 0; i < t.length; i++){
        var template = `
            <div class="well">
              ${t[i].sender_name} ${words}
                ${t[i].sender_name} · ${formatted_time(t[i].created_time)}
                <br>
                ${t[i].tweet_content}
                ${basic_template}
              </div>
              <hr/>
              `;
              log('at tem', template)
        $('#id-div-notification').append(template)
        }
      }

var basic_template = `<button class="btn btn-default pull-right" id="id-button-addtweet">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                        </span>
                        评论
                        </button>
                        <button class="btn btn-default pull-right" id="id-button-addtweet">
                        <span class="glyphicon glyphicon-share" aria-hidden="true">
                        </span>
                        转发
                      </button>`

var none_template = `<p class="nomore text-center">
                      <span class="glyphicon glyphicon-info-sign">
                      </span>
                      没有更多了
                    </p>
                    `
