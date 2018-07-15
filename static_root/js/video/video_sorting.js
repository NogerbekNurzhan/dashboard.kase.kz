$(function () {
	$("#videos").sortable({
		start: function (event, ui) {
			ui.placeholder.height(ui.item.height());
		},
		stop: function(event, ui) {
			video_order = {};
			$("#videos").children().each(function(){
				video_order[$(this).data('id')] = $(this).index();
			});
			$.ajax({
				url: "sorting/",
				type: "post",
				contentType: 'application/json; charset= utf-8',
				dataType: 'json',
				data: JSON.stringify(video_order)
			});
			console.log(video_order);
		},
		disabled: $("#videos .list-group-item").length == 1
	});
});