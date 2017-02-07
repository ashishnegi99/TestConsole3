$(document).ready(function() {
	function toggleIcon(e) {
		$(e.target)
			.prev('.panel-heading')
			.find(".more-less")
			.toggleClass('glyphicon-chevron-left glyphicon-chevron-down');
	}
	$('.panel-grp').on('hidden.bs.collapse', toggleIcon);
	$('.panel-grp').on('shown.bs.collapse', toggleIcon);
});