function urg_fun() {
	var checkBox = document.getElementById("default");
	var a = document.getElementById("urg_reason");
	var b = document.getElementById("urgency_reason");
	if (checkBox.checked == true) {
		if (a.style.display == 'none') {
			a.style.display = 'block';
			b.setAttribute('required','');
		}
	} else {
		a.style.display = 'none';
		b.removeAttribute('required');
		}
	}
	
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");
// Get the <span> element that closes the modal
// When the user clicks the button, open the modal 
function closepopup() {
  document.getElementById("myModal").style = "";
}
// When the user clicks on <span> (x), close the modal

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    document.getElementById("myModal").style = "";
}
	
function timeslot_fun(){
		var checkBox1 = document.getElementById("slot_1");
		var checkBox2 = document.getElementById("slot_2");
		if(checkBox1.checked == true){
		document.getElementById('hiddentime').value = '12:00:00';
		document.getElementById('hiddentime2').value = '13:30:00';
		}
		
		if(checkBox2.checked == true){
		document.getElementById('hiddentime').value = '16:30:00';
		document.getElementById('hiddentime2').value = '17:00:00';
		}
	}
	
function checkURL(abc){
    string = abc.value
    if(!(/^:\/\//.test(string))){
        string = "http://" + string;
    }
    abc.value=string
}

	function timerecord1() {
		var t1 = document.getElementById('time').value;
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
		var today = new Date();
		p = (today.getMonth()+1) + '/' + today.getDate() + '/' + today.getFullYear();
		p2 = document.getElementById('date').value.split('-');
		p2 = p2[1] + '/' + p2[2] + '/' + p2[0];
		var timenow = new Date(p + " " + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds());
		var start_time = new Date(p2 + " " + document.getElementById('hiddentime').value);
		var start_time_a = new Date("01/01/2007 " + document.getElementById('hiddentime').value);
		var staff_start = new Date("01/01/2007 " + "09:00:00");
		if(start_time <= timenow || start_time_a < staff_start){document.getElementById('time_alert_x').style.display = "";document.getElementById('b1').setAttribute('disabled','');}
		else{document.getElementById('time_alert_x').style.display = "none";document.getElementById('b1').removeAttribute('disabled');}
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
		var today = new Date();
		p = (today.getMonth()+1) + '/' + today.getDate() + '/' + today.getFullYear();
		p2 = document.getElementById('date').value.split('-');
		p2 = p2[1] + '/' + p2[2] + '/' + p2[0];
		var timenow = new Date(p + " " + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds());
		var end_time = new Date(p2 + " " + document.getElementById('hiddentime2').value);
		var end_time_a = new Date("01/01/2007 " + document.getElementById('hiddentime').value);
		var staff_end = new Date("01/01/2007 " + "17:00:00");
	if(end_time <= timenow || end_time_a > staff_end){document.getElementById('time_alert_x').style.display = "";document.getElementById('b1').setAttribute('disabled','');}
		else{document.getElementById('time_alert_x').style.display = "none";document.getElementById('b1').removeAttribute('disabled');}
	};

function comp_fun(id){
	if(document.getElementById(id + 'a').style.display == "none"){
		document.getElementById(id + 'a').style.display = "";
		document.getElementById(id + 'b').style.display = "";
		document.getElementById(id + 'd').style.display = "";
		document.getElementById(id + 'e').style.display = "";
		document.getElementById(id + 'f').style.display = "";
		document.getElementById(id + 'c').setAttribute("class", "fas fa-caret-up");

	}
	else{
		document.getElementById(id + 'a').style.display = "none";
		document.getElementById(id + 'b').style.display = "none";
		document.getElementById(id + 'd').style.display = "none";
		document.getElementById(id + 'e').style.display = "none";
		document.getElementById(id + 'f').style.display = "none";
		document.getElementById(id + 'c').setAttribute("class", "fas fa-caret-down");
	}
	
}

function req_fun(id){
	if(document.getElementById(id + 'ra').style.display == "none"){
		document.getElementById(id + 'ra').style.display = "";
		document.getElementById(id + 'rb').style.display = "";
		document.getElementById(id + 'rd').style.display = "";
		document.getElementById(id + 'rc').setAttribute("class", "fas fa-caret-up");
	}
	else{
		document.getElementById(id + 'ra').style.display = "none";
		document.getElementById(id + 'rb').style.display = "none";
		document.getElementById(id + 'rd').style.display = "none";
		document.getElementById(id + 'rc').setAttribute("class", "fas fa-caret-down");
	}
	
}

$(document).ready(function () {
	$('#bhavan_list li').on('click', function(){
		$("#dd_button").text($(this).text());
		let arr = ["K", "R", "S", "G", "B", "V", "GT", "VM", "M", "MM", "VB", "VG", "MR", "H8"];
		let num = parseInt($(this).attr('id'));
		document.getElementById('bhavan').value = arr[num];
		if(arr[num] == "MM" || arr[num] == "M" || arr[num] == "VG"){
			document.getElementById('g_msg').style="";
			document.getElementById('slots').style="";
			document.getElementById('time').style.display="none";
			document.getElementById('time3').style.display="none";
			document.getElementById('time2').style.display="none";
			}
		else{
			document.getElementById('g_msg').style.display = "none";
			document.getElementById('slots').style.display="none";
			document.getElementById('time').style="";
			document.getElementById('time3').style.display="inline";
			document.getElementById('time2').style="";
			}
	});
	
	$("#option").change(function () {
		//document.getElementById('url_unblock').style.display = 'none';
		document.getElementById('other3').style.display = 'none';
		if($(this).val() == 'none'){
		//document.getElementById('url_unblock').style.display = 'none';
		document.getElementById('other3').style.display = 'none';
		}
		if ($(this).val() == 'WF' || $(this).val() == 'LN' || $(this).val() == 'SF') {
			document.getElementById('other3').style.display = 'block';
		} if($(this).val() == 'url_unblock') {
			//document.getElementById('url_unblock').style.display = 'block';
		}
		$(this).css("width","200px");
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
	
	$('#url').change(function (){
		    string = document.getElementById("url").value;
			if(!(new RegExp('://').test(string))){
				string = "http://" + string;
			}
			document.getElementById("url").value = string;
	});
	
	$('#contact_no').change(function (){
		var contact_no = document.getElementById('contact_no');
		var regex = /^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$/ ;
		if((!regex.test(contact_no.value)) || (contact_no.value.length > 12 || contact_no.value.length < 10)){
			contact_no.style.borderColor = 'red';
			document.getElementById('b1').setAttribute('disabled','');
		}
		else{contact_no.style="";document.getElementById('b1').removeAttribute('disabled');}
	});
});

