

$(document).ready(function(){
    console.log('✅ ajax-comment_replay_like_form loaded');

    $(document).on('click', '.comment_replay_like_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.comment_replay_like_form');
        
        var twittid = form.find("input[name='twittid'], #twittid").val();
        var commentid = form.find("input[name='commentid'], #commentid").val();
        var comment_replay_id = form.find("input[name='comment_replay_id'], #comment_replay_id").val();
        var replaytable = form.find("input[name='replaytable'], #replaytable").val();

        console.log("📤 Liking replay data:", { 
            twittid, 
            commentid, 
            comment_replay_id, 
            replaytable 
        });

        if (!comment_replay_id) {
            alert("خطا: شناسه ریپلای پیدا نشد!");
            return;
        }

        $.post({
            url: "/home/twitts/see_comments/like_comment_replays/",
            data: {
                twittid: twittid,
                commentid: commentid,
                comment_replay_id: comment_replay_id,
                replaytable: replaytable || 1
            },
            success: function(response) {
                console.log("✅ Success:", response);
                alert(response.message);

                $("#comment_replay_likes_number_" + response.comment_replay_id).html(response.comment_replay_likes_number);

                if (response.unliked === false) {
                    form.find('.comment_replay_like_form_submit').html('<i class="fa-solid fa-heart text-red-500 text-2xl"></i>');
                } else {
                    form.find('.comment_replay_like_form_submit').html('<i class="fa-regular fa-heart text-2xl"></i>');
                }
            },
            error: function(xhr) {
                console.error("Full Error:", xhr.responseText);
                alert("خطا در لایک کردن");
            }
        });
    });
});

