$(document).ready(function(){
    $(".navbar .nav-link").on('click', function(event) {

        if (this.hash !== "") {

            event.preventDefault();

            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 700, function(){
                window.location.hash = hash;
            });
        } 
    });
});
$('#nav-toggle').click(function(){
    $(this).toggleClass('is-active')
    $('ul.nav').toggleClass('show');
});
var getStartedBtn = document.getElementById('getStartedBtn');
var formDropdown = document.getElementById('formDropdown');
getStartedBtn.onclick = function () {
  formDropdown.style.display = (formDropdown.style.display === 'none' || formDropdown.style.display === '') ? 'block' : 'none';
};