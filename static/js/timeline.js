
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
                  console.log('success', t.content);

                  // for(var i = 0; i < r.length; i++){
                    var tag =t.content + ' --' + t.time + '<br>' + '<br>';
                    $('#id-div-tweet').prepend(tag);

                  }
              };

              $.ajax(request);
            });
          });