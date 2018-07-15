$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#video-modal .modal-content").html(data.html_form);
				fieldSettings();
				$("#video-modal").modal("show");
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/video/';
				}
			},
		});
	};

	var createSaveForm = function(success_message) {
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
						if(data.video_exist){
							$("#videos").prepend(data.html_video);
						}
						else{
							$("#videos").html(data.html_videos);
						}
						$("#videos").sortable("refresh");
						$("#videos").sortable("option", "disabled", $("#videos .list-group-item").length == 1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#video-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#video-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#video-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#video-errors .error-description").html(error_message);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/video/';
				} else {
					$("#video-errors").fadeIn("slow");
					$("#video-errors .error-description").html(thrownError);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	var editSaveForm = function(success_message) {
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
						$('div[data-id='+data.video_id+']').replaceWith(data.html_video);
						$("#videos").sortable("refresh");
						$("#videos").sortable("option", "disabled", $("#videos .list-group-item").length == 1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#video-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#video-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#video-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#video-errors .error-description").html(error_message);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/video/';
				} else {
					$("#video-errors").fadeIn("slow");
					$("#video-errors .error-description").html(thrownError);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	var deleteSaveForm = function(success_message) {
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
						if(data.video_exist){
							$('div[data-id='+data.video_id+']').remove();
						}
						else{
							$("#videos").html(data.html_videos);
						}
						$("#videos").sortable("refresh");
						$("#videos").sortable("option", "disabled", $("#videos .list-group-item").length == 1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#video-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#video-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#video-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#video-errors .error-description").html(error_message);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/video/';
				} else {
					$("#video-errors").fadeIn("slow");
					$("#video-errors .error-description").html(thrownError);
					setTimeout(function() {$("#video-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	function fieldSettings() {
		autosize(document.querySelectorAll('.custom-body-textarea'));
		$("#video-modal").on("focus", "textarea", function () {autosize.update(document.querySelectorAll('textarea'));});
		$('#category_id').select2({minimumResultsForSearch: Infinity, placeholder: "Выберите категорию видео...",});
	}
	
	$("#video-create-btn").click(loadForm);
	$("#video-modal").on("submit", ".video-create-form", function(e) {
		e.preventDefault();
		createSaveForm.call(this, "Новая запись успешно создана!");
	});

	$("#videos").on("click", ".video-edit-btn", loadForm);
	$("#video-modal").on("submit", ".video-edit-form", function(e) {
		e.preventDefault();
		editSaveForm.call(this, "Данные успешно сохранены!");
	});

	$("#videos").on("click", ".video-delete-btn", loadForm);
	$("#video-modal").on("submit", ".video-delete-form", function(e) {
		e.preventDefault();
		deleteSaveForm.call(this, "Запись успешно удалена!");
	});

	$('#video-modal').on('hidden.bs.modal', function () {
		$("#video-modal .modal-content").empty();
	});
});