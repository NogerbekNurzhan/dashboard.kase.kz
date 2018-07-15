$("#document-modal").on("click", "#file-field-clear-btn", function() {
	$('#file-field-file-name').val("");
	$('#file-field-clear-btn').hide();
	$('#file-field-input input:file').val("");
	$("#file-field-input-title").text("Добавить файл");
});
$("#document-modal").on("change", "#file-field-input input:file", function() {
	var file = this.files[0];
	var reader = new FileReader();
	reader.onload = function (e) {
		$("#file-field-input-title").text("Изменить файл");
		$("#file-field-clear-btn").show();
		$("#file-field-file-name").val(file.name);
	}
	reader.readAsDataURL(file);
});