
/*
    navbar and main menu
*/

function openNav() {
	$("#fFile").hide();
    document.getElementById("mySidenav").style.width = "100%";
}

/* Close/hide the sidenav */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
	$("#fFile").show();
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

$(document).on('click', '#eac-container-search ul li .auto-item', function() {
	$('#logs table').html("<tr><th>User Id</th><th>Scan Id</th><th>Scan Date</th><th>Scan Time</th></tr>");
	$(".easy-autocomplete #search").text('');
	$('#empModal').modal('toggle');
	$("#empInfo").hide();
	$("#logs").hide();
	$(".loader").show();
	$.getJSON( '/employee='+$(this).find('span').text().split(" ")[1], function( data ) {
		$('#empInfo #img img').attr('src', data.employee[0].img_path.replace("var/www/flask/accessControl/", ""));
		$('#empInfo #info #name').text(data.employee[0].firstname+", "+data.employee[0].lastname);
		$('#empInfo #info #address').text(data.employee[0].address);
		$('#empInfo #info #card_uid').text(data.employee[0].card_uid); 
		$('#empInfo #info #status').text(data.block);
		$('#empInfo #info #status').removeClass("alert-success");
		$('#empInfo #info #status').removeClass("alert-danger");
		$('#empInfo #info #status').addClass("alert-success");
		if(data.block != 'Working') {
			$('#empInfo #info #status').addClass("alert-danger");
		}
		$.each( data.logs, function( key, value ) {
		  $('#logs table').append("<tr><td>"+value.user_id+"</td><td>"+value.id+"</td><td>"+value.date+"</td><td>"+value.time+"</td></tr>");
		});
		$("#empInfo").show();
		$("#logs").show();
		$(".loader").hide();
		
  	});


});

/* --------------------------------------------------------------------- */
// find matching tr in dashboard table 
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

// submit the form through post to the url
function submitForm(path){
    $(".dForm form").hide();
    $(".loader").show();
    var form = $('.dForm form');
    var url = window.location.pathname;
    var formData = $(form).serializeArray();

if(url == '/adduser/') {
	formData[6] = {'name': 'edit', 'value': $("#edit").is(":checked")};
	formData[7] = {'name': 'add', 'value': $("#add").is(":checked")};
	formData[8] = {'name': 'block', 'value': $("#block").is(":checked")};
	formData[9] = {'name': 'delete', 'value': $("#delete").is(":checked")};
}
else if(url == '/addemployee/') {
	formData[4] = {'name':'img_path', 'value':path};
}
else if(url == '/block/') {
	formData[5] = {'name':'card_uid', 'value':$("#valForm #card_uid").val()};
}
	$.ajax({
		  type: "POST",
		  url: url,
		  data: formData,
		  success: function(data) {
		    $("."+data.class).text(data.msg);
		    $("."+data.class).show();
		    setTimeout(function(){ $(".alert").hide(); $(".alert").text('');}, 3000);
		    if(data.status) {
		    	$(".dForm form").find("input[type=text], input[type=email], input[type=password], input[type=number], input[type=file], input[type=date], input[type=time]").val("");
		    	$(".dForm form").find("input[type=checkbox]").prop('checked',false);
			if(url == '/addemployee/') {
			$("#progBar").css("width", (0).toString()+"%");
			}
			}
		    $(".dForm form").show();
	            $(".loader").hide();
		},
		  dataType: 'json'
	});
    return false;
}

// validate add user form
function valAddUser() {
	if($("#password").val() != $("#passConfirm").val() ) {
		return false;
	}
	var formData = $(".dForm form").serializeArray();
	for(var i=0; i< formData.length; i++) {
		if(formData[i].value == "") {
			return false;
		}

	}
	return true;
}

// validate add employee form
function valAddEmp() {
	if($("#img_path").val() == '')
		return false;
	var formData = $(".dForm form").serializeArray();
	for(var i=0; i< formData.length; i++) {
		if(formData[i].value == "") {
			return false;
		}

	}
	return true;
}

