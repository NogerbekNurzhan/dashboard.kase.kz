$(function () {
	// Section Sorting
	$("#sections").sortable({
		handle: '.section-drag-and-drop-btn',
		stop: function(event, ui) {
			section_order = {};
			$("#sections").children().each(function(){
				section_order[$(this).data('id')] = $(this).index();
			});
			$.ajax({
				url: "section_sorting/",
				type: "post",
				contentType: 'application/json; charset= utf-8',
				dataType: 'json',
				data: JSON.stringify(section_order)
			});
		},
	}).disableSelection();

	// Indicators Sorting
	$('#section-0, #section-1, #section-2, #section-3, #section-4, #section-5, #section-6, #section-7, #section-8, #section-9').sortable({
		opacity: 0.5,
		connectWith: '.indicators',
		items : 'div:not(.empty-list-group-item)',

		start : function(event, ui) {
			myArguments = {}; // Reset the array
		},

		out: function(event, ui){
			if($('div:not(.empty-list-group-item, .ui-sortable-placeholder)', this).length===0){
				ui.placeholder.hide();
				return $('div.empty-list-group-item', this).show();
			}
		},

		over: function(event, ui){
			ui.placeholder.show();
			if($('div[id='+ui.item.attr("id")+']').closest('.list-group').children().length==2){
				$('div[id='+ui.item.attr("id")+']').closest('.list-group').find('.empty-list-group-item').first().show();
			}
			if($('div[id='+ui.item.attr("id")+']').closest('.list-group').children().length>2){
				$('div[id='+ui.item.attr("id")+']').closest('.list-group').find('.empty-list-group-item').first().hide();
			}
			if(event.target.childElementCount<2){
				$(event.target).parent().find('.empty-list-group-item').first().show();
			}
			if(event.target.childElementCount==2){
				$(event.target).parent().find('.empty-list-group-item').first().hide();
			}
		},

		remove : function(event, ui) {
			// Get array of items in the list where we removed the item
			myArguments = assembleData(this, myArguments);
		},

		receive : function(event, ui) {
			// Get array of items where we added a new item
			myArguments = assembleData(this, myArguments);
		},

		update: function(e, ui) {
			if (this === ui.item.parent()[0]) {
				 // In case the change occures in the same container
				 if (ui.sender == null) {
					myArguments = assembleData(this, myArguments);
				}
			}
		},

		beforeStop: function(event, ui){
			refreshEmptyListGroupItem
		},

		stop : function(event, ui) {
			// Send JSON to the server
			$.ajax({
				url: "indicator_sorting/",
				type: "post",
				contentType: 'application/json; charset= utf-8',
				dataType: 'json',
				data: JSON.stringify(myArguments)
			});
		},
	});

	var myArguments = {}; // Here we will store all data

	function assembleData(object, arguments){		
		var data = $(object).sortable('toArray'); // Get array data 
		var section_id = $(object).attr("id"); // Get section_id and we will use it as property name
		var arrayLength = data.length;
		// Create section_id property if it does not exist
		if(!arguments.hasOwnProperty(section_id)) 
		{
			arguments[section_id] = new Array();
		}
		// Loop through all items
		for (var i = 0; i < arrayLength; i++) 
		{
			var indicator_id = data[i];	
			// push all indicator_id onto property section_id (which is an array)
			arguments[section_id].push(indicator_id);
		}
		return arguments;
	}
});