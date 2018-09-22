$(document).ready(function(){
    $('.donation-interact').on('click', function(event){
        $(this.nextElementSibling).toggle();

        $(this)[0].classList.toggle('fa-chevron-down');
        $(this)[0].classList.toggle('fa-chevron-up');

        event.preventDefault();
    });
    $(document).on('submit', '#donate-what', function(event){
        let form = $(this)[0];
        console.log(form)

        let requestObj = {
            'clothes': form[0].checked,
            'furniture': form[1].checked,
            'books': form[2].checked,
            'electronics': form[3].checked,
            'other': form[4].checked,
            'donation_id': form[5].value,
        };


        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/what_form',
        }).done(function(data){
            console.log('done')
        });


        event.preventDefault();
    });

    $('#donate-what').on('submit', function(event){
        console.log('submit')
        let form = $(this)[0];
        console.log(form)

        let requestObj = {
            'clothes': form[0].checked,
            'furniture': form[1].checked,
            'books': form[2].checked,
            'electronics': form[3].checked,
            'other': form[4].checked,
            'donation_id': form[5].value,
        };


        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/what_form',
        }).done(function(data){
            console.log('done')
        });


        event.preventDefault();
    });

    $(document).on('submit', '#estimate-val', function(event){
        let form = $(this)[0];

        console.log(form)

        let requestObj = {
            'value': form[0].value,
            'donation_id': form[1].value
        };


        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/value_form',
        }).done(function(data){
            console.log('done')
        });


        event.preventDefault();
    });

    $('#estimate-val').on('submit', function(event){
        let form = $(this)[0];

        console.log(form)

        let requestObj = {
            'value': form[0].value,
            'donation_id': form[1].value
        };


        $.ajax({
            type : 'POST',
            data : requestObj,
            url : '/value_form',
        }).done(function(data){
            console.log('done')
        });


        event.preventDefault();
    });
});