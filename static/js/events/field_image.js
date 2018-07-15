$("#event-modal").on("click", "#image-field-clear-btn", function() {
	$('#image-field-file-name').val("");
	$('#image-field-clear-btn').hide();
	$('#image-field-input input:file').val("");
	$("#image-field-input-title").text("Добавить изображения");
});
$("#event-modal").on("change", "#image-field-input input:file", function() {
	var files = $.map(this.files, function(val){ return val.name; });
	$("#image-field-input-title").text("Изменить изображения");
	$("#image-field-clear-btn").show();
	$("#image-field-file-name").val(files.join(', '));
});