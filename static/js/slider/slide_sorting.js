$(function () {
	$("#slides").sortable({
		start: function (event, ui) {
			ui.placeholder.height(ui.item.height());
		},
		stop: function(event, ui) {
			slide_order = {};
			$("#slides").children().each(function(){
				slide_order[$(this).data('id')] = $(this).index();
			});
			$.ajax({
				url: "sorting/",
				type: "post",
				contentType: 'application/json; charset= utf-8',
				dataType: 'json',
				data: JSON.stringify(slide_order)
			});
			console.log(slide_order);
		},
		disabled: $("#slides .list-group-item").length == 1
	});
});