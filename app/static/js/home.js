$(document).ready(function(){
    $('.donation-interact').on('click', function(event){
        $(this.nextElementSibling).toggle();

        $(this)[0].classList.toggle('fa-chevron-down');
        $(this)[0].classList.toggle('fa-chevron-up');

        event.preventDefault();
    });
});