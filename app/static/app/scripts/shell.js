$(document).ready(function() {
	var menuItems = {
						"menu-0": {
							"id": "menu-0",
							"title": "Home",
							
							"icon": "/static/app/images/home.png",
							
							"parentId": null,
							"url": "http://127.0.0.1:8000/",
							"childCount": 0,
							"classname" : "home"
						},
						"menu-1": {
							"id": "menu-1",
							"title": "Reports",
						
							"icon": "/static/app/images/reports.png",
							"parentId": null,
							"url": "/Reports",
							"childCount": 0,
							"classname" : "Reports"
						},
						"menu-5": {
							"id": "menu-5",
							"title": "Revo",
							
							"icon": "/static/app/images/revo.png",
							"parentId": null,
							"url": "/revo",
							"childCount": 1,
							"classname" : "revo"
						},
						"menu-4": {
							"id": "menu-4",
							"title": "Configuration",
							
							"icon": "/static/app/images/config.png",
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
							
							"icon": "/static/app/images/storm.png",
							"parentId": null,
							"url": "/Storm",
							"childCount": 0,
							"classname" : "Storm"
						},
						"menu-11": {
							"id": "menu-11",
							"title": "Appium",
							
							"icon": "/static/app/images/appium.png",
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
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#ConfigCollapse" aria-expanded="false" class="more-less collapsed glyphicon glyphicon-large glyphicon-chevron-right config-open" id="revo_openclose2" title="Configuration"></i>'
					s +='<img src="'+ menuItems[x].icon+'" alt="'+ menuItems[x].classname+'" class="img-responsive menu_icon"><a title="'+ menuItems[x].title+'" class="config_link">' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</div></li></div><hr>';	
				}
				else if(menuItems[x].childCount == 1){
					
					s +='<div class="accordion" id="accordion2"><li class="'+ menuItems[x].classname+'"> <div class="accordion-heading">';
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#RevoCollapse" aria-expanded="false" class="more-less glyphicon glyphicon-large glyphicon-chevron-right config-open" id="revo_openclose" title="Configuration"></i>';
					s +='<img src="'+ menuItems[x].icon+'" alt="'+ menuItems[x].classname+'" class="img-responsive menu_icon2"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'"class="revo_link">' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</div></li><hr></div>';
				}
				else{
					if(parent == undefined){
					
						s += '<li class="'+ menuItems[x].classname+'"><img src="'+ menuItems[x].icon+'" alt="'+ menuItems[x].classname+'" class="img-responsive menu_icon2"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'" >' + menuItems[x].title +'</a>';
						s += '</li><hr>';
					}
					else{
						if(parent != undefined && menuItems[x].childCount == 0 && flag == 0){
							s +='<div class="accordion-body panel-collapse collapse scroller" role="tab" id="ConfigCollapse">';
						}
						if(menuItems[x].parentId != null){
							s += '<li class="'+ menuItems[x].classname+'"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'" >' + menuItems[x].title +'</a>';
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
	var activeUrl2=window.location.search;
	
	var subpath = activeUrl[1].split("?");
	
	if(subpath[0] =="" ){
		
		subpath[0] = "home";
		
		$("."+subpath[0]).addClass('active-colors');
	}
	else{
		$("."+subpath[0]).addClass('active-colors');
	}
	
	
	
	if(!activeUrl[2]){
		
		$("."+subpath[0]).addClass('active-colors');
	}
	else{
		$("."+subpath[0]).addClass('active-colors');
		
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
	
	$(function(){
		$('#revo_openclose').click(function(){
			if ( $('#revo_openclose').hasClass('glyphicon-chevron-down') ) {
				$("#revo_openclose").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
			};
		});
	});
	
});
