$(document).ready(function(){
    $('#register').on('submit', function(event){
        console.log($(this));
        let requestObj = {
            'firstName': $('#fname').val(),
            'lastName': $('#lname').val(),
            'pnum': $('#pnum').val(),
            'email': $('#email').val(),
            'pass': $('#pass').val(),
            'confirm_pass': $('#cpass').val()
        };

        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/add_user',
            error: function (xhr, ajaxOptions, thrownError) {
                $('#acct-exists').hide();
                $('#bad-pass').hide();
                if(xhr.status === 400){
                    $('#acct-exists').show();
                }else if(xhr.status === 405){
                    $('#bad-pass').show();
                }
            }
        }).done(function(data){
            $('#acct-creat').show();
            $('#acct-exists').hide();
            $('#bad-pass').hide();
            $('#register').trigger("reset");
        });

        event.preventDefault();
    });
})