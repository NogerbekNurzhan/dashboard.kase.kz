$("#slide-modal").on("click", "#image-field-clear-btn", function() {
	$('#image-field-file-name').val("");
	$('#image-field-clear-btn').hide();
	$('#image-field-input input:file').val("");
	$("#image-field-input-title").text("Добавить изображение");
});
$("#slide-modal").on("change", "#image-field-input input:file", function() {
	var file = this.files[0];
	var reader = new FileReader();
	reader.onload = function (e) {
		$("#image-field-input-title").text("Изменить изображение");
		$("#image-field-clear-btn").show();
		$("#image-field-file-name").val(file.name);
	}
	reader.readAsDataURL(file);
});