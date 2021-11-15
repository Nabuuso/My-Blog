$(document).ready(function () {
    //REGISTER USER
    $("#registerBtn").click(function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                full_name: $('#fullName').val(),
                email: $('#email').val(),
                password: $('#password').val()
            },
            type: 'POST',
            url: 'users'
        }).done(function (data) {
            alert("Registration completed successfully!")
            $('#fullName').val('')
            $('#email').val(''),
                $('#password').val('')
            location.reload()
        });
    });
    //GET QUOTES
    function getQuotes(){
        $.get("http://quotes.stormconsultancy.co.uk/random.json",function(){

        })
    }
});