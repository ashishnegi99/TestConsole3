$(document).ready(function() {
	var menuItems = {
						"menu-0": {
							"id": "menu-0",
							"title": "Home",
							"icon": "glyphicon glyphicon-home",
							"parentId": null,
							"url": "http://127.0.0.1:8000/",
							"childCount": 0,
							"classname" : "home"
						},
						"menu-1": {
							"id": "menu-1",
							"title": "Reports",
							"icon": "glyphicon glyphicon-list-alt",
							"parentId": null,
							"url": "/Reports",
							"childCount": 0,
							"classname" : "Reports"
						},
						"menu-5": {
							"id": "menu-5",
							"title": "Revo",
							"icon": "glyphicon glyphicon-th",
							"parentId": null,
							"url": "/revo",
							"childCount": 1,
							"classname" : "revo"
						},
						"menu-4": {
							"id": "menu-4",
							"title": "Configuration",
							"icon": "glyphicon glyphicon-cog",
							"parentId": "menu-5",
							"url": "",
							"childCount": 4,
							"classname" : "config"
						},
						"menu-6": {
							"id": "menu-6",
							"title": "Devices",
							"icon": "",
							"parentId": "menu-4",
							"url": "/revo/devices",
							"childCount": 0,
							"classname" : "devices"
						},
						"menu-7": {
							"id": "menu-7",
							"title": "Test Suites",
							"icon": "",
							"parentId": "menu-4",
							"url": "/revo/test_suites",
							"childCount": 0,
							"classname" : "test_suites"
						},
						"menu-8": {
							"id": "menu-8",
							"title": "Test Cases",
							"icon": "",
							"parentId": "menu-4",
							"url": "/revo/test-case",
							"childCount": 0,
							"classname" : "test-case"
						},
						"menu-9": {
							"id": "menu-9",
							"title": "Slave Configurations",
							"icon": "",
							"parentId": "menu-4",
							"url": "/revo/configs",
							"childCount": 0,
							"classname" : "configs"
						},
						"menu-10": {
							"id": "menu-10",
							"title": "Storm",
							"icon": "glyphicon glyphicon-picture",
							"parentId": null,
							"url": "/Storm",
							"childCount": 0,
							"classname" : "Storm"
						},
						"menu-11": {
							"id": "menu-11",
							"title": "Appium",
							"icon": "glyphicon glyphicon-check",
							"parentId": null,
							"url": "/Appium",
							"childCount": 0,
							"classname" : "Appium"
						}
					};
					
	function recurseMenu(parent) {
		var flag = 0;
		if(parent == undefined){
			var s = '<ul>';
		}else if(parent != undefined){
			var s = '<ul class="submenu">';			
		}
		for (var x in menuItems) {
			var url2 = menuItems[x].title;
			if (menuItems[x].parentId == parent) {
				if(menuItems[x].childCount > 1){ 
					s +='<div class="accordion-body panel-collapse collapse scroller" role="tab" id="RevoCollapse">';
					s +='<li class="'+ menuItems[x].classname+'"><div class="accordion-heading">';
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#ConfigCollapse" aria-expanded="false" class="collapsed more-less glyphicon glyphicon-large glyphicon-chevron-right config-open" id="revo_openclose2" title="Configuration"></i>'
					s +='<a title="'+ menuItems[x].title+'" class="config_link">' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</div></li></div><hr>';	
				}
				else if(menuItems[x].childCount == 1){
					s +='<div class="accordion" id="accordion2"><li class="'+ menuItems[x].classname+'"> <div class="accordion-heading">';
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#RevoCollapse" aria-expanded="false" class="more-less glyphicon glyphicon-large glyphicon-chevron-right config-open" id="revo_openclose" title="Configuration"></i>';
					s +='<a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'"class="revo_link">' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</div></li><hr></div>';
				}
				else{
					if(parent == undefined){
						s += '<li class="'+ menuItems[x].classname+'"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'" >' + menuItems[x].title +'</a>';
						s += '</li><hr>';
					}
					else{
						if(parent != undefined && menuItems[x].childCount == 0 && flag == 0){
							s +='<div class="accordion-body panel-collapse collapse scroller" role="tab" id="ConfigCollapse">';
						}
						if(menuItems[x].parentId != null){
							s += '<li class="'+ menuItems[x].classname+'"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'" ><span class="'+ menuItems[x].icon+'"></span>' + menuItems[x].title +'</a>';
							s += '</li><hr>';
							flag ++;
						}
						if(flag == menuItems[menuItems[x].parentId].childCount ){
							s += '</div>';
						}
					}					
				}
			}
		}
		return s + '</ul>';
	}
	$("#listContainer").html(recurseMenu());	
	
	var link=window.location.href.toString().split(window.location.host);	
	var activeUrl=link[1].split('/');
	if(activeUrl[1] =="" ){
		activeUrl[1] = "home";
		$("."+activeUrl[1]).addClass('active-colors');
	}
	if(activeUrl[2] == ""){
		$("."+activeUrl[1]).addClass('active-colors');
	}
	else{
		$("."+activeUrl[1]).addClass('active-colors');
		$("."+activeUrl[2]).addClass('active-colors');
	}
		
	for (var x in menuItems) {
		if(activeUrl[2] == menuItems[x].classname){
			$(".submenu").addClass('active');
			$(activeUrl[2]).addClass('active-colors');
			$('#RevoCollapse').addClass('in');
			$('#ConfigCollapse').addClass('in');
		}	
	}	
	
	$("#openNav").css('display','none');
	$("#mySidenav").css('display','block');
	$(".bars").hide();
	$("#closeNav").click(function(){
		$(".content").css('marginLeft','0');
		$("#openNav").css('display','block');
		$("#mySidenav").css('display','none');
		$(".bars").hide();
	});
	$("#openNav").click(function(){
		$(".content").css('marginLeft','250px');
		$("#openNav").css('display','none');
		$("#mySidenav").show();
		$(".bars").hide();
	});
	
	$('#RevoCollapse').on('shown.bs.collapse', function () {
       $("#revo_openclose").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
    });
    $('#RevoCollapse').on('hidden.bs.collapse', function () {
       $("#revo_openclose").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
    });
	$('#ConfigCollapse').on('shown.bs.collapse', function () {
       $("#revo_openclose2").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
    });
    $('#ConfigCollapse').on('hidden.bs.collapse', function () {
       $("#revo_openclose2").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
	   $("#revo_openclose").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
    });
	if ( $('ul.submenu').hasClass('active') ) {
		$("#revo_openclose").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
		$("#revo_openclose2").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");	   
    };
	function openNav() {
		document.getElementById("mySidenav").style.width = "250px";
		/*document.getElementById("main").style.marginLeft = "250px";*/
	}
	function closeNav() {
		document.getElementById("mySidenav").style.width = "0";
		document.getElementById("main").style.marginLeft= "0";
	}
});
