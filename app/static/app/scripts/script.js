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