$(window).resize(function() {
  setTimeout( function(){var count=1;
    $(".scrollingHead").find('tr>th').each(function( event ) {        
      var thWdith=$(this).outerWidth();
      $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
      count++;
    });
  },10);
});

$(function () {
  //$('table').footable();
  
  var count=1;
  $(".scrollingHead").find('tr>th').each(function( event ) {        
    var thWdith=$(this).outerWidth();
    $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
    count++;
  });
});

$(document).ready(function() {
	$('input[type=checkbox]').click(function() {  
		if(this.checked == true) { 
			//$(this).parent().addClass('activetab');
		} else {
			//$(this).parent().removeClass('activetab');
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
          resultclass = "result_available";
		      linkclass = "";
  		    status = "disabled";
        }
        if(item.Result == "FAILURE"){
          resultclass = "result_offline";
		      linkclass = "";
          status = 'disabled';
		    }
        if(item.Result == "IN PROGRESS"){
          resultclass = "result_progress";
		      linkclass = "";
          status = '';
		    }
        if(item.Result == "IN QUEUE"){
          resultclass = "result_queue";
		      linkclass = "";
		      status = '';
        }
        if(item.Result == "ABORTED"){
          resultclass = "result_aborted";
		      linkclass = "";
		      status = 'disabled';
        }
            /*$("#testdataid").append("<tr><td style='cursor:pointer;padding:10px 15px;'><input type='checkbox' name='check2' "+status+" value ='"+ item["Job No"] +","+item["Build No"]+"' style='margin-top:3px;' ></td><td width='70px' style='vertical-align:middle'><label>"+item["Job No"]+" </label></td><td class='suite-name' width='120px' style='vertical-align:middle; padding:0px 0px 0px 0px'>"+item["Suite Name"]+"</td><td width='70px' style='vertical-align:middle'>"+item["Build No"]+"</td><td width='105px' class = " + resultclass + " style='vertical-align:middle'>" + item.Result + "</td><td width='220px' style='vertical-align:middle;word-break:break-all'>" + item.StartTime + "</td><td width='220px' style='vertical-align:middle;word-break:break-all'>" + item.EndTime + "</td><td width='95px' style='vertical-align:middle'>" + item.Duration +" </td><td width='95px' style='vertical-align:middle'>" + item.UserName +" </td><td width='84px' style='vertical-align:middle' data-editable=\"true\"><button onclick=\"stb1('"+item["Job No"]+"',"+item["Build No"]+")\" data-role=\"button\" class=\"btn_stop btn btn-danger\">Stop</button></td><td width='125px' data-editable=\"true\" style='vertical-align:middle'><a href=\"#\" onclick=\"showConsole(this)\" class="+ linkclass +">Console Output</a></td></tr>");*/
			$("#testdataid").append("<tr><td style='padding-left:36px; width:66px; text-align:center'><input type='checkbox' name='check2' "+status+" value ='"+ item["Job No"] +","+item["Build No"]+"'></td><td style='width:37px; text-align: center'><label>"+item["Job No"]+" </label></td><td class='suite-name' style='width:88px; text-align: center'>"+item["Suite Name"]+"</td><td style='width:52px; text-align: center'>"+item["Build No"]+"</td><td class = " + resultclass + " style='width:72px; text-align: center'>" + item.Result + "</td><td style='width:135px; text-align: center'>" + item.StartTime + "</td><td style='width:135px; text-align: center'>" + item.EndTime + "</td><td style='width:77px; text-align: center'>" + item.Duration +" </td><td style='width:59px; text-align: center'>" + item.UserName +" </td><td style='width:202px; text-align: center'><button onclick=\"stb1('"+item["Job No"]+"',"+item["Build No"]+")\" data-role=\"button\" class=\"btn_stop btn btn-danger\">Stop</button></td><td style='width:237px; text-align: center'><a href=\"#\" onclick=\"showConsole(this)\" class="+ linkclass +">Console Output</a></td></tr>");
        });
    }) 
}

function showConsole(that) {
  var vals = $(that).closest("tr").find("input").val().split(",");
  var suite_name = $(that).closest("tr").find("td[class='suite-name']").text();
  var title = "JOB: " + vals[0] +",    SUITE NAME:  " + suite_name;

  $.ajax({
    url: "http://127.0.0.1:8000/revo/console/",
    type: "get",
    data:{"job": vals[0], "build" : vals[1]},
    cache: false,
    success: function(data){
      $('#revo-modal-content').text(data);
      $('#title').text(title);
      $('#myModal').modal();
    }
  });
}
/****Select All Checkbox****/
function checkAll(ele) {
     var checkboxes = document.getElementsByName('check2');
     if (ele.checked) {
         for (var i = 0; i < checkboxes.length; i++) {
             if (checkboxes[i].type == 'checkbox' && checkboxes[i].disabled == '') {
                 checkboxes[i].checked = true;
             }
         }
     } else {
         for (var i = 0; i < checkboxes.length; i++) {
             console.log(i)
             if (checkboxes[i].type == 'checkbox') {
                 checkboxes[i].checked = false;
             }
         }
     }
 }
 
 
 function showMe (box) {
        
	var chboxs = document.getElementsByName("schedule");
	var visible_value = "none";
	for(var i=0;i<chboxs.length;i++) { 
		if(chboxs[i].checked){
		 visible_value = "block";
			break;
		}
	}
	
	document.getElementById(box).style.display = visible_value;
	
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	
	if(dd<10) {
		dd='0'+dd
	} 

	if(mm<10) {
		mm='0'+mm
	} 

	today = yyyy+'/'+mm+'/'+dd;
	document.getElementById("schedule_date").value = today;
	
}

function disable_edit() {
  var obj;
  var count=0;
  var Change = document.getElementsByName('Edit_Button')[0];
      for (var i=0; i<tform.elements.length; i++) {
        obj = tform.elements[i];
        if (obj.type == "checkbox" && obj.checked) {
          count++;
        }
      }
  if(count==1){
      Change.disabled=false;
  }
  if(count>1){
      Change.disabled=true;
  }
}

function disable_edit_test(elementName, checkboxPath) {
  var changeBtn = document.getElementsByName(elementName)[0];

  if($( checkboxPath + " :checkbox:checked").length == 1) {
    changeBtn.disabled=false;
  } else {
    changeBtn.disabled=true;
  }
}

function editTestCase() {
  window.location.href = $( ".list_table tr td :checkbox:checked").attr("data-edit");
  return false;
}

$(function () {
    $("input[type='checkbox']").change(function () {
        $(this).siblings('ul')
            .find("input[type='checkbox']")
            .prop('checked', this.checked);
    });
});
