$(document).ready(function() {
	$('input[type=checkbox]').click(function() {  
		if(this.checked == true) { 
			$(this).parent().addClass('activetab');
		} else {
			$(this).parent().removeClass('activetab');
		}
	}); 

	$(':radio').change(function () {
        $(':radio[name=' + this.name + ']').parent().removeClass('activetab');
        $(this).parent().addClass('activetab');
    }); 
});

$(function() {
    stbststus();
    stbststus1();
});

function stbststus() {
  $.getJSON("Json", function(result) {
      $("#STBStatus").empty();
        $.each(result, function(i, item) {
		var status;
          if(item.STBStatus == "1"){
            colorclass = "available";
            status = "";
          }
          if(item.STBStatus == "0"){
            colorclass = "offline";
            status = "disabled";
          }
          if(item.STBStatus == "2"){
            colorclass = "In use";
            status = "";
          }
            $("#STBStatus").append("<label class='checkbox'><input type='checkbox' name='check1' "+status+" value='"+item.STBLabel+"'>" +item.STBLabel +"   <i class='fa fa-circle pull-right  "+colorclass+"' aria-hidden='true'></i></label> <hr>");
        });
    });
}

function stb2(job, build){
  $.post("stopJob", {"Job Number":job, "Build Number":build}, function(result){
    location.reload();

  });
}

function stb1(job1, build1){
    alert (job1);
    alert (build1);
    $.get("stopJob",{ job: job1, build: build1 },function(result){
     });
}

function stbststus1(){
    $.getJSON("JobStatus", function(result){
      $("#testdataid").empty();
        $.each(result, function(i, item){
		var status;
        if(item.Result == "SUCCESS"){
        colorclass = "available";
		status = 'disabled';
        }
        if(item.Result == "FAILURE"){
        colorclass = "offline";
        status = 'disabled';
		}
        if(item.Result == "IN PROGRESS"){
        colorclass = "progress";
        status = '';
		}
        if(item.Result == "IN QUEUE"){
        colorclass = "queue";
		status = '';
        }
        if(item.Result == "ABORTED"){
        colorclass = "aborted";
		status = 'disabled';
        }
            $("#testdataid").append("<tr><td><label class='checkbox'><input type='checkbox' name='check2' "+status+" value ='"+ item["Job No"] +","+item["Build No"]+"' >"+item["Job No"]+" </label></td><td>"+item["Suite Name"]+"</td><td>"+item["Build No"]+"</td><td><p class = " + colorclass + ">" + item.Result + "</p></td><td>" + item.StartTime + "</td><td>" + item.EndTime + "</td><td>" + item.Duration +" </td><td data-editable=\"true\"><button onclick=\"stb1('"+item["Job No"]+"',"+item["Build No"]+")\" data-role=\"button\" class=\"btn_stop btn btn-danger\">Stop</button></td><td data-editable=\"true\"><a href=\"ReportsLink\">REPORT LINK</a></td></tr>");
        });
    }); 
}

function show_alert() {
  alert("Run Successful!");
}