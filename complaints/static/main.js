function urg_fun() {
	var checkBox = document.getElementById("default");
	var a = document.getElementById("urg_reason");
	if (checkBox.checked == true) {
		if (a.style.display == 'none') {
			a.style.display = 'block';
		}
	} else {
		a.style.display = 'none';
		}
	}

$(document).ready(function () {
	$("#option").change(function () {
		document.getElementById('url_unblock').style.display = 'none';
		document.getElementById('other3').style.display = 'none';
		console.log($(this).val());
		if($(this).val() == 'none'){
		document.getElementById('url_unblock').style.display = 'none';
		document.getElementById('other3').style.display = 'none';
		}
		if ($(this).val() == 'wifi' || $(this).val() == 'lan' || $(this).val() == 'firewall') {
			document.getElementById('other3').style.display = 'block';
		} if($(this).val() == 'url_unblock') {
			document.getElementById('url_unblock').style.display = 'block';
		}
		$(this).css("width","200px");
		console.log("Im here 1");
		console.log($(this).val());
	});
	
	$(".form-control").change(function () {
		var x = $(this);
		if(x.attr("a") != "true"){
		console.log(($(this)).toString());
		var regex = /(?:[^\*\^\#\%\@\!\(\)\=\{\}\[\]\:\'\"]*)/
        var isValid = regex.test(x.val());
		console.log(x.val());
		console.log(isValid);
		if(document.getElementById('option').value == "url_unblock"){var b1 = 'b2';}
		else{var b1 = 'b1';}
	if ((isValid == false || x.val().length > 12) && x.val() != "") {
			console.log("current form: ");
			console.log(document.getElementById('option').value);
            x.css("border", "1px solid red");
			$("#" + b1).attr("disabled", true);
			document.getElementById(b1).style.background = "#888888";
			document.getElementById(b1).style.borderColor = "#777777";

        } else {
            x.attr("style","");
			$("#" + b1).attr("disabled", true);
			$("#" + b1).attr("disabled", false);
			$("#" + b1).css("border-color","black");
			$("#" + b1).css("background","#444444");
        }
		}
	});

});