
$(document).ready(function(){
    $('#login').on('submit', function(event){
        console.log($(this));
        let requestObj = {
            'email': $('#email').val(),
            'pass': $('#pass').val()
        };

        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/check_user',
            error: function (xhr, ajaxOptions, thrownError) {
                if(xhr.status === 400){
                    $('#acct-dne').show();
                }
            }
        }).done(function(data){
            window.location.replace('/home');
        });
        event.preventDefault();
    });
});