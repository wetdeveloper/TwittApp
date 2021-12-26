$(document).ready((function(){
            console.log('ajax-twitt_input_form')
            $(document).on('submit','#twitt_input_form',function(e){
            e.preventDefault();
            $.post({
                type:'post',
                url:"/home/twitts/twitt_it/", // when you use ajax external for flask as external file,don't use url_for.it's just ok when you use ajax as internal file
                data:{
                twitt_text:$("input[name='twitt_text']").val(),
                start:"{{start}}",
                crossDomain: true,
                },
                success:function(response)
                {
                    console.log(response)
                    location.reload()
                   
                },
                error:function(error){
                    console.log('message Error' + JSON.stringify(error));
                }  
            })
            });

            ///////////////////////////Config CSRF
            var csrftoken = $('meta[name=csrf-token]').attr('content')
            $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
            })
            //////////////////////////End

}) )
            