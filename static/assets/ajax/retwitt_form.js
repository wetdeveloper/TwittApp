$(document).ready((function(){
    console.log('ajax-retwitt_form')
    $(document.getElementsByClassName('retwitt_form_submit')).on('click',function(e){
    e.preventDefault();
    // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
    var twittid=$(this).closest('.retwitt_form').find("#twittid").val();
    $.ajax({
        type:'post',
        url:"/home/twitts/retwitt/",
        data:{
        twittid:twittid,
        crossDomain: true,
        },
        success:function(response)
        {
            alert(response['message']);
            location.reload()
        }

    })
    })}))