$(document).ready((function(){
    // follow
    console.log('ajax-follow-unfollow')
    $(document.getElementsByClassName('follow_button')).on('click',function(e){
    e.preventDefault();
    var followingtarget=$(this).closest('.following_form').find("input[name='followingtarget']").val()
    console.log(followingtarget)
    $.post({
        type:'post',
        url:'/home/twitts/follow/',
        data:{
        followingtarget:followingtarget,
        crossDomain: true,
        },
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

    // unfollow
    $(document.getElementsByClassName('unfollow_button')).on('click',function(e){
    e.preventDefault();
    var unfollowingtarget=$(this).closest('.unfollowing_form').find("input[name='unfollowingtarget']").val()
    var unfollower=$(this).closest('.unfollowing_form').find("input[name='unfollower']").val()
    $.post({
        type:'post',
        url:'/home/twitts/unfollow/',
        data:{
            unfollowingtarget:unfollowingtarget,
            unfollower:unfollower,
            crossDomain: true
        }
        ,
        success:function(response)
        {
            console.log(response.message)
            alert(response.message)
           
        },
        error:function(error){
            console.log('message Error' + JSON.stringify(error));
        }  
    })}

)}))
