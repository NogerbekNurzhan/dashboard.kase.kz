$(function () {
	$("#static-pages").sortable({
		start: function (event, ui) {
			ui.placeholder.height(ui.item.height());
		},
		stop: function(event, ui) {
			static_page_order = {};
			$("#static-pages").children().each(function(){
				static_page_order[$(this).data('id')] = $(this).index();
			});
			$.ajax({
				url: "sorting/",
				type: "post",
				contentType: 'application/json; charset= utf-8',
				dataType: 'json',
				data: JSON.stringify(static_page_order)
			});
		},
		disabled: $("#static-pages .list-group-item").length == 1
	});
});