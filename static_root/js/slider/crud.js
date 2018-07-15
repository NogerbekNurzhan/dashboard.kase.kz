$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#slide-modal .modal-content").html(data.html_form);
				customField();
				$("#slide-modal").modal("show");
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/slide/';
				}
			},
		});
	};
	var saveForm = function(success_message) {
		var form = $(this);
		var formData = new FormData(form[0]);
		$.ajax({
			url: form.attr("action"),
			data: formData,
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					$("#loader").show("slow");
					$('body').tooltip({selector:'[rel=tooltip]'});
					setTimeout(function() {
						$("#loader").hide("slow");
						$("#slides").html(data.html_slides);
						$("#slides").sortable("refresh");
						$("#slides").sortable("option", "disabled", $("#slides .list-group-item").length == 1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#slide-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#slide-modal .modal-content").html(data.html_form);
					customField();
					$("#slide-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#slide-errors .error-description").html(error_message);
					setTimeout(function() {$("#slide-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/slide/';
				} else {
					$("#slide-errors").fadeIn("slow");
					$("#slide-errors .error-description").html(thrownError);
					setTimeout(function() {$("#slide-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};
	function customField() {
		autosize(document.querySelectorAll('.custom-body-textarea'));
		$("#slide-modal").on("focus", "textarea", function () {autosize.update(document.querySelectorAll('textarea'));});
		$('#location').select2({minimumResultsForSearch: Infinity, placeholder: "Выберите местоположение слайда...",});
	}

	$("#slide-сreate-btn").click(loadForm);
	$("#slide-modal").on("submit", ".slide-create-form", function(e) {e.preventDefault(); saveForm.call(this, "Новый слайд успешно создан!");});

	$("#slides").on("click", ".slide-edit-btn", loadForm);
	$("#slide-modal").on("submit", ".slide-edit-form", function(e) {e.preventDefault(); saveForm.call(this, "Данные успешно сохранены!");});

	$("#slides").on("click", ".slide-delete-btn", loadForm);
	$("#slide-modal").on("submit", ".slide-delete-form", function(e) {e.preventDefault(); saveForm.call(this, "Слайд успешно удален!");});

	$('#slide-modal').on('hidden.bs.modal', function () {$("#slide-modal .modal-content").empty();});
});