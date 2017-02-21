$(document).ready(function() {
	function toggleIcon(e) {
		$(e.target)
		.prev('.accordion-heading')
		.find(".more-less")
		.toggleClass('glyphicon-chevron-left glyphicon-chevron-down');
	}
	$('.panel-grp').on('hidden.bs.collapse', toggleIcon);
	$('.panel-grp').on('shown.bs.collapse', toggleIcon);
	
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
					s +='<div class="accordion-body panel-collapse collapse scroller" role="tab" id="collapseOne">';
					s +='<li class="'+ menuItems[x].classname+'"><div class="accordion-heading">';
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#collapseOneOne" aria-expanded="false" class="collapsed more-less glyphicon glyphicon-chevron-right config-open" id="revo_openclose" title="Sub Menu"></i>';
					
					s +='<a title="'+ menuItems[x].title+'" class="config_link"><span class="'+ menuItems[x].icon+'"></span>' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</div></li></div><hr>';
				}
				
				else if(menuItems[x].childCount == 1){ 
					s +='<div class="accordion" id="accordion2"><li class="'+ menuItems[x].classname+'">';
					s +='<i role="button" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne" aria-expanded="false" class="collapsed more-less glyphicon glyphicon-chevron-right config-open" id="revo_openclose" title="Configuration"></i>';
					s +='<a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'"><span class="'+ menuItems[x].icon+'"></span>' + menuItems[x].title +'</a>';
					s += recurseMenu(menuItems[x].id);
					s += '</li><hr></div>';
				}

				else{
					if(parent == undefined){
						s += '<li class="'+ menuItems[x].classname+'"><a href="'+ menuItems[x].url +'" title="'+ menuItems[x].title+'" ><span class="'+ menuItems[x].icon+'"></span>' + menuItems[x].title +'</a>';
						s += '</li><hr>';
					}
					else{
						if(parent != undefined && menuItems[x].childCount == 0 && flag == 0){
							s +='<div class="accordion-body panel-collapse collapse scroller" role="tab" id="collapseOneOne">';
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
		  $('#collapseOne').addClass('in');
		  $('#collapseOneOne').addClass('in');
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
});