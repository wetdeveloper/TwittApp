
$(document).ready(function(){
    console.log('✅ ajax-twitt_like_form loaded');

    $(document).on('click', '.twitt_like_form_submit', function(e){
        e.preventDefault();

        var form = $(this).closest('.twitt_like_form');
        var twittid = form.find("#twittid").val() || form.find("input[name='twittid']").val();

        console.log("Liking twittid:", twittid);

        if (!twittid) {
            alert("خطا: شماره توییت پیدا نشد!");
            return;
        }

        $.post({
            url: "/home/twitts/like_twitt/",
            data: {
                twittid: twittid
            },
            success: function(response) {
                console.log("✅ Like Success:", response);
                alert(response.message);

                // به‌روزرسانی تعداد لایک
                $("#twitt_likes_number_" + twittid).html(response.twitt_likes_number);

                // تغییر آیکون قلب (با Font Awesome)
                if (response.unliked === false) {
                    form.find('.twitt_like_form_submit').html('<i class="fa-solid fa-heart text-red-500 text-2xl"></i>');
                } else {
                    form.find('.twitt_like_form_submit').html('<i class="fa-regular fa-heart text-2xl"></i>');
                }
            },
            error: function(xhr) {
                console.error("Error:", xhr);
                alert("خطا در لایک کردن توییت");
            }
        });
    });
});

