
$(document).ready(function(){
    console.log('✅ ajax_replay_on_replay_input_form loaded');

    $(document).on('click', '.replay_on_replay_input_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.replay_on_replays_input_form');
        
        // جستجوی قوی‌تر برای فیلدها
        var comment_replay_id = form.find("input[name='comment_replay_id'], #comment_replay_id").val();
        var id = form.find("input[name='id'], #id").val();
        var twittid = form.find("input[name='twittid'], #twittid").val();
        var replaytable = form.find("input[name='replaytable'], #replaytable").val() || "1";
        var replay = form.find("#replay").val().trim();

        console.log("📤 Sending Replay Data:", { 
            comment_replay_id, 
            id, 
            twittid, 
            replaytable, 
            replay 
        });

        if (!replay) {
            alert("لطفاً متن ریپلای را وارد کنید!");
            return;
        }

        if (!twittid || !comment_replay_id) {
            alert("خطا: اطلاعات ناقص است. صفحه را رفرش کنید.");
            return;
        }

        var submitBtn = $(this);
        submitBtn.prop('disabled', true).text('در حال ارسال...');

        $.post({
            url: '/home/twitts/leave_replay_on_replays/',
            data: {
                comment_replay_id: comment_replay_id,
                id: id,
                twittid: twittid,
                replaytable: replaytable,
                replay: replay
            },
            success: function(response) {
                console.log("✅ Success:", response);
                alert(response.message || "ریپلای ارسال شد!");
                form.find("#replay").val('');
                location.reload();
            },
            error: function(xhr) {
                console.error("❌ Server Error:", xhr.responseText);
                alert("خطا در ارسال. جزئیات در کنسول.");
            },
            complete: function() {
                submitBtn.prop('disabled', false).text('replay');
            }
        });
    });
});

