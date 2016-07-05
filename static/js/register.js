
         $(document).ready(function(){
            console.log('ready');
            var button = $('#id-button-newusr-submit');
            button.on('click', function(){
              console.log('click button');
              var username = $('#id-text-newusr-username').val();
              var password = $('#id-text-newusr-password').val();
              console.log('user', username, password);
              var account = {
                'username': username,
                'password': password
              };
              // JSON.stringify 可以把一个 object 转换为字符串
              var postData = JSON.stringify(account);
              console.log('JSON格式的数据是', postData)
              // get or post
              var request = {
                url: '/register',
                type: 'post',
                contentType: 'application/json',
                data: postData,
                success: function(r){
                  console.log(r);
                  // alert(r);
                  if(r.success) {
                    console.log('成功');
                    url = r.data
                    window.location.href = url
                  } else {
                    console.log('失败');
                  }
                  $('#id-p-info').text(r.message);
                }
              };
              $.ajax(request);
            });
         });
