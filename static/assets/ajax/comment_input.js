$(document).ready((function(){
    console.log('ajax-comment_input_form')
    $(document.getElementsByClassName('comment_input_form_submit')).on('click',function(e){
    e.preventDefault();
    var twittid=$(this).closest('.comment_input_form').find("#twittid").val()
    var comment=$(this).closest('.comment_input_form').find('#comment').val()
    data={
        twittid:twittid,
        comment:comment,
        crossDomain: true,
        },
    $.post({

        type:'post',
        url:'/home/twitts/leave_comments/', 
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
    