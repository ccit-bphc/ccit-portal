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
	
function checkUR(abc){
    string = abc.value
    if(!(/^http:\/\//.test(string))){
        string = "http://" + string;
    }
    abc.value=string
}

	function timerecord1() {
		var t1 = document.getElementById('time').value;
		console.log('Time 1 = ' + t1);
		if(t1.length == 5){document.getElementById('hiddentime').value = t1 + ':00';}
		else{document.getElementById('hiddentime').value = t1;}		
		y = document.getElementById('hiddentime2').value;
		x = document.getElementById('hiddentime').value;
        var y = new Date("01/01/2007 " + y);
        var x = new Date("01/01/2007 " + x);
		var x = y - x;
		x = x / 60 / 60 / 1000;
		if(x < 1){document.getElementById('time_alert').style.display = "";document.getElementById('b1').setAttribute('disabled','');}
		else{document.getElementById('time_alert').style.display = "none";document.getElementById('b1').removeAttribute('disabled');}
	};
	function timerecord2() {
		var t2 = document.getElementById('time2').value;
		if(t2.length == 5){document.getElementById('hiddentime2').value = t2 + ':00';}
		else{document.getElementById('hiddentime2').value = t2;}
		y = document.getElementById('hiddentime2').value;
		x = document.getElementById('hiddentime').value;
        var y = new Date("01/01/2007 " + y);
        var x = new Date("01/01/2007 " + x);
		var x = y - x;
		x = x / 60 / 60 / 1000;
		if(x < 1){document.getElementById('time_alert').style.display = "";document.getElementById('b1').setAttribute('disabled','');}
		else{document.getElementById('time_alert').style.display = "none";document.getElementById('b1').removeAttribute('disabled');}
	};

function comp_fun(id){
	console.log('Im here!');
	console.log(id);
	console.log(document.getElementById(id + 'a'));
	if(document.getElementById(id + 'a').style.display == "none"){
		document.getElementById(id + 'a').style.display = "";
		document.getElementById(id + 'b').style.display = "";
		document.getElementById(id + 'd').style.display = "";
		document.getElementById(id + 'e').style.display = "";
		document.getElementById(id + 'c').setAttribute("class", "fas fa-caret-up");

	}
	else{
		document.getElementById(id + 'a').style.display = "none";
		document.getElementById(id + 'b').style.display = "none";
		document.getElementById(id + 'd').style.display = "none";
		document.getElementById(id + 'e').style.display = "none";
		document.getElementById(id + 'c').setAttribute("class", "fas fa-caret-down");
	}
	
}

function req_fun(id){
	console.log('Im here!');
	console.log(id);
	console.log(document.getElementById(id + 'ra'));
	if(document.getElementById(id + 'ra').style.display == "none"){
		document.getElementById(id + 'ra').style.display = "";
		document.getElementById(id + 'rb').style.display = "";
		document.getElementById(id + 'rc').setAttribute("class", "fas fa-caret-up");

	}
	else{
		document.getElementById(id + 'ra').style.display = "none";
		document.getElementById(id + 'rb').style.display = "none";
		document.getElementById(id + 'rc').setAttribute("class", "fas fa-caret-down");
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

	
	$('#room_no').change(function (){
		var room_no = document.getElementById('room_no');
		var regex = /[ !@#$%^&*()_+\-=\[\]{};':"\\|<>\/?]/ ;
		if(regex.test(room_no.value)){
			room_no.style.borderColor = 'red';
			document.getElementById('b1').setAttribute('disabled','');
		}
		else{room_no.style="";document.getElementById('b1').removeAttribute('disabled');}
	});
	
	$('#contact_no').change(function (){
		var contact_no = document.getElementById('contact_no');
		var regex = /^\d+$/ ;
		if((!regex.test(contact_no.value)) || (contact_no.value.length > 12 || contact_no.value.length < 8)){
			contact_no.style.borderColor = 'red';
			document.getElementById('b1').setAttribute('disabled','');
		}
		else{contact_no.style="";document.getElementById('b1').removeAttribute('disabled');}
	});
});

