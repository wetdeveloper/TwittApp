$(document).ready((function(){
    console.log('ajax-twitt_input_form')
    $(document.getElementsByClassName('comment_like_form_submit')).on('click',function(e){
   
    e.preventDefault();
    var twittid=$(this).closest('.comment_like_form').find("#twittid").val()
    var commentid=$(this).closest('.comment_like_form').find("#commentid").val();
    data={
        commentid:commentid,
        twittid:twittid,
        crossDomain: true,
        },
    $.post({
        type:'post',
        url:"/home/twitts/like_comment/", 
        success:function(response)
        {
            console.log(response.message)
            document.getElementById('comment_likes_number_'+data.commentid).innerHTML=response.comment_likes_number;
            document.getElementById('comment_like_form_'+data.commentid).innerHTML="<h3 style='color: red;'><i class='glyphicon glyphicon-heart'></i</h3>"
            console.log( 'comment likes number='+response.comment_likes_number)
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
    