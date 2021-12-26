$(document).ready((function(){
    console.log('ajax_replay_on_comment_input_form')
    $(document.getElementsByClassName('replay_on_comment_input_form_submit')).on('click',function(e){
    // this=$(document.getElementsByClassName('comment_like_form_submit'))
    e.preventDefault();
    var twittid=$(this).closest('.replay_on_comment_input_form').find("#twittid").val()
    var commentid=$(this).closest('.replay_on_comment_input_form').find('#commentid').val()
    var replay=$(this).closest('.replay_on_comment_input_form').find('#replay').val()
    data={
        twittid:twittid,
        commentid:commentid,
        replay:replay,
        crossDomain: true,
        },
    $.post({

        type:'post',
        url:"/home/twitts/leave_comment_replay/", // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
        data:data,
        success:function(response)
        {
            console.log(response.message)
            alert(response.message)
        },
        error:function(error){
            console.log('message Error' + JSON.stringify(error));
        }  
        
    })
    });

}) )
    