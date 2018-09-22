$(document).ready(function(){
    $('#add-gear').hide();
    $('#add-donation').on('submit', function(event){

        let requestObj = {
            'pnum': $('#donation-pnum').val()
        };

        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/add_donation',
            error: function (xhr, ajaxOptions, thrownError) {
                if(xhr.status === 404){
                    $('#acct-dne').show();
                    $('#donate-success').hide();
                }
            }
        }).done(function(data){
            $('#acct-dne').hide();
            $('#donate-success').show();
        });

        event.preventDefault();
    });

    $('#redeem-reward').on('submit', function(event){
        console.log($(this));
        let requestObj = {
            'pnum': $('#redeem-pnum').val(),
            'code': $('#redeem-code').val()
        };

        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/redeem_code',
            error: function (xhr, ajaxOptions, thrownError) {
                if(xhr.status === 404){
                    $('#code-success').hide();
                    $('#code-dne').show();
                }
            }
        }).done(function(data){
            $('#code-dne').hide();
            $('#code-success').show();
        });

        event.preventDefault();
    });
});