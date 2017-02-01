$(window).resize(function() {
 $(".resize_table").removeClass('fixed_head');
  $(".resize_tbody").removeClass('stb_tbody');
   setTimeout( function(){
   var count1=0;
     $(".resize_table").find('tr>th').each(function( event ) {        
      
		var style = window.getComputedStyle(this, null).width;
		 
       $(".resize_tbody").find('tr>td:eq('+count1+')').attr('width',style);
	   	$(".resize_table").find('tr>th:eq('+count1+')').attr('width',style) ;     	  
		  
       count1++;
     });
	 var wid = $("#stb-table").outerWidth();
	 $("#example").css('width',wid+'px');
	 $(".resize_table").addClass('fixed_head');
  $(".resize_tbody").addClass('stb_tbody');
   },500);
  
 });

$(function() {
  populateTestSuite();
  runJobForm();
  handleTestSuiteCases();
  datetimepickerInit();
});

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


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
    runRevoJson['scheduled']= 'false';
    runRevoJson['time']='';
    runRevoJson['stbs']=[];
    runRevoJson['suites']=[];
    
    var count=0;
    var o = {};
    var a = this.serializeArray();
    var schedule = [];
    var suite = [];
    var casesarry = [];
    
    $.each(a, function(key,values) {
	  
  	  if(values.name=='schedule'){
  	   runRevoJson['scheduled'] = values.value;
  	  }  	
      if(values.name=='time'){
  		  runRevoJson['time'] = values.value;
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
}

function runJobForm() {
  $('#run-job').submit(function() {
    event.preventDefault();
    $('form').serializeObject();

    $.ajax({
      type: "POST",
      url: window.config.revo_run,
      data: JSON.stringify(window.runRevoJson),
      headers: { "X-CSRFToken":  getCookie('csrftoken') },
      success: function(response) {
      },
      dataType: "json",
      contentType : "application/json"
    });
    window.location.href = window.config.revo;
    return false;
  });
}

                function handleTestSuiteCases() {
						
                    var allOpts = $('#lstBoxMain option');
                    $('#lstBox1').append($(allOpts).clone());
                    var selectedOpts = $('#lstBox1 option:selected');
                    $('#lstBox2').append($(selectedOpts).clone());
                    $(selectedOpts).remove();

                    $('#btnRight').click(function (e) {
                        var selectedOpts = $('#lstBox1 option:selected');
                        if (selectedOpts.length == 0) {
                            alert("Nothing to move.");
                            e.preventDefault();
                        }
							
                        $('#lstBox2').append($(selectedOpts).clone());
                        $(selectedOpts).remove();

                        selectedOpts.each(function(key,opt) {
                            $('#lstBoxMain option[value="' + opt.value + '"]').prop('selected', true)
                        });
                        e.preventDefault();
                    });
					
                    $('#btnAllRight').click(function (e) {
                        var selectedOpts = $('#lstBox1 option');
                        if (selectedOpts.length == 0) {
                            alert("Nothing to move.");
                            e.preventDefault();
                        }
                        $('#lstBox2').append($(selectedOpts).clone());
                        $(selectedOpts).remove();
                        selectedOpts.each(function(key,opt) {
                            $('#lstBoxMain option[value="' + opt.value + '"]').prop('selected', true )
                        });
                        e.preventDefault();
                    });
                    $('#btnLeft').click(function (e) {
                        var selectedOpts = $('#lstBox2 option:selected');
                        if (selectedOpts.length == 0) {
                            alert("Nothing to move.");
                            e.preventDefault();
                        }
                        $('#lstBox1').append($(selectedOpts).clone());
                        $(selectedOpts).remove();
                        selectedOpts.each(function(key,opt) {
                            $('#lstBoxMain option[value="' + opt.value + '"]').prop('selected', false)
                        });
                        e.preventDefault();
                    });
                    $('#btnAllLeft').click(function (e) {
                        var selectedOpts = $('#lstBox2 option');
                        if (selectedOpts.length == 0) {
                            alert("Nothing to move.");
                            e.preventDefault();
                        }
                        $('#lstBox1').append($(selectedOpts).clone());
                        $(selectedOpts).remove();
                        selectedOpts.each(function(key,opt) {
                            $('#lstBoxMain option[value="' + opt.value + '"]').prop('selected', false)
                        });
                        e.preventDefault();
                    });
					
                }
				
function stb_table(){			
   var count=0;
   var td_array = [];
   $(".fixed_head").find('tr>th').each(function( event ) {
	 var thWdith = window.getComputedStyle(this, null).width;
	 td_array.push(thWdith);
	 $(".resize_table").find('tr>th:eq('+count+')').attr('width',thWdith);
	count++;
   });
   return td_array;
 }
   
function datetimepickerInit() {
  $('#datetimepicker1').datetimepicker({
    minDate: moment()
  });
}
