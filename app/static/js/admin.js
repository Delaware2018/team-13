$(document).ready(function(){
    $('#admin').on('submit', function(event){
        console.log($(this));
        let requestObj = {
            'pnum': $('#pnum').val()
            'poll': false
            };

        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/add_points',
            error: function (xhr, ajaxOptions, thrownError) {
                $('#points_add').hide();
                $('#acct-not-exists').show();
            }
        }).done(function(data){
            $('#points_add').show();
            $('#acct-not-exists').hide();
        });

        event.preventDefault();
    });
})