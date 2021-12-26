$(document).ready((function(){
    console.log('ajax-comment_replay_like_form')
    $(document.getElementsByClassName('comment_replay_like_form_submit')).on('click',function(e){
    e.preventDefault();
    var twittid=$(this).closest('.comment_replay_like_form').find("#twittid").val()
    var commentid=$(this).closest('.comment_replay_like_form').find("#commentid").val();
    var comment_replay_id=$(this).closest('.comment_replay_like_form').find("#comment_replay_id").val();
    var replaytable=$(this).closest('.comment_replay_like_form').find("#replaytable").val();
    console.log(`twittid:${twittid} , commentid:${commentid} , comment_replay_id:${comment_replay_id} ,
    replaytable:${replaytable}`)
    $.ajax({
        type:'post',
        url:"/home/twitts/see_comments/like_comment_replays/", 
        data:{
        twittid:twittid,
        commentid:commentid,
        comment_replay_id:comment_replay_id,
        replaytable:replaytable
        },
        success:function(response)
        {
            document.getElementById('comment_replay_like_form_'+response.comment_replay_id).innerHTML="<h3 style='color: red;'><i class='glyphicon glyphicon-heart'></i</h3>"
            var comment_replay_likes_number_tag=document.getElementById('comment_replay_likes_number_'+response.comment_replay_id)
            comment_replay_likes_number_tag.innerHTML=response.comment_replay_likes_number
            console.log(response.message)
            console.log('comment_replay_id'+response.comment_replay_id)
            console.log('comment replay likes number='+response.comment_replay_likes_number)
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



}));

    
