$( document ).ready(function() {
    var form = document.getElementById('valForm');
    // Loop over them and prevent submission
      form.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();
        if (validateData() == false) {
        }
        else {
            submitForm();
        }
        form.classList.add('was-validated');

      }, false);
});

function validateData() {
    var u = $("#username").val();
    var p = $("#password").val();
    if(u.length <= 5) {
        return false;
    }
    if(p.length <= 4) {
        return false;
    }
    return true;
}


// submit the form data
function submitForm(){
    $("#login-form form").hide();
    $(".loader").show();
    var form = $('form');
    var url = '/login/';
    var formData = $(form).serializeArray();
    $.post(url, formData).done(function (data) {
        if(data == 'error') {
            $("#wrong").show();
            setTimeout(function(){ $("#wrong").hide(); }, 3000);
            $("#login-form form").show();
            $(".loader").hide();
        }
        else {
            window.location.href = data;
        }

    });
    return false;
}