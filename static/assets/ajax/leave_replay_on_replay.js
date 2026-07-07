
$(document).ready(function(){
    console.log('✅ ajax_replay_on_replay_input_form loaded');

    $(document).on('click', '.replay_on_replay_input_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.replay_on_replays_input_form');
        
        var comment_replay_id = form.find("#comment_replay_id").val();
        var id = form.find("#id").val();
        var twittid = form.find("#twittid").val();
        var replaytable = form.find("#replaytable").val();
        var replay = form.find("#replay").val().trim();

        console.log("📤 Sending:", { comment_replay_id, id, twittid, replaytable, replay });

        if (!replay) {
            alert("لطفاً متن ریپلای را وارد کنید!");
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
                console.error("Full Error:", xhr.responseText);
                alert("خطا در ارسال ریپلای");
            },
            complete: function() {
                submitBtn.prop('disabled', false).text('replay');
            }
        });
    });
});