// validate the block form
function valBlock() {
	if($("#ftime").val() == '' || $("#ttime").val() == '' || $("#fdate").val() == '' || $("#tdate").val() == '' || $("#valForm #card_uid").val() == '')
		return false;
	if($("#fdate").val() > $("#tdate").val()) {
		return false;
	}
	else if($("#fdate").val() == $("#tdate").val()) {
		if($("#ftime").val() >= $("#ttime").val())
			return false;
	}
	return true;
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
	
	$("#reset").click(function(e) {
		e.preventDefault();
        	e.stopPropagation();
		$(".logsTr").show();
		$( "input[type='number']" ).val("");
		$( "input[type='date']" ).val("");
		$( "input[type='text']" ).val("");
		return false;
	});
	
	$("#filter").on('click', function(e) {
		e.preventDefault();
        	e.stopPropagation();
		$(".logsTr").show();
		var n = new RegExp($( ".filter input[type='text']" ).val());
		var u = new RegExp($( ".filter input[type='number']" ).val());
		var d = new RegExp($( ".filter input[type='date']" ).val());
		var temp;
		$.each( $(".logsTr"), function( key, value ) {
			temp = $.parseHTML( value.innerHTML );
			if((temp[1].innerHTML.toLowerCase().match(n)) == null || (temp[2].innerHTML.toLowerCase().match(u)) == null || (temp[4].innerHTML.toLowerCase().match(d)) == null)
				$(this).hide();
			else
				$(this).show();
		});
		return false;
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
	$("#img_path").change(function() {
		$("#img_label").html(' <i class="fas fa-cloud-upload-alt"></i> ' +$(this).val());
	});
	var form = document.getElementById('valForm');
	var submit = document.getElementById('submit');
        submit.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        if (valAddEmp() == false) {
        }
        else {
		var data =  new FormData($("#fFile")[0]);
		$('#valForm p').show();
		$('.progress').show();
		$.ajax({
			xhr: function()
			  {
			    var xhr = new window.XMLHttpRequest();
			    //Upload progress
			    xhr.upload.addEventListener("progress", function(evt){
			      if (evt.lengthComputable) {
			        var percentComplete = evt.loaded / evt.total;
			        //Do something with upload progress
				$('#valForm p').text("Uploading image "+(percentComplete*100).toString()+"% ...");
			        $("#progBar").css("width", (parseInt(percentComplete*100)).toString()+"%");
			      }
			    }, false);
			    //Download progress
			    xhr.addEventListener("progress", function(evt){
			      if (evt.lengthComputable) {
			        var percentComplete = evt.loaded / evt.total;
			        //Do something with download progress
			        console.log(percentComplete);
			      }
			    }, false);
			    return xhr;
  			},
		  enctype: 'multipart/form-data',
		  processData: false,
            	  contentType: false,
            	  cache: false,
            	  timeout: 600000,
		  type: "POST",
		  url: "/upload/",
		  dataType: 'json',
		  data: data,
		  success: function(data) {
			submitForm(data.img_path);
			$('#valForm p').hide();
			$('.progress').hide();
			$("#progBar").css("width", (0).toString()+"%");
			},
 		  error: function (e) {
		    $(".alert-danger").text("Something happened, Couldn't add the data.");
		    $(".alert-danger").show();
		    setTimeout(function(){ $(".alert").hide(); $(".alert").text('');}, 3000);
	                console.log("ERROR : ", e);
			$('#valForm p').hide();
			$("#progBar").css("width", (0).toString()+"%");
			$('.progress').hide();
	
	            }
		});
            
        }
        form.classList.add('was-validated');

      }, false);
}

/* --------------------------------------------------------------------- */
/*
    block employee
*/
else if(path == '/block/') {
	document.getElementById("fdate").min = new Date().toJSON().slice(0,10);
	$( "#fdate" ).change(function() {
		document.getElementById("tdate").min = $(this).val();
	});
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
				return '<div class="block-item"><img src="'+img+'"><div><p>'+value+'</p><span>UID. '+item.card_uid+'</span></div></div>'
			}
		},
		list: {
			match: {
				enabled: true
			}
		}
	}
    $( "#fname" ).easyAutocomplete(options);

	// block user auto complete 
	$(document).on('click', '#eac-container-fname .block-item', function() {
		$("#valForm #card_uid").val($(this).find('span').text().split(" ")[1]);
	});

	var form = document.getElementById('valForm');
	var submit = document.getElementById('submit');
        submit.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        if (valBlock() == false) {
        }
        else {
		submitForm();
	}
        form.classList.add('was-validated');

      }, false);
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

