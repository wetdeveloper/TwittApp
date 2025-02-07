$(document).ready((function(){
    console.log('ajax-replay-on-replay-like-form')
    $(document.getElementsByClassName("replay_on_replay_like_form_submit")).on('click',function(e){
    // this=$(document.getElementsByClassName('comment_like_form_submit'))
    e.preventDefault();
    var twittid=$(this).closest('.replay_on_replay_like_form').find("#twittid").val()
    var liked_replay_id=$(this).closest('.replay_on_replay_like_form').find("#liked_replay_id").val() //id of the replay which we did replay on it.
    var replayid=$(this).closest('.replay_on_replay_like_form').find("#id").val()
    var comment_replay_id=$(this).closest('.replay_on_replay_like_form').find("#comment_replay_id").val();
    var replaytable=$(this).closest('.replay_on_replay_like_form').find("#replaytable").val();


    data={
        twittid:twittid,
        liked_replay_id:liked_replay_id,
        id:replayid,
        comment_replay_id:comment_replay_id,
        replaytable:replaytable,
        crossDomain: true,
        },
    $.post({
        type:'post',
        url:'/home/twitts/see_replay_on_replays/likereplaysonreplay/', // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
        data:data,
        success:function(response)
        {
            alert(response.message)
            document.getElementById('replay_on_replay_likes_number_'+data.id).innerHTML=response.replaysonreplaylikesnumber

            if(response.unliked==false){
                $('#replay_on_replay_like_form_'+data.id).find('.replay_on_replay_like_form').find('.replay_on_replay_like_form_submit').html("<h3 style='color:red'><i class='glyphicon glyphicon-heart'></i></h3>")
            }
            else if (response.unliked==true){
                $('#replay_on_replay_like_form_'+data.id).find('.replay_on_replay_like_form_submit').html("<h3><i class='glyphicon glyphicon-heart-empty'></i></h3>")
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
    
