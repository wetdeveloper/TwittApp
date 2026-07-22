

$(document).ready(function(){
    console.log('✅ ajax_replay_on_comment_input_form loaded');

    $(document).on('click', '.replay_on_comment_input_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.replay_on_comment_input_form');
        
        var twittid = form.find("input[name='twittid'], #twittid").val();
        var commentid = form.find("input[name='commentid'], #commentid").val();
        var replay = form.find("#replay").val().trim();

        console.log("Replay data:", { twittid, commentid, replay });

        if (!twittid || !commentid) {
            alert("خطا: اطلاعات توییت یا کامنت پیدا نشد!");
            return;
        }

        if (!replay) {
            alert("لطفاً متن ریپلای را وارد کنید!");
            return;
        }

        var submitBtn = $(this);
        var originalText = submitBtn.text();
        submitBtn.prop('disabled', true).text('در حال ارسال...');

        $.post({
            url: "/home/twitts/leave_comment_replay/",
            data: {
                twittid: twittid,
                commentid: commentid,
                replay: replay
            },
            success: function(response) {
                console.log("✅ Success:", response);
                alert("✅ ریپلای با موفقیت ارسال شد!");
                form.find("#replay").val('');
                location.reload();
            },
            error: function(xhr) {
                console.error("❌ Error:", xhr);
                alert("خطا در ارسال ریپلای");
            },
            complete: function() {
                submitBtn.prop('disabled', false).text(originalText);
            }
        });
    });
});
EOF
