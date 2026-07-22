
$(document).ready(function(){
    console.log('✅ ajax-retwitt_form loaded');

    $(document).on('click', '.retwitt_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.retwitt_form');
        var twittid = form.find("#twittid").val();

        if (!twittid) {
            alert("خطا: توییت پیدا نشد!");
            return;
        }

        // غیرفعال کردن دکمه
        var submitBtn = $(this);
        var originalText = submitBtn.text();
        submitBtn.prop('disabled', true).text('در حال ری‌توییت...');

        $.post({
            url: "/home/twitts/retwitt/",
            data: {
                twittid: twittid
            },
            success: function(response) {
                console.log("✅ Retweet Success:", response);
                alert(response.message || response['message'] || "ری‌توییت شد!");
                location.reload();  // صفحه ریلود میشه تا ری‌توییت جدید دیده بشه
            },
            error: function(xhr) {
                console.error("❌ Retweet Error:", xhr);
                alert("خطا در ری‌توییت. دوباره تلاش کنید.");
            },
            complete: function() {
                // برگرداندن دکمه به حالت اولیه
                submitBtn.prop('disabled', false).text(originalText);
            }
        });
    });
});

