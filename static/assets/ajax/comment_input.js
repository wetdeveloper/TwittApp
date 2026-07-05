

$(document).ready(function(){
    console.log('✅ ajax-comment_input_form loaded');

    $(document).on('click', '.comment_input_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.comment_input_form');
        var twittid = form.find("#twittid").val();
        var commentInput = form.find('#comment');
        var comment = commentInput.val().trim();

        if (!comment) {
            alert("لطفاً متن کامنت را وارد کنید!");
            commentInput.focus();
            return;
        }

        // غیرفعال کردن دکمه موقع ارسال
        var submitBtn = $(this);
        var originalText = submitBtn.text();
        submitBtn.prop('disabled', true).text('در حال ارسال...');

        $.post({
            url: '/home/twitts/leave_comments/',
            data: {
                twittid: twittid,
                comment: comment
            },
            success: function(response) {
                console.log("✅ Success:", response);
                
                // پیام موفقیت
                alert("✅ کامنت شما با موفقیت ثبت شد!");
                
                // پاک کردن فیلد
                commentInput.val('');
                
                // ریلود صفحه (برای دیدن کامنت جدید)
                // location.reload();
                
                // یا می‌تونی کامنت جدید رو بدون ریلود اضافه کنی (پیشرفته)
            },
            error: function(xhr) {
                console.error("❌ Error:", xhr);
                alert("❌ خطا در ارسال کامنت. دوباره تلاش کنید.");
            },
            complete: function() {
                // برگرداندن دکمه به حالت عادی
                submitBtn.prop('disabled', false).text(originalText);
            }
        });
    });
});

