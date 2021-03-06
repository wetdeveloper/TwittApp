$(document).ready((function(){
    console.log('ajax-twitt_like_form')
    $(document.getElementsByClassName('twitt_like_form_submit')).on('click',function(e){
    // this=$(document.getElementsByClassName('comment_like_form_submit'))
    e.preventDefault();
    var twittid=$(this).closest('.twitt_like_form').find("#twittid").val()
    data={
        twittid:twittid,
        crossDomain: true,
        },
    $.post({
        type:'post',
        url:"/home/twitts/like_twitt/", // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
        data:data,
        success:function(response)
        {
            alert(response.message)
            document.getElementById('twitt_likes_number_'+data.twittid).innerHTML=response.twitt_likes_number
            if(response.unliked==false){
                
                $('#twitt_like_form_'+data.twittid).find('.twitt_like_form').find('.twitt_like_form_submit').html("<h3 style='color:red'><i class='glyphicon glyphicon-heart'></i></h3>")
            }
            else if (response.unliked==true){
                $('#twitt_like_form_'+data.twittid).find('.twitt_like_form').find('.twitt_like_form_submit').html("<h3><i class='glyphicon glyphicon-heart-empty'></i></h3>")
            }
            
        },
        error:function(error){
            console.log('message Error' + JSON.stringify(error));
        }  
        
    })
    });

    ///////////////////////////Config CSRF
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
    })
    //////////////////////////End

}) )
    
