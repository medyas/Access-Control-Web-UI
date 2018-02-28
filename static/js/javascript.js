
/*
    navbar and main menu
*/

function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
}

/* Close/hide the sidenav */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

  $( function() {
	var options = {
		url: function(phrase) {
			return "/findemployee/"+phrase;
		},
		getValue: function(element) {
			return element.firstname + ", "+element.lastname;
		},
		template: {
			type: "custom",
			method: function(value, item) {
				var img = item.img_path.replace("var/www/flask/accessControl/", "");
				return '<div class="auto-item"><img src="'+img+'"><div><p>'+value+'</p><span>N. '+item.id+'</span></div></div>'
			}
		},
		list: {
			match: {
				enabled: true
			}
		}
	}
    $( "#search" ).easyAutocomplete(options);
  } );

$(document).on('click', '#eac-container-search ul li', function() {
	$('#logs table').html("<tr><th>User Id</th><th>Scan Id</th><th>Scan Date</th><th>Scan Time</th></tr>");
	$('#empModal').modal('toggle');
	$("#empInfo").hide();
	$("#logs").hide();
	$(".loader").show();
	$.getJSON( '/employee='+$(this).find('span').text().split(" ")[1], function( data ) {
		$('#empInfo #img img').attr('src', data.employee[0].img_path.replace("var/www/flask/accessControl/", ""));
		$('#empInfo #info #name').text(data.employee[0].firstname+", "+data.employee[0].lastname);
		$('#empInfo #info #address').text(data.employee[0].address);
		$('#empInfo #info #card_uid').text(data.employee[0].card_uid);
		$.each( data.logs, function( key, value ) {
		  $('#logs table').append("<tr><td>"+value.user_id+"</td><td>"+value.id+"</td><td>"+value.date+"</td><td>"+value.time+"</td></tr>");
		});
		$("#empInfo").show();
		$("#logs").show();
		$(".loader").hide();
		
  	});
});

/* --------------------------------------------------------------------- */
function findMatch(string, index) {
	if(string == "")
		$(".logsTr").show();
	var re = new RegExp(string);
	var temp;
	$.each( $(".logsTr"), function( key, value ) {
		temp = $.parseHTML( value.innerHTML );
		if((temp[index].innerHTML.toLowerCase().match(re)) == null)
			$(this).hide();
		else
			$(this).show();
	});
}

function submitForm(){
    $("#dForm form").hide();
    $(".loader").show();
    var form = $('form');
    var url = window.location.pathname;
    var formData = $(form).serializeArray();
    $.post(url, formData).done(function (data) {
	    $(data.class).text(data.msg);
	    $(data.class).show();
	    setTimeout(function(){ $(".alert").hide(); $(".alert").text('');}, 3000);
	    $("#dForm form").find("input[type=text], input[type=email], input[type=password], input[type=text]").val("");
	    $("#dForm form").show();
            $(".loader").hide();


    });
    return false;
}

function valAddUser() {
	return false;
}
/* --------------------------------------------------------------------- */

$( document ).ready(function() {

/*
    dashboard
*/
	var path = window.location.pathname;
if( path== "/dashboard/") {
	document.getElementById("dashDate").max = new Date().toJSON().slice(0,10);
	$( "input[type='date']" ).change(function() {
		findMatch($(this).val(), 4);
	});
	$( "input[type='text']" ).keyup(function() {
		findMatch($(this).val(), 1);
	});
	$( "input[type='number']" ).keyup(function() {
		findMatch($(this).val(), 2);
	});
	
	$(".loader").show();
	$.ajax({
	  type: "POST",
	  url: "/dashboard/",
	  success: function(data) {
		$(".loader").hide();
		$.each( data, function( key, value ) {
		  $('#dashLogs table').append("<tr class='logsTr'><td>"+value.user_id+"</td><td class='trName'>"+value.name+"</td><td class='trCard'>"+value.card_uid+"</td><td>"+value.scan_id+"</td><td class='trDate'>"+value.date+"</td><td>"+value.time+"</td></tr>");
		});
	},
	  dataType: 'json'
	});

}
/* --------------------------------------------------------------------- */
/*
    add User
*/
else if(path == '/adduser/') {
	var form = document.getElementById('valForm');
      form.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();
        if (valAddUser() == false) {
        }
        else {
            submitForm();
        }
        form.classList.add('was-validated');

      }, false);
}

/* --------------------------------------------------------------------- */
/*
    add employee
*/
else if(path == '/addemployee/') {

}

/* --------------------------------------------------------------------- */
/*
    block employee
*/
else if(path == '/block/') {

}

/* --------------------------------------------------------------------- */
/*
    delete User
*/
else if(path == '/deleteuser/') {

}

/* --------------------------------------------------------------------- */
/*
    delete employee
*/
else if(path == '/deleteemployee/') {

}

/* --------------------------------------------------------------------- */
/*
    contact
*/
else if(path == '/contact/') {

}

/* --------------------------------------------------------------------- */
/*
    settings
*/
else if(path == '/settings/') {

}


});


/* --------------------------------------------------------------------- */

