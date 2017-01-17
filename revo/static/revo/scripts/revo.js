// $(window).resize(function() {
//   setTimeout( function(){var count=1;
//     $(".scrollingHead").find('tr>th').each(function( event ) {        
//       var thWdith=$(this).outerWidth();
//       $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
//       count++;
//     });
//   },10);
// });

// $(function () {
  
//   var count=1;
//   $(".scrollingHead").find('tr>th').each(function( event ) {        
//     var thWdith=$(this).outerWidth();
//     $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
//     count++;
//   });
// });

// $(document).ready(function() {
//   var checkboxes_all = document.getElementsByName('check2');

//   for(var i=0; i<checkboxes_all.length; i++) {
//     checkboxes_all[i].addEventListener("click", singleCheck(),true)
//   }

// 	$(':radio').change(function () {
//       $(':radio[name=' + this.name + ']').parent().removeClass('activetab');
//       $(this).parent().addClass('activetab');
//   });

//   $('.dropdown-menu').on('click', function(e) {
//     if($(this).hasClass('dropdown-menu-form')) {
//       e.stopPropagation();
//     }
//   });
// });

// $(window ).resize(function() {
//   setTimeout( function(){var count=1;
//     $(".scrollingHead").find('tr>th').each(function( event ) {        
//       var thWdith=$(this).outerWidth();
    
//       $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
//       count++;
//     });
//   },10);
// });

$(function() {

  //Utility Functionality added to Array
  Array.prototype.contains = function(element){
    return this.indexOf(element) > -1;
  };

  Array.prototype.remove = function(elem, all) {
    for (var i=this.length-1; i>=0; i--) {
      if (this[i] === elem) {
          this.splice(i, 1);
          if(!all)
            break;
      }
    }
    return this;
  };

  //stbststus1();
  populateTestSuite();
  
  // var count=1;
  // $(".scrollingHead").find('tr>th').each(function( event ) {        
  //   var thWdith=$(this).outerWidth();
  
  //   $(".scrollingBody").find('tr>td:nth-child('+count+')').outerWidth(thWdith);       
  //   count++;
  // });
});

// function checkStatus($event) { 
//   if ($event.value && $event.checked == true) {
//     $event.setAttribute("checked", "checked");
//   }
//   else{
//     $event.removeAttribute("checked", "checked");
//   }
// }

// function stb2(job, build) {
//   $.post("stopJob", {"Job Number":job, "Build Number":build}, function(result){
//     location.reload();
//   });
// }

// function stb1(job1, build1){
//     $.get("stopJob",{ job: job1, build: build1 },function(result){
//      });
// }

// function stbststus1(){
//     $.getJSON("JobStatus", function(result) {
//       $("#testdataid").empty();
//         $.each(result, function(i, item){    
// 		    var status;
//         if(item.Result == "SUCCESS"){
//           resultclass = "result_available";
// 		      linkclass = "";
//   		    status = "disabled";
//         }
//         if(item.Result == "FAILURE"){
//           resultclass = "result_offline";
// 		      linkclass = "";
//           status = 'disabled';
// 		    }
//         if(item.Result == "IN PROGRESS"){
//           resultclass = "result_progress";
// 		      linkclass = "";
//           status = '';
// 		    }
//         if(item.Result == "IN QUEUE"){
//           resultclass = "result_queue";
// 		      linkclass = "";
// 		      status = '';
//         }
//         if(item.Result == "ABORTED"){
//           resultclass = "result_aborted";
// 		      linkclass = "";
// 		      status = 'disabled';
//         }
           
