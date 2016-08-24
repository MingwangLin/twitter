var tweet_template = function(avatar_path, tweet, comments_length){
  log('4', tweet)
  return template =
                `
                <div class="media list-group-item tweetbox">
                  <div class="media-left">
                      <a href="#">
                        <img class="media-object img-circle" src="${avatar_path}" alt="32x32" style="width: 32px; height: 32px;">
                      </a>
                  </div>
                  <div class="media-body clearfix singletweet" data-id="${tweet.id}">
                      <span class="font-small">
                        ${href_for_personalpage(tweet.user_name)} ·
                        <span class="font-small">
                        ${formatted_time(tweet.created_time)}
                        </span>
                      </span>
                      <br>
                      ${tweet.content}
                      ${reposted_tweet_template(tweet.original_tweet)}
                    <div class="div-interact-area">
                      <div class="btn-group bottom-right " role="group" aria-label="...">
                      <button type="button" class="btn btn-default btn-xs button-comments">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                        </span>
                        <span class="comment-button-text">评论${comments_length}</span>
                      </button>
                      <button type="button" class="btn btn-default btn-xs button-reposts">
                        <span class="glyphicon glyphicon-share" aria-hidden="true">
                        </span>
                        <span class="repost-button-text">转发</span>
                      </button>
                      </div>
                      <div class="clearfix div-repostarea" style="display: none">
                        ${addrepost_textarea_template}
                      </div>
                      <div class="clearfix div-commentarea" style="display: none">
                        ${addcomment_textarea_template}
                      </div>
                    </div>
                    <hr />
                  </div>
                </div>
                `
              };

var reposted_tweet_template = function(tweet){
  log('tweet3', tweet[0])
  if (tweet.length != 0) {
    comments_length = tweet[0].comments_length
    if (comments_length == 0) {
      comments_length = '';
    }
    return template =
                `
              <div class="media list-group-item well  clearfix">
                  <div class="media-left">
                    <a href="#">
                      <img class="media-object img-circle" src="${tweet[0].avatar}" alt="32x32" style="width: 28px; height: 28px;">
                    </a>
                  </div>
                  <div class="media-body singletweet clearfix" data-id="${tweet[0].id}">
                    <span class="font-smaller">
                      ${href_for_personalpage(tweet[0].user_name)} ·
                        <span class="font-smaller">
                          ${formatted_time(tweet[0].created_time)}
                        </span>
                    </span>
                    <p class="font-small">
                      ${tweet[0].content}
                    </p>
                    <div class="div-interact-area">
                      <div class="btn-group bottom-right" role="group" aria-label="...">
                        <button type="button" class="btn btn-default btn-xs button-comments">
                          <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                          </span>
                          <span class="comment-button-text">评论${comments_length}</span>
                        </button>
                        <button type="button" class="btn btn-default btn-xs button-reposts">
                          <span class="glyphicon glyphicon-share" aria-hidden="true">
                          </span>
                          <span class="repost-button-text">转发</span>
                        </button>
                      </div>
                      <div class="clearfix div-repostarea" style="display: none">
                        ${addrepost_textarea_template}
                      </div>
                      <div class="clearfix div-commentarea" style="display: none">
                        ${addcomment_textarea_template}
                      </div>
                    </div>
                    <hr />
                  </div>
              </div>
                `
              }else {
                return template = ``
              }

              };

var picture_gallery = function(url, index){
  return template =
                    `
                    <div class="img">
                      <a href="#">
                      <img src="${url}" data-url="${url}" alt="Trolltunga Norway" width="300" height="200">
                      </a>
                    </div>
                    `
                  }


var none_template = `<div class="none transbox">
                      <p class="text-center ">
                        你还未发表任何微博
                      </p>
                    </div>
                    `

var nomore_template = `<p class="nomore text-center">
                    <span class="glyphicon glyphicon-info-sign">
                    </span>
                    没有更多了
                    </p>
                    `
var addcomment_textarea_template = `
                      <hr />
                      <div class="input-group">
                      <input class="form-control text-addcomment" name="content" placeholder="评论点什么">
                      <span class="input-group-btn">
                      <button class="btn btn-default pull-right button-addcomment" type="button">
                      <span class="glyphicon glyphicon-send" aria-hidden="true">
                      </span>
                      发表评论
                      </button>
                      </span>
                      </div>
                      `
var addrepost_textarea_template = `
                      <hr />
                      <div class="input-group">
                      <input class="form-control text-addrepost" name="content" placeholder="说点什么">
                      <span class="input-group-btn">
                      <button class="btn btn-default pull-right button-addrepost" type="button">
                      <span class="glyphicon glyphicon-share" aria-hidden="true">
                      </span>
                      转发
                      </button>
                      </span>
                      </div>
                      `
