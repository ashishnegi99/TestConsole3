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

  $('.dropdown-menu').on('click', function(e) {
    if($(this).hasClass('dropdown-menu-form')) {
      e.stopPropagation();
    }
  });
});

$(window ).resize(function() {
  setTimeout( function(){var count=1;
    $(".scrollingHead").find('tr>th').each(function( event ) {        
      var thWdith=$(this).outerWidth();
      //console.log(count+'dddddd');
      $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
      count++;
    });
  },10);
});

$(function() {
  $('table').footable();
  
  stbststus();
  stbststus1();
  
  var count=1;
  $(".scrollingHead").find('tr>th').each(function( event ) {        
    var thWdith=$(this).outerWidth();
    //console.log(count+'dddddd');
    $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
    count++;
  });
});

function show_alert() {
  alert("Run Successful!");
}

$(function() {
});

function checkStatus($event){
  //console.log($event.toSource());
    if ($event.value && $event.checked == true){
      //console.log($event.value);
      console.log($event.checked);
      //alert($event.checked);
      $event.setAttribute("checked", "checked");
    }
    else{$event.removeAttribute("checked", "checked");
    }
}
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

function stb2(job, build) {
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
    $.getJSON("JobStatus", function(result) {
      $("#testdataid").empty();
        $.each(result, function(i, item){
		var status;
        if(item.Result == "SUCCESS"){
          colorclass = "available";
		  linkclass = "";
  		    status = "";
        }
        if(item.Result == "FAILURE"){
          colorclass = "offline";
		  linkclass = "linkclass";
          status = 'disabled';
		}
        if(item.Result == "IN PROGRESS"){
         colorclass = "progress";
		 linkclass = "linkclass";
          status = '';
		}
        if(item.Result == "IN QUEUE"){
          colorclass = "queue";
		  linkclass = "linkclass";
		      status = '';
        }
        if(item.Result == "ABORTED"){
          colorclass = "aborted";
		  linkclass = "linkclass";
		      status = 'disabled';
        }
            $("#testdataid").append("<tr><td width='130px' style='vertical-align:middle'><label class='checkbox'><input type='checkbox' name='check2' "+status+" value ='"+ item["Job No"] +","+item["Build No"]+"' style='margin-top:3px;' >"+item["Job No"]+" </label></td><td width='110px' style='vertical-align:middle'>"+item["Suite Name"]+"</td><td width='80px' style='vertical-align:middle'>"+item["Build No"]+"</td><td width='105px'><p class = " + colorclass + " style='vertical-align:middle'>" + item.Result + "</p></td><td width='160px' style='vertical-align:middle;word-break:break-all'>" + item.StartTime + "</td><td width='160px' style='vertical-align:middle;word-break:break-all'>" + item.EndTime + "</td><td width='95px' style='vertical-align:middle'>" + item.Duration +" </td><td width='84px' style='vertical-align:middle' data-editable=\"true\"><button onclick=\"stb1('"+item["Job No"]+"',"+item["Build No"]+")\" data-role=\"button\" class=\"btn_stop btn btn-danger\">Stop</button></td><td width='125px' data-editable=\"true\" style='vertical-align:middle'><a href=\"#\" onclick=\"showConsole(this)\" class="+ linkclass +">Console Output</a></td></tr>");
        });
    }); 
}

function showConsole(that) {
  var vals = $(that).closest("tr").find("input").val().split(",");

  $.ajax({
    url: "http://127.0.0.1:8000/revo/console/",
    type: "get",
    data:{"job": vals[0], "build" : vals[1]},
    cache: false,
    success: function(data){
      $('#revo-modal-content').text(data);
      $('#myModal').modal();
    }
  });
}