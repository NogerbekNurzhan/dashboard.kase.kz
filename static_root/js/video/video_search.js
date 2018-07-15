(function ($) {
	jQuery.expr[':'].Contains = function(a,i,m){
		return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
	};
	function filterList(header, list) {
		var $empty_list_group = $('#empty-list-group');
		$("#search-videos").change( function () {
			var filter = $(this).val();
			if(filter) {
				$matches = $(list).find('.search_by:Contains(' + filter + ')').parent();
				$('.list-group-item', list).not($matches).hide();
				$matches.show();
				$empty_list_group.hide();
				$("#videos").sortable("refresh");
				$("#videos").sortable("option", "disabled", $matches.length==1);
				if($matches.length){
					$empty_list_group.hide();
				}
				else{
					$empty_list_group.show();
				}
			} else {
				$(list).find(".list-group-item").show();
				$empty_list_group.hide();
			}
			return false;
		}).keyup( function () {
			$empty_list_group.hide();
			$(this).change();
		});
	}
	$(function () {
		filterList($("#search-videos"), $("#videos"));
	});
}(jQuery));