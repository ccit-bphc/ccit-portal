function urg_fun() {
	var checkBox = document.getElementById("urgency_id");
	var a = document.getElementById("urg_reason");
	if (checkBox.checked == true) {
		if (a.style.display == 'none') {
			a.style.display = 'block';
			document.getElementById("boxclass").style.height = '38em';
		}
	} else {
		a.style.display = 'none';
		document.getElementById("boxclass").style.height = '34em';
		}
	}

$(document).ready(function () {
	$(".form_class").hide();
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
		console.log($(this).val());
	});
	
	$(".text_cls").change(function () {
		var x = $(this);
		console.log($(this));
		var regex = /^[A-Za-z0-9 ]+$/
        var isValid = regex.test(x.val());
		console.log(x.val());
	if ((isValid == false || x.val().length > 12) && x.val() != "") {
            x.css("border", "1px solid red");
			$(":submit").attr("disabled", true);
			document.getElementById('button').style.color = "#FFFFFF";
			document.getElementById('button').style.borderColor = "red";

        } else {
            x.css("border", "none");
			$(":submit").attr("disabled", true);
			$(":submit").attr("disabled", false);
        }
	});

});