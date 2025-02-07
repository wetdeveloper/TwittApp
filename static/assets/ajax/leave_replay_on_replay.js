$(document).ready((function(){
    console.log('ajax_replay_on_replay_input_form')
    $(document.getElementsByClassName('replay_on_replay_input_form_submit')).on('click',function(e){
    // this=$(document.getElementsByClassName('comment_like_form_submit'))
    e.preventDefault();
    var comment_replay_id=$(this).closest('.replay_on_replays_input_form').find("#comment_replay_id").val()
    var id=$(this).closest('.replay_on_replays_input_form').find("#id").val()
    var twittid=$(this).closest('.replay_on_replays_input_form').find("#twittid").val()
    var replaytable=$(this).closest('.replay_on_replays_input_form').find("#replaytable").val()
    var replay=$(this).closest('.replay_on_replays_input_form').find('#replay').val()
    data={
        comment_replay_id:comment_replay_id,
        id:id,
        twittid:twittid,
        replaytable:replaytable,
        replay:replay,
        crossDomain: true,
        },
    $.post({

        type:'post',
        url:'/home/twitts/leave_replay_on_replays/', // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
        data:data,
        success:function(response)
        {
            alert(response.message)
            console.log(response.message)
        },
        error:function(error){
            console.log('message Error' + JSON.stringify(error));
        }  
        
    })
    });

}) )
    