// 			$("#testdataid").append("<tr><td style='padding:14px; width:20px; text-align:center'></td><td style='padding-left:36px; width:66px; text-align:center'><input type='checkbox' name='check2' "+status+" value ='"+ item["Job No"] +","+item["Build No"]+"'></td><td style='width:37px; text-align: center'><label>"+item["Job No"]+" </label></td><td class='suite-name' style='width:88px; text-align: center'>"+item["Suite Name"]+"</td><td style='width:52px; text-align: center'>"+item["Build No"]+"</td><td class = " + resultclass + " style='width:72px; text-align: center'>" + item.Result + "</td><td style='width:135px; text-align: center'>" + item.StartTime + "</td><td style='width:135px; text-align: center'>" + item.EndTime + "</td><td style='width:77px; text-align: center'>" + item.Duration +" </td><td style='width:59px; text-align: center'>" + item.UserName +" </td><td style='width:202px; text-align: center'><button onclick=\"stb1('"+item["Job No"]+"',"+item["Build No"]+")\" data-role=\"button\" class=\"btn_stop btn btn-danger\">Stop</button></td><td style='width:237px; text-align: center'><a href=\"#\" onclick=\"showConsole(this)\" class="+ linkclass +">Console Output</a></td></tr>");
//         });
//     }) 
// }

function showConsole(job_name, build_num, suite_name) {
  var title = "JOB: " + job_name +",    SUITE NAME:  " + suite_name;

  $.ajax({
    url: window.config.buildConsole ,
    type: "get",
    data:{"job": job_name, "build" : build_num },
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
      
             if (checkboxes[i].type == 'checkbox') {
                 checkboxes[i].checked = false;
             }
         }
     }
 }


 // // function singleCheck(ele) {
	// //  var checkboxes = document.getElementsByName('check2');
	// //  console.log($(checkboxes+':checked').length,$(checkboxes).length,'----',ele);
	
	// //  if($(checkboxes+':checked').length == $(checkboxes).length){
	// //  console.log('inside')
	// // 	$('.parent_chk_job').prop("checked",true);
	// //  }
	// //  else{
	// // 	$('.parent_chk_job').prop("checked",false);
	// // 	}
	 
	
	 
 // }

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

// $(function () {
//     $("input[type='checkbox']").change(function () {
//         $(this).siblings('ul')
//             .find("input[type='checkbox']")
//             .prop('checked', this.checked);
//     });
// });

// /*parent child checkbox*/
// $(document).ready(
//     function() {
		 
// 		  $(".parentCheckBox1").on("click", function(){
		
// 				var chkval = $(this).attr("data-chk");
				
// 				$(".tab-pane").removeClass('active');
// 				$('.chk'+ chkval).attr('checked', this.checked);
// 				$('.view_chk'+ chkval).addClass('active');/**/
				
//             }
//         );
//         //clicking the last unchecked or checked checkbox should check or uncheck the parent checkbox
//         $('.childCheckBox').click(
//             function() {
//                 if ($(this).parents('label:eq(0)').find('.parentCheckBox').attr('checked') == true && this.checked == false)
//                     $(this).parents('label:eq(0)').find('.parentCheckBox').attr('checked', false);
//                 if (this.checked == true) {
//                     var flag = true;
//                     $(this).parents('label:eq(0)').find('.childCheckBox').each(
// 	                    function() {
// 	                        if (this.checked == false)
// 	                            flag = false;
// 	                    }
//                     );
//                     $(this).parents('label:eq(0)').find('.parentCheckBox').attr('checked', flag);
//                 }
//             }
//         );
		
// 		$('.nav-tabs a').click(function(){

// 		$('.nav-tabs a').parent().removeClass('selectCheckbox');
// 		$(this).parent().addClass('selectCheckbox');
// 	});
		
//     }
// );

function parentClick(e){		
	$(".tab-pane").removeClass('active');
	var j = $(e.target).attr("data-chk");
	 if($(e.target).is(":checked")){
              $('.chk'+j).prop('checked',true);
			  $(e.target).parent().parent().addClass('selectCheckbox');
        }else{
		$('.chk'+j).prop('checked',false);
		  $(e.target).parent().parent().removeClass('selectCheckbox');
		}
	$('.view_chk'+j).addClass('active');
}

function navClick(e){
  $('.nav-tabs a').parent().removeClass('selectCheckbox');
  $(e.target).parent().addClass('selectCheckbox');
}

// var tabsFn = (function() {
//   function init() {
//     //setHeight();
//   }
  
//   function setHeight() {
//     var $tabPane = $('.tab-pane'),
//         tabsHeight = $('.nav-tabs').height();
    
