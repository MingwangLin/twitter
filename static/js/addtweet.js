
         $(document).ready(function(){
            console.log('ready');
            var button = $('#id-text-submit');
            button.on('click', function(){
              console.log('click button');
              var content = $('#id-text-content').val();
              console.log('content', content);
              var tweet = {
                'content': content,
              };
              // JSON.stringify 可以把一个 object 转换为字符串
              var postData = JSON.stringify(tweet);
              console.log('JSON格式的数据是', postData)
              // get or post
              var request = {
                url: '/tweet/add',
                type: 'post',
                contentType: 'application/json',
                data: postData,
                success: function(data){
                  console.log('success', data);
                  var t = data;

                  var template = `
                      <p>
                      ${t.content} --${t.created_time}
                      <br>
                      <a href="/tweet/update/${t.id}">编辑</a>
                      <a href="/tweet/delete/${t.id}">删除</a>
                      <a href="/tweets/${t.id}">评论</a>
                      <a href="/tweets/${t.id}">转发</a>
                      </p>
                  `;
                    $('#id-div-tweet').prepend(template);

                  }
              };

              $.ajax(request);
            });
          });