//     $tabPane.css({
//       height: tabsHeight
//     });
//   }
    
//   $(init);
// })();

/*datetime*/
	$(function() {
		$("#schedule_date").datepicker({ minDate: 0, dateFormat: 'yy/mm/dd' });   
		$('#schedule_time').timepicker({
			
			onHourShow: function( hour ) { 
				var now = new Date();
				if ( $('#schedule_date').val() == $.datepicker.formatDate ( 'yy/mm/dd', now ) ) {
					if ( hour <= now.getHours() ) {
						return false;
					}
				}
				return true;
			}
		});
	});

function populateTestSuite() {
    $.getJSON("test-suite-cases", function(result) {
      var parentresult, childresult,i = 0,j=0;
  
          $.each(result,function(item,childItem){
            var active='';
            if(j==0) {
              active='selectCheckbox';
            }
            parentresult = "";
            parentresult = "<li ><label class='checkbox "+active+" revo_dropdown' name='suites'  for='one' >";
            parentresult += "<a href='#' id='btn-1' data-target='#submenu"+j+"' aria-expanded='false'>";
            parentresult += "<input name='suites' value=\'"+item+"\' onclick='parentClick(event)' type='checkbox' class='parentCheckBox' data-chk="+j+"  data-count=\'"+j+"\' data-len=\'"+childItem.length+"\' /></a>";
            parentresult += "<a href='#testsuite"+j+"' data-toggle='tab' onclick='navClick(event)'>"+item+"</a></label></li><hr>";
            $("#testsuite ul").append(parentresult);
            
            if(j==0) {
              active='active';
            }
            childresult ="<div class='tab-pane "+active+" view_chk"+j+" ' id='testsuite"+j+"'><ul class='nav' id='submenu"+j+"' role='menu' aria-labelledby='btn-1'>";
          
            $.each(childItem, function(child,val){
              childresult += "<li><label class='checkbox' for='one' class='revo_dropdown'><input type='checkbox' class='childCheckBox chk"+j+"' name='cases' value=\'"+val+"\'  />"+val+"</label></li><hr>";
              i++;
            });
            childresult +="</ul></div>";
            j++;
            $("#testcase").append(childresult);
          });    
    });
}

$.fn.serializeObject = function() {
    var runRevoJson = {};
    runRevoJson['scheduled']= false;
    runRevoJson['time']='';
    runRevoJson['stbs']=[];
    runRevoJson['suites']=[];
    
    var count=0;
      var o = {};
      var a = this.serializeArray();
      var scheduled = [];
      var suite = [];
      var casesarry = [];
      var date='';
      
      $.each(a, function(key,values) {
        if(values.name=='schedule'){
          scheduled = values.value;
        }
        if(values.name=='date'){
          date=values.value;
        }        
        if(values.name=='time'){
          runRevoJson['time'] = date+' '+values.value;
        }
        if(values.name=='stbs'){        
          var x=values.value;
          suite.push(x);
        }
        if(values.name=='cases'){
          casesarry.push(values.value);
        }         
        if(values.name=='suites'){
          runRevoJson['suites'].push({'name':values.value,'cases':null});
          count++;
        }
      });
      runRevoJson['stbs'] = suite;
      
      var all=0, count=0;
      $('.parentCheckBox:checked').each(function(){
        var len=$(this).attr('data-len');
        var arrycases=[];
        len=parseInt(len)+ parseInt(all);
        
        for(var i=all; i<len; i++) {
          arrycases.push(casesarry[i]);
        }
        all=parseInt(arrycases.length)+parseInt(all);
        runRevoJson['suites'][count].cases=arrycases;
        count++;
      });

      window.runRevoJson = runRevoJson;
    };

$(function() {
  $('form').submit(function() {
    event.preventDefault();
    $('form').serializeObject();

    $.ajax({
      type: "POST",
      url: window.config.revo_run,
      data: JSON.stringify(window.runRevoJson),
      success: function(response) {
      },
      dataType: "json",
      contentType : "application/json"
    });
    window.location.href = window.config.revo;
    return false;
  });
});